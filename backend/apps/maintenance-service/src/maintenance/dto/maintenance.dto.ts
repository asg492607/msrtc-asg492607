import { IsString, IsNotEmpty, IsEnum, IsUUID, IsNumber, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { JobType } from '../enums/maintenance.enums';

export class CreateMaintenanceJobDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty({ enum: JobType })
  @IsEnum(JobType)
  jobType: JobType;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  description: string;
}

export class BreakdownReportDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  busId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  locationCoordinates: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  issueDescription: string;
}

export class InspectionDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  comments: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  passed: string; // 'YES' or 'NO'
}

export class CompleteMaintenanceDto {
  @ApiProperty()
  @IsNumber()
  @IsNotEmpty()
  laborHours: number;
}
