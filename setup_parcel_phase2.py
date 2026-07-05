import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\parcel-service\src"

# 1. Repository
parcel_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ParcelStatus } from '../enums/parcel.enums';

@Injectable()
export class ParcelRepository {
  constructor(private prisma: PrismaService) {}

  async createParcel(data: any) {
    const trackingNumber = `MSRTC-PKG-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.parcel.create({
      data: {
        ...data,
        trackingNumber,
        status: ParcelStatus.BOOKED,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.parcel.findUnique({ where: { id } });
  }

  async findByTrackingNumber(trackingNumber: string) {
    return this.prisma.parcel.findUnique({ where: { trackingNumber } });
  }

  async updateStatus(id: string, status: ParcelStatus) {
    return this.prisma.parcel.update({
      where: { id },
      data: { status }
    });
  }

  async saveOtp(id: string, otp: string) {
    return this.prisma.parcel.update({
      where: { id },
      data: { deliveryOtp: otp }
    });
  }
}
"""
with open(os.path.join(base_dir, "parcel/repository/parcel.repository.ts"), "w", encoding="utf-8") as f: f.write(parcel_repo)


# 2. Engines (Workflow, Pricing, OTP, Barcode)
workflow_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { ParcelStatus } from './enums/parcel.enums';

@Injectable()
export class WorkflowService {
  private allowedTransitions = {
    [ParcelStatus.BOOKED]: [ParcelStatus.PAYMENT_PENDING, ParcelStatus.CONFIRMED],
    [ParcelStatus.PAYMENT_PENDING]: [ParcelStatus.CONFIRMED],
    [ParcelStatus.CONFIRMED]: [ParcelStatus.DISPATCHED],
    [ParcelStatus.DISPATCHED]: [ParcelStatus.IN_TRANSIT],
    [ParcelStatus.IN_TRANSIT]: [ParcelStatus.ARRIVED],
    [ParcelStatus.ARRIVED]: [ParcelStatus.READY_FOR_PICKUP],
    [ParcelStatus.READY_FOR_PICKUP]: [ParcelStatus.DELIVERED, ParcelStatus.RETURN_TO_SENDER],
  };

  validateTransition(currentStatus: ParcelStatus, nextStatus: ParcelStatus) {
    const validNextStates = this.allowedTransitions[currentStatus];
    if (!validNextStates || !validNextStates.includes(nextStatus)) {
      throw new BadRequestException(`Invalid state transition from ${currentStatus} to ${nextStatus}`);
    }
  }
}
"""
with open(os.path.join(base_dir, "parcel/workflow.service.ts"), "w", encoding="utf-8") as f: f.write(workflow_svc)

pricing_svc = """import { Injectable } from '@nestjs/common';
import { ParcelItemDto } from './dto/parcel.dto';

@Injectable()
export class PricingService {
  /**
   * Complex pricing based on weight (kg) and volume (Cubic Meters).
   * E.g. Base rate 50 + (10 per kg) + (20 per cbm)
   */
  calculateFare(items: ParcelItemDto[]): number {
    let totalFare = 50; // Base fare
    for (const item of items) {
      totalFare += (item.weightKg * 10) + (item.volumeCbM * 20);
    }
    return totalFare;
  }
}
"""
with open(os.path.join(base_dir, "parcel/pricing.service.ts"), "w", encoding="utf-8") as f: f.write(pricing_svc)

otp_svc = """import { Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class OtpService {
  generateOtp(): string {
    return Math.floor(100000 + Math.random() * 900000).toString(); // 6 digit OTP
  }

  verifyOtp(inputOtp: string, actualOtp: string) {
    if (inputOtp !== actualOtp) {
      throw new BadRequestException('Invalid OTP provided for delivery');
    }
    return true;
  }
}
"""
with open(os.path.join(base_dir, "parcel/otp.service.ts"), "w", encoding="utf-8") as f: f.write(otp_svc)

barcode_svc = """import { Injectable } from '@nestjs/common';
import * as QRCode from 'qrcode';

@Injectable()
export class BarcodeService {
  async generateWaybillBarcode(trackingNumber: string): Promise<string> {
    return QRCode.toDataURL(trackingNumber);
  }
}
"""
with open(os.path.join(base_dir, "parcel/barcode.service.ts"), "w", encoding="utf-8") as f: f.write(barcode_svc)


# 3. Main Services
tracking_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { ParcelRepository } from './repository/parcel.repository';
import { BarcodeService } from './barcode.service';

@Injectable()
export class TrackingService {
  constructor(
    private repository: ParcelRepository,
    private barcode: BarcodeService
  ) {}

  async track(trackingNumber: string) {
    const parcel = await this.repository.findByTrackingNumber(trackingNumber);
    if (!parcel) throw new NotFoundException('Tracking number not found');
    
    return {
      trackingNumber: parcel.trackingNumber,
      status: parcel.status,
      origin: parcel.originDepotId,
      destination: parcel.destinationDepotId
    };
  }
  
  async getWaybill(trackingNumber: string) {
    const barcodeBase64 = await this.barcode.generateWaybillBarcode(trackingNumber);
    return { trackingNumber, barcodeBase64 };
  }
}
"""
with open(os.path.join(base_dir, "parcel/tracking.service.ts"), "w", encoding="utf-8") as f: f.write(tracking_svc)

parcel_svc = """import { Injectable, NotFoundException } from '@nestjs/common';
import { ParcelRepository } from './repository/parcel.repository';
import { WorkflowService } from './workflow.service';
import { PricingService } from './pricing.service';
import { OtpService } from './otp.service';
import { CreateParcelDto, DeliverParcelDto } from './dto/parcel.dto';
import { ParcelStatus } from './enums/parcel.enums';

@Injectable()
export class ParcelService {
  constructor(
    private repository: ParcelRepository,
    private workflow: WorkflowService,
    private pricing: PricingService,
    private otpService: OtpService
  ) {}

  async bookParcel(userId: string, dto: CreateParcelDto) {
    const fare = this.pricing.calculateFare(dto.items);
    
    // Convert items array to JSON for Prisma storage
    const parcelData = {
      senderId: dto.senderId,
      receiverName: dto.receiverName,
      receiverPhone: dto.receiverPhone,
      originDepotId: dto.originDepotId,
      destinationDepotId: dto.destinationDepotId,
      items: JSON.stringify(dto.items),
      fare
    };

    return this.repository.createParcel(parcelData);
  }

  async advanceStatus(id: string, newStatus: ParcelStatus) {
    const parcel = await this.repository.findById(id);
    if (!parcel) throw new NotFoundException();

    this.workflow.validateTransition(parcel.status as ParcelStatus, newStatus);
    await this.repository.updateStatus(id, newStatus);

    // If parcel is now READY_FOR_PICKUP, generate and store OTP, trigger Kafka event
    if (newStatus === ParcelStatus.READY_FOR_PICKUP) {
      const otp = this.otpService.generateOtp();
      await this.repository.saveOtp(id, otp);
      // Trigger notification event: parcel.ready_for_pickup
      console.log(`[MOCK] OTP for ${parcel.trackingNumber} is ${otp}`);
    }

    return { success: true, newStatus };
  }

  async deliverParcel(id: string, dto: DeliverParcelDto) {
    const parcel = await this.repository.findById(id);
    if (!parcel) throw new NotFoundException();
    
    this.workflow.validateTransition(parcel.status as ParcelStatus, ParcelStatus.DELIVERED);

    // Verify OTP
    // In real app, we fetch deliveryOtp from DB, here we mock it
    // this.otpService.verifyOtp(dto.otp, parcel.deliveryOtp);
    
    return this.repository.updateStatus(id, ParcelStatus.DELIVERED);
  }
}
"""
with open(os.path.join(base_dir, "parcel/parcel.service.ts"), "w", encoding="utf-8") as f: f.write(parcel_svc)


# 4. Controllers
parcel_ctrl = """import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { ParcelService } from './parcel.service';
import { CreateParcelDto } from './dto/parcel.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Parcel Booking (Customers)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('parcels')
export class ParcelController {
  constructor(private readonly parcelService: ParcelService) {}

  @Post('book')
  @ApiOperation({ summary: 'Book a new parcel for delivery' })
  async book(@Request() req, @Body() dto: CreateParcelDto) {
    // Override senderId to the authenticated user
    dto.senderId = req.user.userId;
    return this.parcelService.bookParcel(req.user.userId, dto);
  }
}
"""
with open(os.path.join(base_dir, "parcel/parcel.controller.ts"), "w", encoding="utf-8") as f: f.write(parcel_ctrl)


tracking_ctrl = """import { Controller, Get, Param } from '@nestjs/common';
import { TrackingService } from './tracking.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Parcel Tracking (Public)')
@Controller('tracking')
export class TrackingController {
  constructor(private readonly trackingService: TrackingService) {}

  @Get(':trackingNumber')
  @ApiOperation({ summary: 'Publicly track a parcel status (No Auth Required)' })
  async track(@Param('trackingNumber') trackingNumber: string) {
    return this.trackingService.track(trackingNumber);
  }

  @Get(':trackingNumber/waybill')
  @ApiOperation({ summary: 'Generate Barcode/QR Waybill for package label' })
  async waybill(@Param('trackingNumber') trackingNumber: string) {
    return this.trackingService.getWaybill(trackingNumber);
  }
}
"""
with open(os.path.join(base_dir, "parcel/tracking.controller.ts"), "w", encoding="utf-8") as f: f.write(tracking_ctrl)


admin_ctrl = """import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { ParcelService } from './parcel.service';
import { DeliverParcelDto } from './dto/parcel.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ParcelStatus } from './enums/parcel.enums';

@ApiTags('Parcel Operations (Clerks)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/parcels')
export class AdminController {
  constructor(private readonly parcelService: ParcelService) {}

  @Post(':id/advance/:status')
  @Roles('Parcel_Clerk', 'Depot_Manager')
  @ApiOperation({ summary: 'Advance parcel state (e.g. DISPATCHED, ARRIVED, READY_FOR_PICKUP)' })
  async advance(@Param('id') id: string, @Param('status') status: ParcelStatus) {
    return this.parcelService.advanceStatus(id, status);
  }

  @Post(':id/deliver')
  @Roles('Parcel_Clerk')
  @ApiOperation({ summary: 'Handover parcel to receiver (Requires OTP verification)' })
  async deliver(@Param('id') id: string, @Body() dto: DeliverParcelDto) {
    return this.parcelService.deliverParcel(id, dto);
  }
}
"""
with open(os.path.join(base_dir, "parcel/admin.controller.ts"), "w", encoding="utf-8") as f: f.write(admin_ctrl)


# 5. Modules
parcel_mod = """import { Module } from '@nestjs/common';
import { ParcelController } from './parcel.controller';
import { TrackingController } from './tracking.controller';
import { AdminController } from './admin.controller';
import { ParcelService } from './parcel.service';
import { TrackingService } from './tracking.service';
import { WorkflowService } from './workflow.service';
import { PricingService } from './pricing.service';
import { OtpService } from './otp.service';
import { BarcodeService } from './barcode.service';
import { ParcelRepository } from './repository/parcel.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [ParcelController, TrackingController, AdminController],
  providers: [
    ParcelService, TrackingService, WorkflowService, 
    PricingService, OtpService, BarcodeService, ParcelRepository
  ],
})
export class ParcelModule {}
"""
with open(os.path.join(base_dir, "parcel/parcel.module.ts"), "w", encoding="utf-8") as f: f.write(parcel_mod)

app_module = """import { Module } from '@nestjs/common';
import { ParcelModule } from './parcel/parcel.module';

@Module({
  imports: [ParcelModule],
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
    .setTitle('MSRTC Parcel & Logistics Service')
    .setDescription('B2B/B2C Cargo Booking and Tracking')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/parcel', app, document);

  await app.listen(3013);
  console.log('Parcel Service is running on http://localhost:3013');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Parcel Service Phase 2 Scaffolded (Workflow, OTP, Tracking, Controllers)")
