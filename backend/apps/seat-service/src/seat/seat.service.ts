import { Injectable, BadRequestException } from '@nestjs/common';
import { LockService, CacheKeys } from '@msrtc/redis';

@Injectable()
export class SeatService {
  constructor(private lockService: LockService) {}

  async lockSeat(tripId: string, seatNo: string) {
    const key = CacheKeys.SEAT_LOCK(tripId, seatNo);
    // 10 minutes TTL
    const lockToken = await this.lockService.acquire(key, 600);
    
    if (!lockToken) {
      throw new BadRequestException(`Seat ${seatNo} on trip ${tripId} is currently locked or booked.`);
    }

    return { success: true, lockToken, expiresId: 600 };
  }

  async releaseSeat(tripId: string, seatNo: string, lockToken: string) {
    const key = CacheKeys.SEAT_LOCK(tripId, seatNo);
    const success = await this.lockService.release(key, lockToken);
    
    if (!success) {
      // Could be expired or invalid token
      return { success: false, message: 'Invalid lock token or lock expired' };
    }
    return { success: true };
  }
}
