import { Controller, Post, Get, Param, Body, UseGuards, Request, Delete } from '@nestjs/common';
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
