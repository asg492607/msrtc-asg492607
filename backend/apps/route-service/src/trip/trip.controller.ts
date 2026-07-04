import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { TripService } from './trip.service';
import { SearchTripsDto } from './dto/search-trips.dto';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('Trips (Search Engine)')
@Controller('trips')
export class TripController {
  constructor(private readonly tripService: TripService) {}

  @Get('search')
  @ApiOperation({ summary: 'Search for available buses between two stations on a given date' })
  @ApiResponse({ status: 200, description: 'List of available trips with fares and timings.' })
  async searchTrips(@Query() dto: SearchTripsDto) {
    return this.tripService.searchAvailableTrips(dto);
  }
}
