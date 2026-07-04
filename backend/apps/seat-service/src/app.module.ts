import { Module } from '@nestjs/common';
import { SeatModule } from './seat/seat.module';

@Module({
  imports: [SeatModule],
})
export class AppModule {}
