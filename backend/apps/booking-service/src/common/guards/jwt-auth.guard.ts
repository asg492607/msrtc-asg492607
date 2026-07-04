import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

// Simple mocked guard for the reference architecture.
// In a real microservice mesh, this would validate the token against the auth-service or verify the signature locally.
@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    // Mock user injection
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Passenger'] };
    return true;
  }
}
