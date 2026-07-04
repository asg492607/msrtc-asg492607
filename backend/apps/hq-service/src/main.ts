import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1/hq');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Hq Service')
    .setDescription('The Hq API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/hq', app, document);

  await app.listen(3019);
  console.log('Hq Service is running on http://localhost:3019');
}
bootstrap();
