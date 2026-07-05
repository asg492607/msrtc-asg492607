import { NestFactory } from '@nestjs/core';
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
