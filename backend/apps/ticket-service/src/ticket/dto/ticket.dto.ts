import { IsString, IsNotEmpty, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class GenerateTicketDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  bookingId: string;
}

export class ValidateTicketDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  qrPayload: string;
}
