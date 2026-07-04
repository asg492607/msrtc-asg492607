import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class FirebaseAdapter implements INotificationProvider {
  async send(to: string, content: string, subject: string): Promise<boolean> {
    console.log(`[Firebase] Sending Push to token ${to} | Title: ${subject}`);
    return true; // Mock success
  }
}
