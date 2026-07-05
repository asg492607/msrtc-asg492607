import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { PassStatus, PassCategory } from '../enums/pass.enums';

@Injectable()
export class PassRepository {
  constructor(private prisma: PrismaService) {}

  async createPassApplication(data: any) {
    const passNumber = `PASS-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.pass.create({
      data: {
        ...data,
        passNumber,
        status: PassStatus.SUBMITTED,
      }
    });
  }

  async findById(id: string) {
    return this.prisma.pass.findUnique({ where: { id } });
  }

  async updateStatus(id: string, status: PassStatus, additionalData: any = {}) {
    return this.prisma.pass.update({
      where: { id },
      data: { status, ...additionalData }
    });
  }
}
