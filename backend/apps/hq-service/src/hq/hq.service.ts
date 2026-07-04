import { Injectable } from '@nestjs/common';

@Injectable()
export class HqService {
  getHello(): string {
    return 'Hello from Hq Service!';
  }
}
