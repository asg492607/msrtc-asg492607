import { Controller, Get, Param, UseGuards } from '@nestjs/common';
import { FileService } from '../services/file.service';
// import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('File Download')
@Controller('files')
// @UseGuards(JwtAuthGuard)
export class DownloadController {
  constructor(private fileService: FileService) {}

  @Get(':id/presign')
  @ApiOperation({ summary: 'Get a temporary, secure download URL' })
  async getPresignedUrl(@Param('id') id: string) {
    const url = await this.fileService.getDownloadUrl(id);
    return { url, expiresIn: 900 }; // 15 mins
  }
}
