import { Injectable } from '@nestjs/common';
import { authenticator } from 'otplib';
import * as qrcode from 'qrcode';

@Injectable()
export class MfaService {
  async generateMfaSecret(email: string) {
    const secret = authenticator.generateSecret();
    const otpauthUrl = authenticator.keyuri(email, 'MSRTC Enterprise', secret);
    const qrCodeDataUrl = await qrcode.toDataURL(otpauthUrl);
    
    return { secret, qrCodeDataUrl };
  }

  verifyMfaToken(token: string, secret: string): boolean {
    return authenticator.verify({ token, secret });
  }
}
