import { IsString, IsNotEmpty, IsUUID, IsNumber } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateDepotDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  location: string;
}

export class AddBusDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  registrationNumber: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  depotId: string;
}

export class DispatchBusDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;

  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  crewAssignmentId: string; // To verify crew check-in
}

export class AssignPlatformDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty()
  @IsNumber()
  @IsNotEmpty()
  platformNumber: number;
}
