import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\booking-service\src"

# 1. Global Exception Filter
http_exception_filter = """import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = 
      exception instanceof HttpException
        ? exception.getResponse()
        : 'Internal server error';

    // Log the error (would use Pino/Winston here)
    console.error(`[${request.method}] ${request.url} - ${status}`, exception);

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: typeof message === 'string' ? message : (message as any).message || message,
    });
  }
}
"""
with open(os.path.join(base_dir, "common/filters/http-exception.filter.ts"), "w") as f: f.write(http_exception_filter)

# 2. Update Main to use the filter
main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1/booking');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Booking Service')
    .setDescription('The Core Reservation Engine API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/booking', app, document);

  await app.listen(3005);
  console.log('Booking Service is running on http://localhost:3005');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)

print("Exception Filters and Main updated.")
