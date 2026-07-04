import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { TicketRepository } from './repository/ticket.repository';
import { QrService } from './qr.service';
import { ValidateTicketDto } from './dto/ticket.dto';
import { TicketStatus } from './enums/ticket.enums';

@Injectable()
export class ValidatorService {
  constructor(
    private readonly repository: TicketRepository,
    private readonly qrService: QrService
  ) {}

  async validateScannedQr(dto: ValidateTicketDto) {
    // 1. Decode and verify signature/checksum
    const decodedPayload = this.qrService.verifyPayload(dto.qrPayload);
    if (!decodedPayload) {
      throw new BadRequestException('Invalid or forged QR Code');
    }

    // 2. Fetch Ticket
    const ticket = await this.repository.findTicketById(decodedPayload.ticketId);
    if (!ticket) {
      throw new NotFoundException('Ticket record not found in database');
    }

    // 3. State Machine Checks
    if (ticket.status === TicketStatus.CANCELLED || ticket.status === TicketStatus.ARCHIVED) {
      throw new BadRequestException(`Ticket is ${ticket.status}`);
    }

    // If valid, mark as USED
    await this.repository.updateTicketStatus(ticket.id, TicketStatus.USED);

    return {
      valid: true,
      ticket: {
        id: ticket.id,
        pnr: ticket.pnr,
        status: 'USED'
      }
    };
  }
}
