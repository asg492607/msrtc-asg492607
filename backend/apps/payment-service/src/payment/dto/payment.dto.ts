import { IsString, IsNotEmpty, IsNumber, IsEnum, IsUUID, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { PaymentGateway } from '../enums/payment.enums';

export class CreatePaymentDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  bookingId: string;

  @ApiProperty()
  @IsNumber()
  amount: number;

  @ApiProperty({ default: 'INR' })
  @IsString()
  @IsNotEmpty()
  currency: string;

  @ApiProperty({ enum: PaymentGateway })
  @IsEnum(PaymentGateway)
  gateway: PaymentGateway;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsString()
  paymentMethod?: string;
}

export class WebhookDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  event: string;

  @ApiProperty()
  @IsNotEmpty()
  payload: any;
}
