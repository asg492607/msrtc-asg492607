import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1/passenger');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Passenger Service')
    .setDescription('The Passenger API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/passenger', app, document);

  await app.listen(3009);
  console.log('Passenger Service is running on http://localhost:3009');
}
bootstrap();
