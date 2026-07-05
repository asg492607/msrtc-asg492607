import { Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class OtpService {
  generateOtp(): string {
    return Math.floor(100000 + Math.random() * 900000).toString(); // 6 digit OTP
  }

  verifyOtp(inputOtp: string, actualOtp: string) {
    if (inputOtp !== actualOtp) {
      throw new BadRequestException('Invalid OTP provided for delivery');
    }
    return true;
  }
}
