import { Injectable } from '@nestjs/common';

@Injectable()
export class MasterDataService {
  getHello(): string {
    return 'Hello from MasterData Service!';
  }
}
