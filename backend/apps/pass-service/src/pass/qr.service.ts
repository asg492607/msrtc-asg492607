import { Injectable } from '@nestjs/common';
import * as QRCode from 'qrcode';

@Injectable()
export class QrService {
  async generatePassQr(passId: string, passNumber: string, validUntil: Date): Promise<string> {
    const payload = JSON.stringify({
      passId,
      passNumber,
      validUntil: validUntil.toISOString(),
      checksum: 'secure-hash-placeholder'
    });
    return QRCode.toDataURL(payload);
  }

  verifyPayload(payloadStr: string): any {
    try {
      const payload = JSON.parse(payloadStr);
      if (!payload.checksum) throw new Error('Invalid checksum');
      return payload;
    } catch (e) {
      return null;
    }
  }
}
