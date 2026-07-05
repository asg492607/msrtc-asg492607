import { IsString, IsNotEmpty, IsEnum, IsOptional, IsDateString } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { AlertSeverity, MetricDomain } from '../enums/hq.enums';

export class DateRangeDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsDateString()
  startDate?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsDateString()
  endDate?: string;
}

export class AlertFilterDto {
  @ApiPropertyOptional({ enum: AlertSeverity })
  @IsOptional()
  @IsEnum(AlertSeverity)
  severity?: AlertSeverity;
}

export class ReportConfigDto {
  @ApiProperty({ enum: MetricDomain })
  @IsEnum(MetricDomain)
  domain: MetricDomain;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  reportName: string;
}
