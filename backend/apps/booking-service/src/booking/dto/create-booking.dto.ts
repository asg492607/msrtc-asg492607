import { IsString, IsNotEmpty, IsArray, ValidateNested, IsNumber, IsEnum, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty } from '@nestjs/swagger';
import { PassengerGender } from '../../common/enums/booking.enums';

export class PassengerDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty()
  @IsNumber()
  age: number;

  @ApiProperty({ enum: PassengerGender })
  @IsEnum(PassengerGender)
  gender: PassengerGender;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  seatNo: string;
}

export class CreateBookingDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;

  @ApiProperty({ type: [PassengerDto] })
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => PassengerDto)
  passengers: PassengerDto[];
}
