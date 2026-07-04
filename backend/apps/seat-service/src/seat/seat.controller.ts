import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { SeatService } from './seat.service';
import { LockSeatDto } from './dto/lock-seat.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Seats')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('seats')
export class SeatController {
  constructor(private readonly seatService: SeatService) {}

  @Post('lock')
  @ApiOperation({ summary: 'Lock seats temporarily in Redis for a booking session' })
  async lockSeats(@Request() req, @Body() dto: LockSeatDto) {
    return this.seatService.lockSeats(req.user.userId, dto);
  }

  @Post('release')
  @ApiOperation({ summary: 'Manually release held seats' })
  async releaseSeats(@Request() req, @Body() dto: LockSeatDto) {
    return this.seatService.releaseSeats(req.user.userId, dto);
  }
}
