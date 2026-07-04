import { IsString, IsNotEmpty, IsArray, ArrayMinSize, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class LockSeatDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  tripInstanceId: string;

  @ApiProperty({ type: [String], example: ['1A', '1B'] })
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  seatNumbers: string[];
}
