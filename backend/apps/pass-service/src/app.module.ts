import { Module } from '@nestjs/common';
import { PassModule } from './pass/pass.module';

@Module({
  imports: [PassModule],
})
export class AppModule {}
