import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\api-gateway\src"

# 1. Swagger Aggregation
swagger_ctrl = """import { Controller, Get } from '@nestjs/common';
import axios from 'axios';

@Controller('swagger-json')
export class SwaggerAggregatorController {
  
  @Get()
  async getAggregatedSwagger() {
    // In production, these would be fetched from internal Docker DNS names
    const services = [
      { name: 'Auth', url: 'http://localhost:3001/api/docs/auth-json' },
      { name: 'Booking', url: 'http://localhost:3002/api/docs/bookings-json' }
    ];

    const aggregated = {
      openapi: '3.0.0',
      info: { title: 'MSRTC Enterprise API Gateway', version: '1.0.0' },
      paths: {},
      components: { schemas: {} }
    };

    for (const s of services) {
      try {
        const res = await axios.get(s.url);
        // Merge paths
        for (const [path, methods] of Object.entries(res.data.paths || {})) {
           aggregated.paths[path] = methods;
        }
        // Merge schemas
        for (const [schema, def] of Object.entries(res.data.components?.schemas || {})) {
           aggregated.components.schemas[schema] = def;
        }
      } catch (e) {
        console.error(`Failed to fetch swagger from ${s.name}: ${e.message}`);
      }
    }

    return aggregated;
  }
}
"""
with open(os.path.join(base_dir, "swagger/swagger.controller.ts"), "w", encoding="utf-8") as f: f.write(swagger_ctrl)


# 2. AppModule Integration (Throttler + Proxy)
app_mod = """import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { CircuitBreakerProxyMiddleware } from './proxy/circuit-breaker.middleware';
import { SwaggerAggregatorController } from './swagger/swagger.controller';
// import { RedisModule } from '@msrtc/redis';

@Module({
  imports: [
    // RedisModule, // In reality, we'd use ThrottlerStorageRedisService
    ThrottlerModule.forRoot([{
      ttl: 60000, // 60 seconds
      limit: 100, // 100 requests per minute per IP
    }])
  ],
  controllers: [SwaggerAggregatorController],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard
    }
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(CircuitBreakerProxyMiddleware)
      .exclude('swagger-json') // Don't proxy the swagger endpoint itself
      .forRoutes('*');
  }
}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w", encoding="utf-8") as f: f.write(app_mod)


print("Gateway Hardening Phase 2 Scaffolded (Swagger, Throttler, AppModule)")
