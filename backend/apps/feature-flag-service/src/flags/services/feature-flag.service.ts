import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CacheService } from '@msrtc/redis';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class FeatureFlagService {
  private readonly logger = new Logger(FeatureFlagService.name);

  constructor(
    private prisma: PrismaService,
    private cache: CacheService,
    private cls: ClsService
  ) {}

  async isEnabled(key: string, context?: any): Promise<boolean> {
    const tenantId = this.cls.get('tenantId') || 'global';
    const cacheKey = `tenant:${tenantId}:flag:${key}`;
    
    // Fast path: Redis
    let cached = await this.cache.get(cacheKey);
    if (cached !== null) {
      return cached === 'true';
    }

    // Slow path: Postgres
    const flag = await this.prisma.featureFlag.findUnique({ where: { key } });
    if (!flag) return false;

    // Simple tenant override logic (can be expanded for percentages/roles)
    const result = flag.isEnabled;
    
    await this.cache.set(cacheKey, result ? 'true' : 'false', 300); // 5 min TTL
    return result;
  }
}
