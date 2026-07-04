import { Controller, Get } from '@nestjs/common';
import { TicketService } from './ticket.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Ticket')
@Controller()
export class TicketController {
  constructor(private readonly service: TicketService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
