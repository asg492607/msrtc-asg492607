import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { BookingStatus } from '../../common/enums/booking.enums';

@Injectable()
export class BookingRepository {
  constructor(private prisma: PrismaService) {}

  async createPendingBooking(userId: string, tripId: string, passengers: any[], totalFare: number) {
    // We use an interactive transaction to ensure atomicity
    return this.prisma.$transaction(async (tx) => {
      // 1. Create the booking record
      const booking = await tx.booking.create({
        data: {
          pnr: `PNR${Date.now()}${Math.floor(Math.random() * 1000)}`,
          userId,
          tripInstanceId: tripId,
          status: BookingStatus.PENDING,
          totalFare,
          netAmount: totalFare,
        },
      });

      // 2. Create passenger records
      const passengerData = passengers.map(p => ({
        bookingId: booking.id,
        name: p.name,
        age: p.age,
        gender: p.gender,
        seatNo: p.seatNo,
        status: 'CONFIRMED',
        fare: totalFare / passengers.length // Mock fare split
      }));

      await tx.bookingPassenger.createMany({
        data: passengerData,
      });

      // 3. Create Audit Log
      await tx.bookingLog.create({
        data: {
          bookingId: booking.id,
          action: 'BOOKING_INITIATED',
        }
      });

      return booking;
    });
  }
  
  async findBookingById(id: string) {
    return this.prisma.booking.findUnique({
      where: { id },
      include: { passengers: true }
    });
  }

  async updateBookingStatus(id: string, status: BookingStatus) {
    return this.prisma.booking.update({
      where: { id },
      data: { status }
    });
  }
}
