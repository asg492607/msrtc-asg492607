import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1/fleet');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Fleet Service')
    .setDescription('The Fleet API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/fleet', app, document);

  await app.listen(3003);
  console.log('Fleet Service is running on http://localhost:3003');
}
bootstrap();
