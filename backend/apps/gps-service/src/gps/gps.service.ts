import { Injectable } from '@nestjs/common';

@Injectable()
export class GpsService {
  getHello(): string {
    return 'Hello from Gps Service!';
  }
}
