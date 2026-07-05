import { Module } from '@nestjs/common';
import { ComplaintController } from './complaint.controller';
import { AdminController } from './admin.controller';
import { ComplaintService } from './complaint.service';
import { SlaService } from './sla.service';
import { EscalationService } from './escalation.service';
import { ComplaintRepository } from './repository/complaint.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [ComplaintController, AdminController],
  providers: [ComplaintService, SlaService, EscalationService, ComplaintRepository],
})
export class ComplaintModule {}
