import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CrewStatus } from '../enums/crew.enums';

@Injectable()
export class CrewRepository {
  constructor(private prisma: PrismaService) {}

  async createEmployee(data: any) {
    const employeeId = `EMP-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.crew.create({
      data: {
        ...data,
        employeeId,
        status: CrewStatus.AVAILABLE,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.crew.findUnique({ where: { id } });
  }

  async updateStatus(id: string, status: CrewStatus) {
    return this.prisma.crew.update({
      where: { id },
      data: { status }
    });
  }

  async saveAssignment(crewId: string, tripInstanceId: string) {
    return this.prisma.crewAssignment.create({
      data: { crewId, tripInstanceId, assignedAt: new Date() }
    });
  }
}
