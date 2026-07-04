import { Injectable } from '@nestjs/common';

@Injectable()
export class ComplaintService {
  getHello(): string {
    return 'Hello from Complaint Service!';
  }
}
