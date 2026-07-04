import { Injectable } from '@nestjs/common';
import * as QRCode from 'qrcode';

@Injectable()
export class QrService {
  /**
   * Generates a base64 Data URI for a given payload.
   * In a real implementation, the payload includes a checksum to prevent forgery.
   */
  async generateQrCode(payload: any): Promise<string> {
    const stringified = JSON.stringify(payload);
    // Return Base64 encoded image
    return QRCode.toDataURL(stringified);
  }

  /**
   * Decodes and verifies a QR payload (e.g., checksum validation).
   */
  verifyPayload(payloadStr: string): any {
    try {
      const payload = JSON.parse(payloadStr);
      // Mock Checksum verification
      if (!payload.checksum) throw new Error('Invalid checksum');
      return payload;
    } catch (e) {
      return null;
    }
  }
}
