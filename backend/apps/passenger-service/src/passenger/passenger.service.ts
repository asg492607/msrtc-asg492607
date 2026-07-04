import { Injectable } from '@nestjs/common';

@Injectable()
export class PassengerService {
  getHello(): string {
    return 'Hello from Passenger Service!';
  }
}
