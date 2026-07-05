import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { CircuitBreakerProxyMiddleware } from './proxy/circuit-breaker.middleware';
import { SwaggerAggregatorController } from './swagger/swagger.controller';
import { AppController } from './app.controller';
import { ServeStaticModule } from '@nestjs/serve-static';
import { join } from 'path';
// import { RedisModule } from '@msrtc/redis';

@Module({
  imports: [
    // RedisModule, // In reality, we'd use ThrottlerStorageRedisService
    ThrottlerModule.forRoot([{
      ttl: 60000, // 60 seconds
      limit: 100, // 100 requests per minute per IP
    }]),
    ServeStaticModule.forRoot({
      rootPath: join(process.cwd(), '..', '..', '..'), // Up to msrtc root from api-gateway
      exclude: ['/api/(.*)', '/swagger-json'],
    })
  ],
  controllers: [SwaggerAggregatorController, AppController],
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
