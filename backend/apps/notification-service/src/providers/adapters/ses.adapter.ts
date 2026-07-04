import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class SesAdapter implements INotificationProvider {
  async send(to: string, content: string, subject: string): Promise<boolean> {
    console.log(`[SES] Sending Email to ${to} | Sub: ${subject}`);
    return true; // Mock success
  }
}
