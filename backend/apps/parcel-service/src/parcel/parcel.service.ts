import { Injectable } from '@nestjs/common';

@Injectable()
export class ParcelService {
  getHello(): string {
    return 'Hello from Parcel Service!';
  }
}
