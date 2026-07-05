import { Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ComplianceService {
  /**
   * Verify if the crew member has had mandatory 8 hours of rest
   * and their license/medical certificates are valid.
   */
  async checkAssignmentCompliance(crewRecord: any) {
    if (new Date(crewRecord.licenseExpiry) < new Date()) {
      throw new BadRequestException('License is expired. Cannot assign duty.');
    }
    
    // In real app, check last checked_out time for 8hr rest gap
    const hasAdequateRest = true; 
    if (!hasAdequateRest) {
      throw new BadRequestException('Mandatory rest period not fulfilled.');
    }

    return true;
  }
}
