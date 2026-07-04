import { Injectable } from '@nestjs/common';
import { INotificationProvider } from '../interfaces/provider.interface';

@Injectable()
export class Msg91Adapter implements INotificationProvider {
  async send(to: string, content: string): Promise<boolean> {
    console.log(`[MSG91] Sending SMS to ${to}: ${content}`);
    return true; // Mock success
  }
}
