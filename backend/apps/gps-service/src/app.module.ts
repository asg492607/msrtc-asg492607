import { Module } from '@nestjs/common';
import { GpsModule } from './gps/gps.module';

@Module({
  imports: [GpsModule],
})
export class AppModule {}
