import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
ff_src = os.path.join(base_dir, "backend/apps/feature-flag-service/src")
rm_dir = os.path.join(base_dir, "release-management")

os.makedirs(os.path.join(rm_dir, "argo-rollouts"), exist_ok=True)
os.makedirs(os.path.join(rm_dir, "rollout-policies"), exist_ok=True)
os.makedirs(os.path.join(rm_dir, "docs"), exist_ok=True)

# 1. Feature Flag Service
ff_svc = """import { Injectable, Logger } from '@nestjs/common';
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
"""
with open(os.path.join(ff_src, "flags/services/feature-flag.service.ts"), "w", encoding="utf-8") as f: f.write(ff_svc)


# 2. Controllers
ff_ctrl = """import { Controller, Get, Param, Query } from '@nestjs/common';
import { FeatureFlagService } from '../services/feature-flag.service';

@Controller('feature-flags')
export class FeatureFlagController {
  constructor(private flagService: FeatureFlagService) {}

  @Get(':key/eval')
  async evaluateFlag(@Param('key') key: string) {
    const isEnabled = await this.flagService.isEnabled(key);
    return { key, isEnabled };
  }
}
"""
with open(os.path.join(ff_src, "flags/controllers/feature-flag.controller.ts"), "w", encoding="utf-8") as f: f.write(ff_ctrl)


# 3. Module & Main
ff_mod = """import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { FeatureFlagService } from './flags/services/feature-flag.service';
import { FeatureFlagController } from './flags/controllers/feature-flag.controller';
import { PrismaModule } from './prisma/prisma.module';
import { RedisModule } from '@msrtc/redis';
import { TenantModule, TenantMiddleware } from '@msrtc/tenant';

@Module({
  imports: [PrismaModule, RedisModule, TenantModule],
  controllers: [FeatureFlagController],
  providers: [FeatureFlagService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
     consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
"""
with open(os.path.join(ff_src, "app.module.ts"), "w", encoding="utf-8") as f: f.write(ff_mod)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix('api/v1');
  await app.listen(3024);
  console.log('Feature Flag Service is running on http://localhost:3024');
}
bootstrap();
"""
with open(os.path.join(ff_src, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


# 4. Argo Rollouts Configuration
argo_canary = """apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: booking-service
spec:
  replicas: 5
  strategy:
    canary:
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2 # Start analysis on step 2
        args:
        - name: service-name
          value: booking-service
      steps:
      - setWeight: 10
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {duration: 10m}
      - setWeight: 100
  selector:
    matchLabels:
      app: booking-service
  template:
    metadata:
      labels:
        app: booking-service
    spec:
      containers:
      - name: booking-service
        image: ghcr.io/msrtc/booking-service:latest
"""
with open(os.path.join(rm_dir, "argo-rollouts/canary-strategy.yaml"), "w", encoding="utf-8") as f: f.write(argo_canary)

argo_analysis = """apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 1m
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: >+
          sum(rate(http_requests_total{job="{{args.service-name}}", status!~"5.*"}[1m])) 
          / 
          sum(rate(http_requests_total{job="{{args.service-name}}"}[1m]))
"""
with open(os.path.join(rm_dir, "rollout-policies/success-rate-analysis.yaml"), "w", encoding="utf-8") as f: f.write(argo_analysis)


# 5. Documentation
docs_runbook = """# Release Runbook

## Overview
MSRTC utilizes **Argo Rollouts** to provide Zero-Downtime deployments. We no longer use standard Kubernetes `Deployments`; we use `Rollouts`.

## Canary Strategy
When a new container image is synced by ArgoCD:
1. **10% Traffic:** Argo spins up a small subset of the new Pods and routes 10% of live traffic to them.
2. **Analysis:** The `AnalysisTemplate` constantly queries Prometheus. If the HTTP 500 error rate spikes or latency drops below 95% success, Argo **automatically aborts and rolls back**.
3. **50% Traffic:** If healthy after 10 minutes, traffic shifts to 50%.
4. **100% Traffic:** If healthy, the old Pods are completely terminated.
"""
with open(os.path.join(rm_dir, "docs/RELEASE_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(docs_runbook)

docs_ff = """# Feature Flag Guide

## Decoupling Deployment from Release
Code deployment (pushing to Kubernetes) should be boring. Releasing a feature (turning it on for users) is a business decision.

## `feature-flag-service`
To wrap a new risky feature:
```typescript
const isEnabled = await this.ffService.isEnabled('NEW_PAYMENT_GATEWAY');
if (isEnabled) {
   // Execute new logic
} else {
   // Fallback to old logic
}
```
If the new payment gateway crashes in production, a Product Manager simply toggles the flag to `false` via the API. The Redis cache expires in 5 minutes, instantly routing users back to the safe code without requiring a hotfix deployment.
"""
with open(os.path.join(rm_dir, "docs/FEATURE_FLAG_GUIDE.md"), "w", encoding="utf-8") as f: f.write(docs_ff)

print("Release Management Phase 2 Scaffolded")
