import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\booking-service\src"

# 1. Guards
jwt_guard = """import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

// Simple mocked guard for the reference architecture.
// In a real microservice mesh, this would validate the token against the auth-service or verify the signature locally.
@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    // Mock user injection
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Passenger'] };
    return true;
  }
}
"""
with open(os.path.join(base_dir, "common/guards/jwt-auth.guard.ts"), "w") as f: f.write(jwt_guard)

# 2. Service
booking_svc = """import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
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
"""
with open(os.path.join(base_dir, "booking/booking.service.ts"), "w") as f: f.write(booking_svc)

# 3. Controller
booking_ctrl = """import { Controller, Post, Get, Param, Body, UseGuards, Request, Delete } from '@nestjs/common';
import { BookingService } from './booking.service';
import { CreateBookingDto } from './dto/create-booking.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Bookings')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller()
export class BookingController {
  constructor(private readonly bookingService: BookingService) {}

  @Post()
  @ApiOperation({ summary: 'Initiate a new booking reservation' })
  async createBooking(@Request() req, @Body() dto: CreateBookingDto) {
    return this.bookingService.createBooking(req.user.userId, dto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get booking details by ID' })
  async getBooking(@Request() req, @Param('id') id: string) {
    return this.bookingService.getBooking(id, req.user.userId);
  }

  @Delete(':id/cancel')
  @ApiOperation({ summary: 'Cancel an existing booking' })
  async cancelBooking(@Request() req, @Param('id') id: string) {
    return this.bookingService.cancelBooking(id, req.user.userId);
  }
}
"""
with open(os.path.join(base_dir, "booking/booking.controller.ts"), "w") as f: f.write(booking_ctrl)

# 4. Module
booking_mod = """import { Module } from '@nestjs/common';
import { BookingController } from './booking.controller';
import { BookingService } from './booking.service';
import { BookingRepository } from './repository/booking.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [BookingController],
  providers: [BookingService, BookingRepository],
})
export class BookingModule {}
"""
with open(os.path.join(base_dir, "booking/booking.module.ts"), "w") as f: f.write(booking_mod)

print("Booking Service Phase 2 Scaffolded (Service, Controller, Module, Guard)")
