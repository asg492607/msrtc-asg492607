import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ValidatorService } from './validator.service';
import { ValidateTicketDto } from './dto/ticket.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Validation (Conductors)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('validation')
export class ValidationController {
  constructor(private readonly validatorService: ValidatorService) {}

  @Post('scan')
  @Roles('Conductor', 'Inspector')
  @ApiOperation({ summary: 'Scan and validate a ticket QR code (Conductors Only)' })
  async scanQrCode(@Body() dto: ValidateTicketDto) {
    return this.validatorService.validateScannedQr(dto);
  }
}
