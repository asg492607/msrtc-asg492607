import { Controller, Post, Param, Body, UseGuards } from '@nestjs/common';
import { ParcelService } from './parcel.service';
import { DeliverParcelDto } from './dto/parcel.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ParcelStatus } from './enums/parcel.enums';

@ApiTags('Parcel Operations (Clerks)')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller('admin/parcels')
export class AdminController {
  constructor(private readonly parcelService: ParcelService) {}

  @Post(':id/advance/:status')
  @Roles('Parcel_Clerk', 'Depot_Manager')
  @ApiOperation({ summary: 'Advance parcel state (e.g. DISPATCHED, ARRIVED, READY_FOR_PICKUP)' })
  async advance(@Param('id') id: string, @Param('status') status: ParcelStatus) {
    return this.parcelService.advanceStatus(id, status);
  }

  @Post(':id/deliver')
  @Roles('Parcel_Clerk')
  @ApiOperation({ summary: 'Handover parcel to receiver (Requires OTP verification)' })
  async deliver(@Param('id') id: string, @Body() dto: DeliverParcelDto) {
    return this.parcelService.deliverParcel(id, dto);
  }
}
