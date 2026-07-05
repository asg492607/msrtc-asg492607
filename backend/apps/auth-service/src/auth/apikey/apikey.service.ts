import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import * as crypto from 'crypto';

@Injectable()
export class ApiKeyService {
  constructor(private prisma: PrismaService) {}

  async generateApiKey(name: string, serviceName?: string) {
    const rawKey = crypto.randomBytes(32).toString('hex');
    const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');

    const apiKey = await this.prisma.apiKey.create({
      data: { name, serviceName, keyHash }
    });

    return { apiKeyId: apiKey.id, rawKey }; // rawKey is only shown once
  }

  async validateApiKey(rawKey: string): Promise<boolean> {
    const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
    const key = await this.prisma.apiKey.findUnique({ where: { keyHash } });
    return key ? key.isActive : false;
  }
}
