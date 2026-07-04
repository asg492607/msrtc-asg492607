import { Module } from '@nestjs/common';
import { TicketController } from './ticket.controller';
import { ValidationController } from './validation.controller';
import { TicketService } from './ticket.service';
import { ValidatorService } from './validator.service';
import { QrService } from './qr.service';
import { PdfService } from './pdf.service';
import { TicketRepository } from './repository/ticket.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [TicketController, ValidationController],
  providers: [TicketService, ValidatorService, QrService, PdfService, TicketRepository],
})
export class TicketModule {}
