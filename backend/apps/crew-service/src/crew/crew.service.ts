import { Injectable } from '@nestjs/common';

@Injectable()
export class CrewService {
  getHello(): string {
    return 'Hello from Crew Service!';
  }
}
