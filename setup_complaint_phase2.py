import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\complaint-service\src"

# 1. Repository
complaint_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ComplaintStatus, ComplaintPriority } from '../enums/complaint.enums';

@Injectable()
export class ComplaintRepository {
  constructor(private prisma: PrismaService) {}

  async createComplaint(data: any) {
    // Generate a reference number e.g. CMP-168923482
    const referenceId = `CMP-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.complaint.create({
      data: {
        ...data,
        referenceId,
        status: ComplaintStatus.OPEN,
        priority: ComplaintPriority.MEDIUM, // Default, updated by SLA engine later
      }
    });
  }

  async findById(id: string) {
    return this.prisma.complaint.findUnique({
      where: { id },
      include: { comments: true }
    });
  }

  async updateStatus(id: string, status: ComplaintStatus) {
    return this.prisma.complaint.update({
      where: { id },
      data: { status }
    });
  }

  async addComment(complaintId: string, authorId: string, content: string, isInternal: boolean) {
    return this.prisma.complaintComment.create({
      data: { complaintId, authorId, content, isInternal }
    });
  }
}
"""
with open(os.path.join(base_dir, "complaint/repository/complaint.repository.ts"), "w", encoding="utf-8") as f: f.write(complaint_repo)


# 2. SLA & Escalation Services
sla_svc = """import { Injectable } from '@nestjs/common';
import { ComplaintCategory, ComplaintPriority } from './enums/complaint.enums';

@Injectable()
export class SlaService {
  /**
   * Determines priority and resolution deadlines based on category.
   */
  calculateSla(category: ComplaintCategory) {
    if (category === ComplaintCategory.STAFF_BEHAVIOR) {
      return { priority: ComplaintPriority.HIGH, resolutionHours: 24 };
    }
    if (category === ComplaintCategory.DELAY) {
      return { priority: ComplaintPriority.LOW, resolutionHours: 72 };
    }
    return { priority: ComplaintPriority.MEDIUM, resolutionHours: 48 };
  }
}
"""
with open(os.path.join(base_dir, "complaint/sla.service.ts"), "w", encoding="utf-8") as f: f.write(sla_svc)

escalation_svc = """import { Injectable } from '@nestjs/common';
import { ComplaintRepository } from './repository/complaint.repository';
import { ComplaintStatus } from './enums/complaint.enums';

@Injectable()
export class EscalationService {
  constructor(private repository: ComplaintRepository) {}

  async escalateComplaint(id: string) {
    // In real app, this might be triggered by a Cron Job if SLA is breached
    await this.repository.updateStatus(id, ComplaintStatus.ESCALATED);
    // Trigger Kafka event for HQ Admin notification
    return { message: 'Complaint escalated successfully.' };
  }
}
"""
with open(os.path.join(base_dir, "complaint/escalation.service.ts"), "w", encoding="utf-8") as f: f.write(escalation_svc)


# 3. Complaint Service
complaint_svc = """import { Injectable, NotFoundException, BadRequestException, UnauthorizedException } from '@nestjs/common';
import { ComplaintRepository } from './repository/complaint.repository';
import { SlaService } from './sla.service';
import { CreateComplaintDto, ComplaintCommentDto } from './dto/complaint.dto';
import { ComplaintStatus } from './enums/complaint.enums';

@Injectable()
export class ComplaintService {
  constructor(
    private repository: ComplaintRepository,
    private slaService: SlaService
  ) {}

  async registerComplaint(userId: string, dto: CreateComplaintDto) {
    const slaDetails = this.slaService.calculateSla(dto.category);
    
    const complaint = await this.repository.createComplaint({
      userId,
      title: dto.title,
      description: dto.description,
      category: dto.category,
      priority: slaDetails.priority,
      bookingId: dto.bookingId,
    });

    // Fire Kafka event: complaint.created -> Triggers Notification Service
    return complaint;
  }

  async getComplaintForPassenger(id: string, userId: string) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');
    if (complaint.userId !== userId) throw new UnauthorizedException('Access denied');

    // Filter out internal comments before returning to passenger
    complaint.comments = complaint.comments.filter(c => !c.isInternal);
    return complaint;
  }

  async addComment(id: string, authorId: string, dto: ComplaintCommentDto) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');
    
    if (complaint.status === ComplaintStatus.CLOSED) {
      throw new BadRequestException('Cannot comment on a closed complaint');
    }

    return this.repository.addComment(id, authorId, dto.content, !!dto.isInternal);
  }

  async resolveComplaint(id: string) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');

    if (complaint.status === ComplaintStatus.CLOSED) {
      throw new BadRequestException('Complaint is already closed');
    }

    return this.repository.updateStatus(id, ComplaintStatus.RESOLVED);
  }
}
"""
with open(os.path.join(base_dir, "complaint/complaint.service.ts"), "w", encoding="utf-8") as f: f.write(complaint_svc)


# 4. Controllers
complaint_ctrl = """import { Controller, Post, Get, Body, Param, UseGuards, Request } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { CreateComplaintDto, ComplaintCommentDto } from './dto/complaint.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Passenger Complaints')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('complaints')
export class ComplaintController {
  constructor(private readonly complaintService: ComplaintService) {}

  @Post()
  @ApiOperation({ summary: 'Register a new grievance' })
  async register(@Request() req, @Body() dto: CreateComplaintDto) {
    return this.complaintService.registerComplaint(req.user.userId, dto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get details of a specific complaint (Passenger view)' })
  async getDetails(@Request() req, @Param('id') id: string) {
    return this.complaintService.getComplaintForPassenger(id, req.user.userId);
  }

  @Post(':id/comment')
  @ApiOperation({ summary: 'Add a comment to an open complaint' })
  async addComment(@Request() req, @Param('id') id: string, @Body() dto: ComplaintCommentDto) {
    // Force isInternal to false for passenger submissions
    dto.isInternal = false; 
    return this.complaintService.addComment(id, req.user.userId, dto);
  }
}
"""
with open(os.path.join(base_dir, "complaint/complaint.controller.ts"), "w", encoding="utf-8") as f: f.write(complaint_ctrl)


admin_ctrl = """import { Controller, Post, Param, Body, UseGuards, Request } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { EscalationService } from './escalation.service';
import { ComplaintCommentDto } from './dto/complaint.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Admin Complaint Management')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/complaints')
export class AdminController {
  constructor(
    private readonly complaintService: ComplaintService,
    private readonly escalationService: EscalationService
  ) {}

  @Post(':id/resolve')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Mark a complaint as resolved (Staff only)' })
  async resolve(@Param('id') id: string) {
    return this.complaintService.resolveComplaint(id);
  }

  @Post(':id/escalate')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Manually escalate a complaint (Staff only)' })
  async escalate(@Param('id') id: string) {
    return this.escalationService.escalateComplaint(id);
  }

  @Post(':id/comment')
  @Roles('Depot_Manager', 'HQ_Admin')
  @ApiOperation({ summary: 'Add an internal staff comment' })
  async addInternalComment(@Request() req, @Param('id') id: string, @Body() dto: ComplaintCommentDto) {
    return this.complaintService.addComment(id, req.user.userId, dto);
  }
}
"""
with open(os.path.join(base_dir, "complaint/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
complaint_mod = """import { Module } from '@nestjs/common';
import { ComplaintController } from './complaint.controller';
import { AdminController } from './admin.controller';
import { ComplaintService } from './complaint.service';
import { SlaService } from './sla.service';
import { EscalationService } from './escalation.service';
import { ComplaintRepository } from './repository/complaint.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [ComplaintController, AdminController],
  providers: [ComplaintService, SlaService, EscalationService, ComplaintRepository],
})
export class ComplaintModule {}
"""
with open(os.path.join(base_dir, "complaint/complaint.module.ts"), "w", encoding="utf-8") as f: f.write(complaint_mod)

app_module = """import { Module } from '@nestjs/common';
import { ComplaintModule } from './complaint/complaint.module';

@Module({
  imports: [ComplaintModule],
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
    .setTitle('MSRTC Complaint & SLA Service')
    .setDescription('Grievance lifecycle management and SLA tracking')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/complaint', app, document);

  await app.listen(3011);
  console.log('Complaint Service is running on http://localhost:3011');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Complaint Service Phase 2 Scaffolded (State Machine, SLA, Admin Controllers)")
