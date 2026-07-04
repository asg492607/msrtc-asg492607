import { IsString, IsNotEmpty, IsDateString, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class SearchTripsDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  sourceStationId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  destinationStationId: string;

  @ApiProperty()
  @IsDateString()
  travelDate: string;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsString()
  busType?: string;
}
