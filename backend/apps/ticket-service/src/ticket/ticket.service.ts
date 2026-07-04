import { Injectable, BadRequestException } from '@nestjs/common';
import { TicketRepository } from './repository/ticket.repository';
import { QrService } from './qr.service';
import { PdfService } from './pdf.service';
import { GenerateTicketDto } from './dto/ticket.dto';

@Injectable()
export class TicketService {
  constructor(
    private readonly repository: TicketRepository,
    private readonly qrService: QrService,
    private readonly pdfService: PdfService
  ) {}

  async generateTicket(dto: GenerateTicketDto) {
    // In real app, query Booking Service to ensure it is CONFIRMED and PAYMENT_SUCCESS
    const isBookingConfirmed = true; 
    if (!isBookingConfirmed) {
      throw new BadRequestException('Cannot generate ticket for unconfirmed booking');
    }

    const ticketNumber = `TKT-${Date.now()}`;
    const pnr = `PNR-${Math.random().toString(36).substring(7).toUpperCase()}`;

    // Generate QR
    const qrPayloadObj = {
      ticketId: ticketNumber, // Mock mapping
      bookingId: dto.bookingId,
      pnr: pnr,
      checksum: 'valid-hash'
    };
    const qrCodeBase64 = await this.qrService.generateQrCode(qrPayloadObj);

    // Generate PDF
    const pdfUrl = await this.pdfService.generateTicketPdf({ ticketNumber, pnr, qr: qrCodeBase64 });

    // Persist
    const ticket = await this.repository.createTicket(dto.bookingId, ticketNumber, pnr, JSON.stringify(qrPayloadObj), pdfUrl);

    // Kafka event emission would happen here

    return ticket;
  }
}
