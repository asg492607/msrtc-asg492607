import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1/notification');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Notification Service')
    .setDescription('The Notification API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/notification', app, document);

  await app.listen(3011);
  console.log('Notification Service is running on http://localhost:3011');
}
bootstrap();
