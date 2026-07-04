import { Injectable, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class RedisService implements OnModuleDestroy {
  private readonly client: Redis;

  constructor() {
    // In production, use env variables for Redis host/port
    this.client = new Redis({ host: 'localhost', port: 6379, maxRetriesPerRequest: null });
  }

  onModuleDestroy() {
    this.client.disconnect();
  }

  /**
   * Acquires a lock for a specific seat on a specific trip.
   * @param tripId The trip instance ID
   * @param seatNo The seat number (e.g., '1A')
   * @param ttlSeconds Time to live in seconds (e.g., 600 for 10 minutes)
   * @param userId The ID of the user acquiring the lock
   * @returns boolean True if lock acquired successfully, false if already locked
   */
  async lockSeat(tripId: string, seatNo: string, ttlSeconds: number, userId: string): Promise<boolean> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    // SETNX (Set if Not eXists) with EX (Expire in seconds)
    const result = await this.client.set(key, userId, 'EX', ttlSeconds, 'NX');
    return result === 'OK';
  }

  /**
   * Releases a lock for a specific seat on a specific trip.
   * @param tripId The trip instance ID
   * @param seatNo The seat number
   */
  async releaseSeat(tripId: string, seatNo: string): Promise<void> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    await this.client.del(key);
  }

  /**
   * Checks if a seat is currently locked in Redis.
   */
  async isSeatLocked(tripId: string, seatNo: string): Promise<boolean> {
    const key = `lock:trip:${tripId}:seat:${seatNo}`;
    const exists = await this.client.exists(key);
    return exists === 1;
  }
}
