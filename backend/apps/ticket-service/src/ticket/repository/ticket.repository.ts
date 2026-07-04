import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { TicketStatus } from '../enums/ticket.enums';

@Injectable()
export class TicketRepository {
  constructor(private prisma: PrismaService) {}

  async createTicket(bookingId: string, ticketNumber: string, pnr: string, qrPayload: string, pdfUrl: string) {
    return this.prisma.ticket.create({
      data: {
        bookingId,
        ticketNumber,
        pnr,
        status: TicketStatus.GENERATED,
        qrPayload,
        pdfUrl,
      }
    });
  }

  async findTicketById(id: string) {
    return this.prisma.ticket.findUnique({ where: { id } });
  }

  async updateTicketStatus(id: string, status: TicketStatus) {
    return this.prisma.ticket.update({
      where: { id },
      data: { status }
    });
  }
}
