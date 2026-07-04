import { Module } from '@nestjs/common';
import { ComplaintModule } from './complaint/complaint.module';

@Module({
  imports: [ComplaintModule],
})
export class AppModule {}
