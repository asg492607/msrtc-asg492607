import { Controller, Post, Get, Body, Param, UseGuards, Request } from '@nestjs/common';
import { PassService } from './pass.service';
import { CreatePassApplicationDto } from './dto/pass.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('Passenger Passes')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('passes')
export class PassController {
  constructor(private readonly passService: PassService) {}

  @Post('apply')
  @ApiOperation({ summary: 'Apply for a new monthly or concession pass' })
  async apply(@Request() req, @Body() dto: CreatePassApplicationDto) {
    return this.passService.applyForPass(req.user.userId, dto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'View a specific pass (Passenger)' })
  async getPass(@Request() req, @Param('id') id: string) {
    return this.passService.getMyPass(id, req.user.userId);
  }

  @Post(':id/mock-payment')
  @ApiOperation({ summary: 'Mock endpoint to simulate payment completion -> Activation' })
  async mockPayment(@Param('id') id: string) {
    return this.passService.activatePass(id);
  }
}
