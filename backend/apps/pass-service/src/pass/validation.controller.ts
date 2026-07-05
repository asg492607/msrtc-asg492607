import { Controller, Post, Body, UseGuards, BadRequestException } from '@nestjs/common';
import { QrService } from './qr.service';
import { ValidatePassDto } from './dto/pass.dto';
import { PassRepository } from './repository/pass.repository';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { PassStatus } from './enums/pass.enums';

@ApiTags('Validation (Conductors)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('validation/passes')
export class ValidationController {
  constructor(
    private qrService: QrService,
    private repository: PassRepository
  ) {}

  @Post('scan')
  @Roles('Conductor', 'Inspector')
  @ApiOperation({ summary: 'Scan and validate a digital Pass QR (Conductors Only)' })
  async scanPass(@Body() dto: ValidatePassDto) {
    const decoded = this.qrService.verifyPayload(dto.qrPayload);
    if (!decoded) throw new BadRequestException('Invalid QR Payload');

    const pass = await this.repository.findById(decoded.passId);
    if (!pass) throw new BadRequestException('Pass not found');

    if (pass.status !== PassStatus.ACTIVE) {
      throw new BadRequestException(`Pass is currently ${pass.status}`);
    }

    if (new Date() > pass.validUntil) {
      throw new BadRequestException('Pass has expired');
    }

    return { valid: true, pass: { passNumber: pass.passNumber, validUntil: pass.validUntil } };
  }
}
