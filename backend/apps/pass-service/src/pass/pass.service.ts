import { Injectable, NotFoundException, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { PassRepository } from './repository/pass.repository';
import { WorkflowService } from './workflow.service';
import { ConcessionService } from './concession.service';
import { QrService } from './qr.service';
import { CreatePassApplicationDto, RejectPassDto } from './dto/pass.dto';
import { PassStatus } from './enums/pass.enums';

@Injectable()
export class PassService {
  constructor(
    private repository: PassRepository,
    private workflow: WorkflowService,
    private concession: ConcessionService,
    private qrService: QrService
  ) {}

  async applyForPass(userId: string, dto: CreatePassApplicationDto) {
    const discount = this.concession.calculateDiscount(dto.category);
    // Base fare calculation logic would go here
    const fare = 1000 - (1000 * (discount / 100));

    return this.repository.createPassApplication({
      userId,
      category: dto.category,
      originStop: dto.originStop,
      destinationStop: dto.destinationStop,
      documentUrl: dto.documentUrl,
      fare
    });
  }

  async getMyPass(id: string, userId: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    if (pass.userId !== userId) throw new UnauthorizedException();
    return pass;
  }

  async approvePass(id: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    
    // Jump straight to APPROVED (skipping UNDER_REVIEW for brevity in this mock)
    // Normally it goes SUBMITTED -> UNDER_REVIEW -> APPROVED
    this.workflow.validateTransition(pass.status as PassStatus, PassStatus.UNDER_REVIEW);
    
    // Trigger notification: pass.approved
    return this.repository.updateStatus(id, PassStatus.APPROVED);
  }

  async rejectPass(id: string, dto: RejectPassDto) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException('Pass not found');
    // Save rejection reason
    return this.repository.updateStatus(id, PassStatus.REJECTED);
  }

  async activatePass(id: string) {
    const pass = await this.repository.findById(id);
    if (!pass) throw new NotFoundException();
    
    // Assume payment completed
    const validFrom = new Date();
    const validUntil = new Date();
    validUntil.setMonth(validUntil.getMonth() + 1); // 1 Month Pass
    
    const qrCode = await this.qrService.generatePassQr(pass.id, pass.passNumber, validUntil);

    return this.repository.updateStatus(id, PassStatus.ACTIVE, {
      validFrom,
      validUntil,
      qrPayload: qrCode
    });
  }
}
