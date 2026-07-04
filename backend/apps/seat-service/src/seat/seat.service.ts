import { Injectable } from '@nestjs/common';

@Injectable()
export class SeatService {
  getHello(): string {
    return 'Hello from Seat Service!';
  }
}
