import { Controller, Post, Get, Body, Param, UseGuards } from '@nestjs/common';
import { GpsService } from './gps.service';
import { GpsPingDto } from './dto/gps.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('GPS Ingestion')
@Controller('gps')
export class GpsController {
  constructor(private readonly gpsService: GpsService) {}

  @Post('ping')
  @ApiOperation({ summary: 'Receive GPS ping from vehicle IoT device or conductor app' })
  async receivePing(@Body() dto: GpsPingDto) {
    return this.gpsService.processPing(dto);
  }

  @Get('vehicle/:id/current')
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  @ApiOperation({ summary: 'Get the last known location of a vehicle (reads from Redis)' })
  async getCurrentLocation(@Param('id') vehicleId: string) {
    return this.gpsService.getLastKnownLocation(vehicleId);
  }
}
