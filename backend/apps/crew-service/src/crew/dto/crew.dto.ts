import { IsString, IsNotEmpty, IsEnum, IsUUID, IsDateString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { CrewRole } from '../enums/crew.enums';

export class CreateEmployeeDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty({ enum: CrewRole })
  @IsEnum(CrewRole)
  role: CrewRole;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  depotId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  licenseNumber: string;

  @ApiProperty()
  @IsDateString()
  licenseExpiry: string;
}

export class AssignCrewDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;
}
