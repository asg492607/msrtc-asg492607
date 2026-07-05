import { Injectable, NotFoundException } from '@nestjs/common';
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
