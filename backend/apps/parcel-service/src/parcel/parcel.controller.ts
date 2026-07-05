import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
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
