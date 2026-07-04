import { Injectable } from '@nestjs/common';

@Injectable()
export class RouteService {
  getHello(): string {
    return 'Hello from Route Service!';
  }
}
