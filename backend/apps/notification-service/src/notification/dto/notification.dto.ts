import { IsString, IsNotEmpty, IsEnum, IsUUID, IsObject, IsOptional, IsArray } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { NotificationChannel } from '../enums/notification.enums';

export class SendNotificationDto {
  @ApiProperty()
  @IsUUID()
  @IsNotEmpty()
  userId: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  templateCode: string;

  @ApiProperty({ enum: [NotificationChannel] })
  @IsArray()
  @IsEnum(NotificationChannel, { each: true })
  channels: NotificationChannel[];

  @ApiProperty()
  @IsObject()
  @IsOptional()
  payload?: Record<string, any>;
}
