import { Injectable } from '@nestjs/common';
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
