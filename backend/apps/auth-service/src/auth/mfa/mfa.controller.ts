import { Controller, Post, Body, UseGuards, Request } from '@nestjs/common';
import { MfaService } from './mfa.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('IAM MFA')
@Controller('iam/mfa')
export class MfaController {
  constructor(private mfaService: MfaService) {}

  @Post('setup')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Setup TOTP MFA for user' })
  async setupMfa(@Request() req) {
    // req.user contains userId and email from JWT
    const email = req.user.email || 'user@msrtc.gov.in'; 
    return this.mfaService.generateMfaSecret(email);
  }

  @Post('verify')
  @ApiOperation({ summary: 'Verify TOTP code' })
  async verifyMfa(@Body('token') token: string, @Body('secret') secret: string) {
    const isValid = this.mfaService.verifyMfaToken(token, secret);
    return { valid: isValid };
  }
}
