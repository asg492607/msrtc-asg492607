import { Module } from '@nestjs/common';
import { PassController } from './pass.controller';
import { AdminController } from './admin.controller';
import { ValidationController } from './validation.controller';
import { PassService } from './pass.service';
import { WorkflowService } from './workflow.service';
import { ConcessionService } from './concession.service';
import { QrService } from './qr.service';
import { PassRepository } from './repository/pass.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [PassController, AdminController, ValidationController],
  providers: [PassService, WorkflowService, ConcessionService, QrService, PassRepository],
})
export class PassModule {}
