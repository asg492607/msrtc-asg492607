import { Controller, Post, UseInterceptors, UploadedFile, Body, UseGuards, Request } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { FileService } from '../services/file.service';
// import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiConsumes, ApiBody } from '@nestjs/swagger';

@ApiTags('File Upload')
@Controller('files')
// @UseGuards(JwtAuthGuard)
export class UploadController {
  constructor(private fileService: FileService) {}

  @Post('upload')
  @ApiConsumes('multipart/form-data')
  @ApiOperation({ summary: 'Upload a binary file to object storage' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: Express.Multer.File, @Body('folder') folder: string, @Request() req: any) {
    // const userId = req.user.userId;
    const userId = 'sys-admin'; // mocked for now
    return this.fileService.processUpload(file, folder || 'misc', userId);
  }
}
