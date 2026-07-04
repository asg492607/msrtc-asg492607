import { Module } from '@nestjs/common';
import { TripModule } from './trip/trip.module';

@Module({
  imports: [TripModule],
})
export class AppModule {}
