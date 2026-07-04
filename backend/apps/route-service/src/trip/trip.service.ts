import { Injectable, BadRequestException } from '@nestjs/common';
import { TripRepository } from './repository/trip.repository';
import { SearchTripsDto } from './dto/search-trips.dto';

@Injectable()
export class TripService {
  constructor(private readonly repository: TripRepository) {}

  /**
   * Executes the search engine logic.
   */
  async searchAvailableTrips(dto: SearchTripsDto) {
    const travelDate = new Date(dto.travelDate);
    if (travelDate < new Date(new Date().setHours(0,0,0,0))) {
      throw new BadRequestException('Travel date cannot be in the past');
    }

    if (dto.sourceStationId === dto.destinationStationId) {
      throw new BadRequestException('Source and destination cannot be the same');
    }

    const trips = await this.repository.searchTrips(dto);
    
    return {
      message: 'Trips found successfully',
      date: dto.travelDate,
      count: trips.length,
      trips
    };
  }
}
