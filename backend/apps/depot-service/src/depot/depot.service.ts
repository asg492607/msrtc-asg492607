import { Injectable } from '@nestjs/common';

@Injectable()
export class DepotService {
  getHello(): string {
    return 'Hello from Depot Service!';
  }
}
