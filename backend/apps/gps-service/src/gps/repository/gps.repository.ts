import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class GpsRepository {
  constructor(private prisma: PrismaService) {}

  async savePingHistory(vehicleId: string, tripInstanceId: string, lat: number, lng: number, speed?: number) {
    // Note: In a real system, we'd batch these writes to avoid killing the DB
    return this.prisma.vehicleLocation.create({
      data: {
        vehicleId,
        tripInstanceId,
        latitude: lat,
        longitude: lng,
        speed,
        timestamp: new Date()
      }
    });
  }
}
