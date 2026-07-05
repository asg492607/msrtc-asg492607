import { Module } from '@nestjs/common';
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
