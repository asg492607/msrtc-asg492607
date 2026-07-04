import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { BookingRepository } from './repository/booking.repository';
import { CreateBookingDto } from './dto/create-booking.dto';
import { BookingStatus } from '../common/enums/booking.enums';

@Injectable()
export class BookingService {
  constructor(private readonly repository: BookingRepository) {}

  async createBooking(userId: string, dto: CreateBookingDto) {
    if (!dto.passengers || dto.passengers.length === 0) {
      throw new BadRequestException('At least one passenger is required');
    }

    // 1. Validate Seat Availability (Mocked for now, will connect to seat-service via Redis)
    const seatsAvailable = true;
    if (!seatsAvailable) {
      throw new BadRequestException('Selected seats are no longer available');
    }

    // 2. Calculate Fare (Mocked)
    const baseFare = 500;
    const totalFare = baseFare * dto.passengers.length;

    // 3. Create Booking via Transaction
    const booking = await this.repository.createPendingBooking(userId, dto.tripInstanceId, dto.passengers, totalFare);

    return {
      message: 'Booking initiated successfully. Please proceed to payment.',
      bookingId: booking.id,
      pnr: booking.pnr,
      totalFare: booking.totalFare,
      status: booking.status
    };
  }

  async getBooking(bookingId: string, userId: string) {
    const booking = await this.repository.findBookingById(bookingId);
    if (!booking) {
      throw new NotFoundException('Booking not found');
    }
    
    // Authorization check
    if (booking.userId !== userId) {
      throw new BadRequestException('You do not have permission to view this booking');
    }

    return booking;
  }

  async cancelBooking(bookingId: string, userId: string) {
    const booking = await this.getBooking(bookingId, userId);
    
    if (booking.status === BookingStatus.CANCELLED) {
      throw new BadRequestException('Booking is already cancelled');
    }
    if (booking.status === BookingStatus.COMPLETED) {
      throw new BadRequestException('Cannot cancel a completed trip');
    }

    // Transition state
    return this.repository.updateBookingStatus(bookingId, BookingStatus.CANCELLED);
  }
}
