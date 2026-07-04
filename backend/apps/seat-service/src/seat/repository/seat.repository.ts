import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class SeatRepository {
  constructor(private prisma: PrismaService) {}

  /**
   * Checks if a seat is permanently booked in PostgreSQL.
   */
  async isSeatPermanentlyBooked(tripId: string, seatNo: string): Promise<boolean> {
    const bookingPassenger = await this.prisma.bookingPassenger.findFirst({
      where: {
        seatNo: seatNo,
        booking: {
          tripInstanceId: tripId,
          status: { in: ['CONFIRMED', 'COMPLETED'] }
        }
      }
    });
    return !!bookingPassenger;
  }
}
