import { Module } from '@nestjs/common';
import { DepotModule } from './depot/depot.module';

@Module({
  imports: [DepotModule],
})
export class AppModule {}
