import { Injectable } from '@nestjs/common';

@Injectable()
export class FleetService {
  getHello(): string {
    return 'Hello from Fleet Service!';
  }
}
