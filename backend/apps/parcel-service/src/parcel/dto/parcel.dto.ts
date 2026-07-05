import { IsString, IsNotEmpty, IsNumber, IsOptional, MaxLength, Min, ValidateNested, IsArray, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty } from '@nestjs/swagger';

export class ParcelItemDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  description: string;

  @ApiProperty()
  @IsNumber()
  @Min(0.1)
  weightKg: number;

  @ApiProperty()
  @IsNumber()
  @Min(0.1)
  volumeCbM: number;
}

export class CreateParcelDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  senderId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  receiverName: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  receiverPhone: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  originDepotId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  destinationDepotId: string;

  @ApiProperty({ type: [ParcelItemDto] })
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => ParcelItemDto)
  items: ParcelItemDto[];
}

export class DeliverParcelDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  otp: string;
}
