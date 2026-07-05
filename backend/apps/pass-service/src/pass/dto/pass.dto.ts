import { IsString, IsNotEmpty, IsEnum, IsUUID, IsOptional, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { PassCategory } from '../enums/pass.enums';

export class CreatePassApplicationDto {
  @ApiProperty({ enum: PassCategory })
  @IsEnum(PassCategory)
  category: PassCategory;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  originStop: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  destinationStop: string;

  @ApiProperty({ description: 'URL to uploaded ID document' })
  @IsString()
  @IsNotEmpty()
  documentUrl: string;
}

export class ValidatePassDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  qrPayload: string;
}

export class RejectPassDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  reason: string;
}
