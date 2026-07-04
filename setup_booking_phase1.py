import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps\booking-service\src"

dirs = [
    "common/enums",
    "common/constants",
    "common/filters",
    "common/interceptors",
    "common/guards",
    "common/decorators",
    "booking/dto",
    "booking/repository",
    "prisma"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Enums
enums = """export enum BookingStatus {
  PENDING = 'PENDING',
  SEAT_LOCKED = 'SEAT_LOCKED',
  PAYMENT_PENDING = 'PAYMENT_PENDING',
  CONFIRMED = 'CONFIRMED',
  CANCELLED = 'CANCELLED',
  PARTIALLY_CANCELLED = 'PARTIALLY_CANCELLED',
  REFUNDED = 'REFUNDED',
  EXPIRED = 'EXPIRED',
}

export enum PassengerGender {
  MALE = 'MALE',
  FEMALE = 'FEMALE',
  OTHER = 'OTHER',
}
"""
with open(os.path.join(base_dir, "common/enums/booking.enums.ts"), "w") as f: f.write(enums)


# 2. DTOs
create_booking_dto = """import { IsString, IsNotEmpty, IsArray, ValidateNested, IsNumber, IsEnum, IsUUID } from 'class-validator';
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
"""
with open(os.path.join(base_dir, "booking/dto/create-booking.dto.ts"), "w") as f: f.write(create_booking_dto)


# 3. Prisma Service
prisma_service = """import { Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
"""
with open(os.path.join(base_dir, "prisma/prisma.service.ts"), "w") as f: f.write(prisma_service)

prisma_module = """import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
"""
with open(os.path.join(base_dir, "prisma/prisma.module.ts"), "w") as f: f.write(prisma_module)


# 4. Repository (Data Access Layer Pattern)
repo = """import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { BookingStatus } from '../../common/enums/booking.enums';

@Injectable()
export class BookingRepository {
  constructor(private prisma: PrismaService) {}

  async createPendingBooking(userId: string, tripId: string, passengers: any[], totalFare: number) {
    // We use an interactive transaction to ensure atomicity
    return this.prisma.$transaction(async (tx) => {
      // 1. Create the booking record
      const booking = await tx.booking.create({
        data: {
          pnr: `PNR${Date.now()}${Math.floor(Math.random() * 1000)}`,
          userId,
          tripInstanceId: tripId,
          status: BookingStatus.PENDING,
          totalFare,
          netAmount: totalFare,
        },
      });

      // 2. Create passenger records
      const passengerData = passengers.map(p => ({
        bookingId: booking.id,
        name: p.name,
        age: p.age,
        gender: p.gender,
        seatNo: p.seatNo,
        status: 'CONFIRMED',
        fare: totalFare / passengers.length // Mock fare split
      }));

      await tx.bookingPassenger.createMany({
        data: passengerData,
      });

      // 3. Create Audit Log
      await tx.bookingLog.create({
        data: {
          bookingId: booking.id,
          action: 'BOOKING_INITIATED',
        }
      });

      return booking;
    });
  }
  
  async findBookingById(id: string) {
    return this.prisma.booking.findUnique({
      where: { id },
      include: { passengers: true }
    });
  }

  async updateBookingStatus(id: string, status: BookingStatus) {
    return this.prisma.booking.update({
      where: { id },
      data: { status }
    });
  }
}
"""
with open(os.path.join(base_dir, "booking/repository/booking.repository.ts"), "w") as f: f.write(repo)

print("Booking Service Phase 1 Scaffolded (Enums, DTOs, Repo)")
