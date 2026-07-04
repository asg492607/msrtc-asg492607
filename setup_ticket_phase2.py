import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\ticket-service\src"

# 1. Repository
ticket_repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { TicketStatus } from '../enums/ticket.enums';

@Injectable()
export class TicketRepository {
  constructor(private prisma: PrismaService) {}

  async createTicket(bookingId: string, ticketNumber: string, pnr: string, qrPayload: string, pdfUrl: string) {
    return this.prisma.ticket.create({
      data: {
        bookingId,
        ticketNumber,
        pnr,
        status: TicketStatus.GENERATED,
        qrPayload,
        pdfUrl,
      }
    });
  }

  async findTicketById(id: string) {
    return this.prisma.ticket.findUnique({ where: { id } });
  }

  async updateTicketStatus(id: string, status: TicketStatus) {
    return this.prisma.ticket.update({
      where: { id },
      data: { status }
    });
  }
}
"""
with open(os.path.join(base_dir, "ticket/repository/ticket.repository.ts"), "w") as f: f.write(ticket_repo)


# 2. QR Service
qr_svc = """import { Injectable } from '@nestjs/common';
import * as QRCode from 'qrcode';

@Injectable()
export class QrService {
  /**
   * Generates a base64 Data URI for a given payload.
   * In a real implementation, the payload includes a checksum to prevent forgery.
   */
  async generateQrCode(payload: any): Promise<string> {
    const stringified = JSON.stringify(payload);
    // Return Base64 encoded image
    return QRCode.toDataURL(stringified);
  }

  /**
   * Decodes and verifies a QR payload (e.g., checksum validation).
   */
  verifyPayload(payloadStr: string): any {
    try {
      const payload = JSON.parse(payloadStr);
      // Mock Checksum verification
      if (!payload.checksum) throw new Error('Invalid checksum');
      return payload;
    } catch (e) {
      return null;
    }
  }
}
"""
with open(os.path.join(base_dir, "ticket/qr.service.ts"), "w") as f: f.write(qr_svc)


# 3. PDF Service
pdf_svc = """import { Injectable } from '@nestjs/common';

@Injectable()
export class PdfService {
  /**
   * Mock PDF generation.
   * In production, this would use pdfkit or puppeteer, store the PDF in AWS S3,
   * and return the S3 URL.
   */
  async generateTicketPdf(ticketData: any): Promise<string> {
    const mockS3Url = `https://msrtc-tickets.s3.ap-south-1.amazonaws.com/${ticketData.ticketNumber}.pdf`;
    console.log(`[PDF Service] Generated PDF and uploaded to ${mockS3Url}`);
    return mockS3Url;
  }
}
"""
with open(os.path.join(base_dir, "ticket/pdf.service.ts"), "w") as f: f.write(pdf_svc)


# 4. Validator Service (For Conductors)
val_svc = """import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { TicketRepository } from './repository/ticket.repository';
import { QrService } from './qr.service';
import { ValidateTicketDto } from './dto/ticket.dto';
import { TicketStatus } from './enums/ticket.enums';

@Injectable()
export class ValidatorService {
  constructor(
    private readonly repository: TicketRepository,
    private readonly qrService: QrService
  ) {}

  async validateScannedQr(dto: ValidateTicketDto) {
    // 1. Decode and verify signature/checksum
    const decodedPayload = this.qrService.verifyPayload(dto.qrPayload);
    if (!decodedPayload) {
      throw new BadRequestException('Invalid or forged QR Code');
    }

    // 2. Fetch Ticket
    const ticket = await this.repository.findTicketById(decodedPayload.ticketId);
    if (!ticket) {
      throw new NotFoundException('Ticket record not found in database');
    }

    // 3. State Machine Checks
    if (ticket.status === TicketStatus.CANCELLED || ticket.status === TicketStatus.ARCHIVED) {
      throw new BadRequestException(`Ticket is ${ticket.status}`);
    }

    // If valid, mark as USED
    await this.repository.updateTicketStatus(ticket.id, TicketStatus.USED);

    return {
      valid: true,
      ticket: {
        id: ticket.id,
        pnr: ticket.pnr,
        status: 'USED'
      }
    };
  }
}
"""
with open(os.path.join(base_dir, "ticket/validator.service.ts"), "w") as f: f.write(val_svc)


# 5. Ticket Service
ticket_svc = """import { Injectable, BadRequestException } from '@nestjs/common';
import { TicketRepository } from './repository/ticket.repository';
import { QrService } from './qr.service';
import { PdfService } from './pdf.service';
import { GenerateTicketDto } from './dto/ticket.dto';

