import { Injectable } from '@nestjs/common';

@Injectable()
export class PassService {
  getHello(): string {
    return 'Hello from Pass Service!';
  }
}
