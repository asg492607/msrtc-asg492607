import { Injectable, ConflictException, BadRequestException } from '@nestjs/common';
import { SeatRepository } from './repository/seat.repository';
import { RedisService } from '../redis/redis.service';
import { LockSeatDto } from './dto/lock-seat.dto';

@Injectable()
export class SeatService {
  constructor(
    private readonly repository: SeatRepository,
    private readonly redis: RedisService
  ) {}

  /**
   * Attempts to lock seats concurrently via Redis.
   */
  async lockSeats(userId: string, dto: LockSeatDto) {
    const lockedSeats: string[] = [];
    const TTL_SECONDS = 600; // 10 minutes to complete booking & payment

    try {
      for (const seatNo of dto.seatNumbers) {
        // 1. Check if permanently booked in Postgres
        const isPermanentlyBooked = await this.repository.isSeatPermanentlyBooked(dto.tripInstanceId, seatNo);
        if (isPermanentlyBooked) {
          throw new ConflictException(`Seat ${seatNo} is already booked.`);
        }

        // 2. Attempt to acquire Redis Lock
        const lockAcquired = await this.redis.lockSeat(dto.tripInstanceId, seatNo, TTL_SECONDS, userId);
        if (!lockAcquired) {
          throw new ConflictException(`Seat ${seatNo} is currently reserved by another user.`);
        }
        
        lockedSeats.push(seatNo);
      }

      return {
        message: 'Seats locked successfully for 10 minutes.',
        tripInstanceId: dto.tripInstanceId,
        lockedSeats,
        expiresIn: TTL_SECONDS
      };

    } catch (error) {
      // Rollback: Release any seats we managed to lock before the failure occurred
      for (const seatNo of lockedSeats) {
        await this.redis.releaseSeat(dto.tripInstanceId, seatNo);
      }
      throw error;
    }
  }

  /**
   * Releases seats manually (e.g. if passenger cancels booking before payment).
   */
  async releaseSeats(userId: string, dto: LockSeatDto) {
    for (const seatNo of dto.seatNumbers) {
      // In a real system, we'd verify the user owns the lock before releasing it
      await this.redis.releaseSeat(dto.tripInstanceId, seatNo);
    }
    return { message: 'Seats released successfully.' };
  }
}
