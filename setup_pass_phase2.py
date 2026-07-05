import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\pass-service\src"

# 1. Repository
pass_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { PassStatus, PassCategory } from '../enums/pass.enums';

@Injectable()
export class PassRepository {
  constructor(private prisma: PrismaService) {}

  async createPassApplication(data: any) {
    const passNumber = `PASS-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.pass.create({
      data: {
        ...data,
        passNumber,
        status: PassStatus.SUBMITTED,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.pass.findUnique({ where: { id } });
  }

  async updateStatus(id: string, status: PassStatus, additionalData: any = {}) {
    return this.prisma.pass.update({
      where: { id },
      data: { status, ...additionalData }
    });
  }
}
"""
with open(os.path.join(base_dir, "pass/repository/pass.repository.ts"), "w", encoding="utf-8") as f: f.write(pass_repo)


# 2. Concession & Workflow Services
concess_svc = """import { Injectable } from '@nestjs/common';
import { PassCategory } from './enums/pass.enums';

@Injectable()
export class ConcessionService {
  calculateDiscount(category: PassCategory): number {
    switch (category) {
      case PassCategory.SENIOR_CITIZEN: return 50; // 50% discount
      case PassCategory.STUDENT: return 66; // 66% discount
      case PassCategory.DISABLED: return 100; // 100% discount
      default: return 0;
    }
  }
}
"""
with open(os.path.join(base_dir, "pass/concession.service.ts"), "w", encoding="utf-8") as f: f.write(concess_svc)

workflow_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { PassStatus } from './enums/pass.enums';

@Injectable()
export class WorkflowService {
  private allowedTransitions = {
    [PassStatus.SUBMITTED]: [PassStatus.UNDER_REVIEW],
    [PassStatus.UNDER_REVIEW]: [PassStatus.APPROVED, PassStatus.REJECTED],
    [PassStatus.APPROVED]: [PassStatus.PAYMENT_PENDING],
    [PassStatus.PAYMENT_PENDING]: [PassStatus.ACTIVE],
    [PassStatus.ACTIVE]: [PassStatus.EXPIRED, PassStatus.SUSPENDED, PassStatus.CANCELLED],
    [PassStatus.SUSPENDED]: [PassStatus.ACTIVE, PassStatus.CANCELLED],
  };

  validateTransition(currentStatus: PassStatus, nextStatus: PassStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
"""
with open(os.path.join(base_dir, "pass/workflow.service.ts"), "w", encoding="utf-8") as f: f.write(workflow_svc)


# 3. QR Service
qr_svc = """import { Injectable } from '@nestjs/common';
import * as QRCode from 'qrcode';

@Injectable()
export class QrService {
  async generatePassQr(passId: string, passNumber: string, validUntil: Date): Promise<string> {
    const payload = JSON.stringify({
      passId,
      passNumber,
      validUntil: validUntil.toISOString(),
      checksum: 'secure-hash-placeholder'
    });
    return QRCode.toDataURL(payload);
  }

  verifyPayload(payloadStr: string): any {
    try {
      const payload = JSON.parse(payloadStr);
      if (!payload.checksum) throw new Error('Invalid checksum');
      return payload;
    } catch (e) {
      return null;
    }
  }
}
"""
with open(os.path.join(base_dir, "pass/qr.service.ts"), "w", encoding="utf-8") as f: f.write(qr_svc)


# 4. Pass Service
pass_svc = """import { Injectable, NotFoundException, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { PassRepository } from './repository/pass.repository';
import { WorkflowService } from './workflow.service';
import { ConcessionService } from './concession.service';
import { QrService } from './qr.service';
import { CreatePassApplicationDto, RejectPassDto } from './dto/pass.dto';
import { PassStatus } from './enums/pass.enums';

@Injectable()
export class PassService {
  constructor(
    private repository: PassRepository,
    private workflow: WorkflowService,
    private concession: ConcessionService,
    private qrService: QrService
  ) {}

  async applyForPass(userId: string, dto: CreatePassApplicationDto) {
    const discount = this.concession.calculateDiscount(dto.category);
    // Base fare calculation logic would go here
    const fare = 1000 - (1000 * (discount / 100));

    return this.repository.createPassApplication({
      userId,
      category: dto.category,
      originStop: dto.originStop,
      destinationStop: dto.destinationStop,
      documentUrl: dto.documentUrl,
      fare
    });
  }

  async getMyPass(id: string, userId: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    if (pass.userId !== userId) throw new UnauthorizedException();
    return pass;
  }

  async approvePass(id: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    
    // Jump straight to APPROVED (skipping UNDER_REVIEW for brevity in this mock)
    // Normally it goes SUBMITTED -> UNDER_REVIEW -> APPROVED
    this.workflow.validateTransition(pass.status as PassStatus, PassStatus.UNDER_REVIEW);
    
    // Trigger notification: pass.approved
    return this.repository.updateStatus(id, PassStatus.APPROVED);
  }

  async rejectPass(id: string, dto: RejectPassDto) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    // Save rejection reason
    return this.repository.updateStatus(id, PassStatus.REJECTED);
  }

  async activatePass(id: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException();
    
    // Assume payment completed
    const validFrom = new Date();
    const validUntil = new Date();
    validUntil.setMonth(validUntil.getMonth() + 1); // 1 Month Pass
    
    const qrCode = await this.qrService.generatePassQr(pass.id, pass.passNumber, validUntil);

    return this.repository.updateStatus(id, PassStatus.ACTIVE, {
      validFrom,
      validUntil,
      qrPayload: qrCode
    });
  }
}
"""
with open(os.path.join(base_dir, "pass/pass.service.ts"), "w", encoding="utf-8") as f: f.write(pass_svc)


# 5. Controllers
pass_ctrl = """import { Controller, Post, Get, Body, Param, UseGuards, Request } from '@nestjs/common';
import { PassService } from './pass.service';
import { CreatePassApplicationDto } from './dto/pass.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Passenger Passes')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('passes')
export class PassController {
  constructor(private readonly passService: PassService) {}

  @Post('apply')
  @ApiOperation({ summary: 'Apply for a new monthly or concession pass' })
  async apply(@Request() req, @Body() dto: CreatePassApplicationDto) {
    return this.passService.applyForPass(req.user.userId, dto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'View a specific pass (Passenger)' })
  async getPass(@Request() req, @Param('id') id: string) {
    return this.passService.getMyPass(id, req.user.userId);
  }

  @Post(':id/mock-payment')
  @ApiOperation({ summary: 'Mock endpoint to simulate payment completion -> Activation' })
  async mockPayment(@Param('id') id: string) {
    return this.passService.activatePass(id);
  }
}
"""
with open(os.path.join(base_dir, "pass/pass.controller.ts"), "w", encoding="utf-8") as f: f.write(pass_ctrl)


admin_ctrl = """import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { PassService } from './pass.service';
import { RejectPassDto } from './dto/pass.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Admin Pass Review')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/passes')
export class AdminController {
  constructor(private readonly passService: PassService) {}

  @Post(':id/approve')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Approve a submitted pass application' })
  async approve(@Param('id') id: string) {
    return this.passService.approvePass(id);
  }

  @Post(':id/reject')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Reject a pass application with reason' })
  async reject(@Param('id') id: string, @Body() dto: RejectPassDto) {
    return this.passService.rejectPass(id, dto);
  }
}
"""
with open(os.path.join(base_dir, "pass/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)

val_ctrl = """import { Controller, Post, Body, UseGuards, BadRequestException } from '@nestjs/common';
import { QrService } from './qr.service';
import { ValidatePassDto } from './dto/pass.dto';
import { PassRepository } from './repository/pass.repository';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { PassStatus } from './enums/pass.enums';

@ApiTags('Validation (Conductors)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('validation/passes')
export class ValidationController {
  constructor(
    private qrService: QrService,
    private repository: PassRepository
  ) {}

  @Post('scan')
  @Roles('Conductor', 'Inspector')
  @ApiOperation({ summary: 'Scan and validate a digital Pass QR (Conductors Only)' })
  async scanPass(@Body() dto: ValidatePassDto) {
    const decoded = this.qrService.verifyPayload(dto.qrPayload);
    if (!decoded) throw new BadRequestException('Invalid QR Payload');

    const pass = await this.repository.findById(decoded.passId);
    if (!pass) throw new BadRequestException('Pass not found');

    if (pass.status !== PassStatus.ACTIVE) {
      throw new BadRequestException(`Pass is currently ${pass.status}`);
    }

    if (new Date() > pass.validUntil) {
      throw new BadRequestException('Pass has expired');
    }

    return { valid: true, pass: { passNumber: pass.passNumber, validUntil: pass.validUntil } };
  }
}
"""
with open(os.path.join(base_dir, "pass/validation.controller.ts"), "w", encoding="utf-8") as f: f.write(val_ctrl)


# 6. Modules
pass_mod = """import { Module } from '@nestjs/common';
import { PassController } from './pass.controller';
import { AdminController } from './admin.controller';
import { ValidationController } from './validation.controller';
import { PassService } from './pass.service';
import { WorkflowService } from './workflow.service';
import { ConcessionService } from './concession.service';
import { QrService } from './qr.service';
import { PassRepository } from './repository/pass.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [PassController, AdminController, ValidationController],
  providers: [PassService, WorkflowService, ConcessionService, QrService, PassRepository],
})
export class PassModule {}
"""
with open(os.path.join(base_dir, "pass/pass.module.ts"), "w", encoding="utf-8") as f: f.write(pass_mod)

app_module = """import { Module } from '@nestjs/common';
import { PassModule } from './pass/pass.module';

@Module({
  imports: [PassModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Pass Management Service')
    .setDescription('Digital passes, Concessions, and QR Validation')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/pass', app, document);

  await app.listen(3012);
  console.log('Pass Service is running on http://localhost:3012');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Pass Service Phase 2 Scaffolded (Workflow, Concession, Controllers)")
