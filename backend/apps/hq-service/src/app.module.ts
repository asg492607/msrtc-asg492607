import { Module } from '@nestjs/common';
import { HqModule } from './hq/hq.module';

@Module({
  imports: [HqModule],
})
export class AppModule {}
