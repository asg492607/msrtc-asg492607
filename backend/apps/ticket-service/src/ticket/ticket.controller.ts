import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { TicketService } from './ticket.service';
import { GenerateTicketDto } from './dto/ticket.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Tickets')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('tickets')
export class TicketController {
  constructor(private readonly ticketService: TicketService) {}

  @Post('generate')
  @ApiOperation({ summary: 'Generate a new QR/PDF ticket for a confirmed booking' })
  async generateTicket(@Body() dto: GenerateTicketDto) {
    return this.ticketService.generateTicket(dto);
  }
}
