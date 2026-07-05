import { IsString, IsNotEmpty, IsEnum, IsUUID, IsOptional, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { ComplaintCategory, ComplaintPriority, ComplaintStatus } from '../enums/complaint.enums';

export class CreateComplaintDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  title: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(1000)
  description: string;

  @ApiProperty({ enum: ComplaintCategory })
  @IsEnum(ComplaintCategory)
  category: ComplaintCategory;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsUUID()
  bookingId?: string;
}

export class AssignComplaintDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  assigneeId: string;
}

export class ComplaintCommentDto {
  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  @MaxLength(500)
  content: string;

  @ApiProperty()
  @IsOptional()
  isInternal?: boolean;
}
