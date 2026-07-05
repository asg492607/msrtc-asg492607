import { IsString, IsNotEmpty, IsEnum, IsUUID, IsNumber, Min } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { TransactionSource } from '../enums/finance.enums';

export class RevenueEntryDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  sourceId: string; // e.g., bookingId

  @ApiProperty({ enum: TransactionSource })
  @IsEnum(TransactionSource)
  sourceType: TransactionSource;

  @ApiProperty()
  @IsNumber()
  @Min(0)
  amount: number;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  description: string;
}

export class ExpenseDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  depotId: string;

  @ApiProperty()
  @IsNumber()
  @Min(0.01)
  amount: number;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  description: string;
}

export class ReconciliationDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  depotId: string;

  @ApiProperty()
  @IsNumber()
  reportedCash: number;
}
