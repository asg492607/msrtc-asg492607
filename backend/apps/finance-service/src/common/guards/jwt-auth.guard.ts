import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;
    if (!authHeader) {
      throw new UnauthorizedException('Missing authorization header');
    }
    // Mock user decoding
    request.user = { userId: '123e4567-e89b-12d3-a456-426614174000', roles: ['Finance_Officer', 'Auditor', 'Depot_Manager', 'HQ_Admin'] };
    return true;
  }
}