@Injectable()
export class TicketService {
  constructor(
    private readonly repository: TicketRepository,
    private readonly qrService: QrService,
    private readonly pdfService: PdfService
  ) {}

  async generateTicket(dto: GenerateTicketDto) {
    // In real app, query Booking Service to ensure it is CONFIRMED and PAYMENT_SUCCESS
    const isBookingConfirmed = true; 
    if (!isBookingConfirmed) {
      throw new BadRequestException('Cannot generate ticket for unconfirmed booking');
    }

    const ticketNumber = `TKT-${Date.now()}`;
    const pnr = `PNR-${Math.random().toString(36).substring(7).toUpperCase()}`;

    // Generate QR
    const qrPayloadObj = {
      ticketId: ticketNumber, // Mock mapping
      bookingId: dto.bookingId,
      pnr: pnr,
      checksum: 'valid-hash'
    };
    const qrCodeBase64 = await this.qrService.generateQrCode(qrPayloadObj);

    // Generate PDF
    const pdfUrl = await this.pdfService.generateTicketPdf({ ticketNumber, pnr, qr: qrCodeBase64 });

    // Persist
    const ticket = await this.repository.createTicket(dto.bookingId, ticketNumber, pnr, JSON.stringify(qrPayloadObj), pdfUrl);

    // Kafka event emission would happen here

    return ticket;
  }
}
"""
with open(os.path.join(base_dir, "ticket/ticket.service.ts"), "w") as f: f.write(ticket_svc)


# 6. Controllers
ticket_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { TicketService } from './ticket.service';
import { GenerateTicketDto } from './dto/ticket.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Tickets')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('tickets')
export class TicketController {
  constructor(private readonly ticketService: TicketService) {}

  @Post('generate')
  @ApiOperation({ summary: 'Generate a new QR/PDF ticket for a confirmed booking' })
  async generateTicket(@Body() dto: GenerateTicketDto) {
    return this.ticketService.generateTicket(dto);
  }
}
"""
with open(os.path.join(base_dir, "ticket/ticket.controller.ts"), "w") as f: f.write(ticket_ctrl)


val_ctrl = """import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ValidatorService } from './validator.service';
import { ValidateTicketDto } from './dto/ticket.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Validation (Conductors)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('validation')
export class ValidationController {
  constructor(private readonly validatorService: ValidatorService) {}

  @Post('scan')
  @Roles('Conductor', 'Inspector')
  @ApiOperation({ summary: 'Scan and validate a ticket QR code (Conductors Only)' })
  async scanQrCode(@Body() dto: ValidateTicketDto) {
    return this.validatorService.validateScannedQr(dto);
  }
}
"""
with open(os.path.join(base_dir, "ticket/validation.controller.ts"), "w") as f: f.write(val_ctrl)


# 7. Modules
ticket_mod = """import { Module } from '@nestjs/common';
import { TicketController } from './ticket.controller';
import { ValidationController } from './validation.controller';
import { TicketService } from './ticket.service';
import { ValidatorService } from './validator.service';
import { QrService } from './qr.service';
import { PdfService } from './pdf.service';
import { TicketRepository } from './repository/ticket.repository';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [TicketController, ValidationController],
  providers: [TicketService, ValidatorService, QrService, PdfService, TicketRepository],
})
export class TicketModule {}
"""
with open(os.path.join(base_dir, "ticket/ticket.module.ts"), "w") as f: f.write(ticket_mod)

app_module = """import { Module } from '@nestjs/common';
import { TicketModule } from './ticket/ticket.module';

@Module({
  imports: [TicketModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "app.module.ts"), "w") as f: f.write(app_module)

main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new AllExceptionsFilter());
  
  app.setGlobalPrefix('api/v1');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Ticket Service')
    .setDescription('QR Generation and Conductor Validation API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/ticket', app, document);

  await app.listen(3008);
  console.log('Ticket Service is running on http://localhost:3008');
}
bootstrap();
"""
with open(os.path.join(base_dir, "main.ts"), "w") as f: f.write(main_ts)


print("Ticket Service Phase 2 Scaffolded (QR, PDF, Validator, Controllers)")
