import { Injectable } from '@nestjs/common';
import { DepotRepository } from './repository/depot.repository';
import { CreateDepotDto, AddBusDto } from './dto/depot.dto';

@Injectable()
export class InventoryService {
  constructor(private repository: DepotRepository) {}

  async createDepot(dto: CreateDepotDto) {
    return this.repository.createDepot(dto);
  }

  async addBusToDepot(dto: AddBusDto) {
    return this.repository.addBus(dto);
  }
}
