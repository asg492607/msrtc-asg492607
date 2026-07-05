import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { VehicleStatus } from '../enums/depot.enums';

@Injectable()
export class DepotRepository {
  constructor(private prisma: PrismaService) {}

  async createDepot(data: any) {
    return this.prisma.depot.create({ data });
  }

  async addBus(data: any) {
    return this.prisma.vehicleInventory.create({
      data: {
        ...data,
        status: VehicleStatus.AVAILABLE
      }
    });
  }

  async findBusById(id: string) {
    return this.prisma.vehicleInventory.findUnique({ where: { id } });
  }

  async updateBusStatus(id: string, status: VehicleStatus) {
    return this.prisma.vehicleInventory.update({
      where: { id },
      data: { status }
    });
  }

  async logDispatch(busId: string, tripInstanceId: string) {
    return this.prisma.dispatchLog.create({
      data: { busId, tripInstanceId, dispatchedAt: new Date() }
    });
  }
}
