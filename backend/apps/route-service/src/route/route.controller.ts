import { Controller, Get } from '@nestjs/common';
import { RouteService } from './route.service';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Route')
@Controller()
export class RouteController {
  constructor(private readonly service: RouteService) {}

  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  getHello(): string {
    return this.service.getHello();
  }
}
