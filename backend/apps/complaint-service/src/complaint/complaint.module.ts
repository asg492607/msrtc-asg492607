import { Module } from '@nestjs/common';
import { ComplaintService } from './complaint.service';
import { ComplaintController } from './complaint.controller';

@Module({
  controllers: [ComplaintController],
  providers: [ComplaintService],
})
export class ComplaintModule {}
