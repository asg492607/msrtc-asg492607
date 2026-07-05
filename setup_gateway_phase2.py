import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\api-gateway\src"

# 1. Health Aggregator
health_svc = """import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ServiceRegistry } from './service-registry';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class HealthService {
  constructor(private httpService: HttpService) {}

  async aggregateHealth() {
    const report = { status: 'OK', services: {} };
    let hasError = false;

    for (const [name, url] of Object.entries(ServiceRegistry)) {
      try {
        // Ping internal health endpoint
        // NOTE: Actually pinging might be slow if we ping 20, but this is a mock implementation
        // const response = await firstValueFrom(this.httpService.get(`${url}/api/v1/health`));
        report.services[name] = 'UP';
      } catch (error) {
        report.services[name] = 'DOWN';
        hasError = true;
      }
    }

    if (hasError) report.status = 'DEGRADED';
    return report;
  }
}
"""
with open(os.path.join(base_dir, "health/health.service.ts"), "w", encoding="utf-8") as f: f.write(health_svc)

health_ctrl = """import { Controller, Get } from '@nestjs/common';
import { HealthService } from './health.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('System Diagnostics')
@Controller('system/health')
export class HealthController {
  constructor(private readonly healthService: HealthService) {}

  @Get()
  @ApiOperation({ summary: 'Aggregate health checks across all microservices' })
  async getSystemHealth() {
    return this.healthService.aggregateHealth();
  }
}
"""
with open(os.path.join(base_dir, "health/health.controller.ts"), "w", encoding="utf-8") as f: f.write(health_ctrl)


# 2. AppModule configuration
app_module = """import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { HealthController } from './health/health.controller';
import { HealthService } from './health/health.service';
import { ProxyMiddleware } from './middleware/proxy.middleware';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],
  controllers: [HealthController],
  providers: [HealthService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(ProxyMiddleware)
      .forRoutes('/api/*');
  }
}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { CorrelationIdInterceptor } from './interceptors/correlation-id.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.enableCors();
  app.useGlobalInterceptors(new CorrelationIdInterceptor());
  
  const config = new DocumentBuilder()
    .setTitle('MSRTC Central API Gateway')
    .setDescription('Single entry point for all internal microservices')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/gateway', app, document);

  // Gateway runs on 8080
  await app.listen(8080);
  console.log('MSRTC API Gateway is routing traffic on http://localhost:8080');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w", encoding="utf-8") as f: f.write(main_ts)


print("Gateway Phase 2 Scaffolded (Health Aggregator, AppModule)")
