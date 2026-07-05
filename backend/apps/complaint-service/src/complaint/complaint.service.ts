import { Injectable, NotFoundException, BadRequestException, UnauthorizedException } from '@nestjs/common';
import { ComplaintRepository } from './repository/complaint.repository';
import { SlaService } from './sla.service';
import { CreateComplaintDto, ComplaintCommentDto } from './dto/complaint.dto';
import { ComplaintStatus } from './enums/complaint.enums';

@Injectable()
export class ComplaintService {
  constructor(
    private repository: ComplaintRepository,
    private slaService: SlaService
  ) {}

  async registerComplaint(userId: string, dto: CreateComplaintDto) {
    const slaDetails = this.slaService.calculateSla(dto.category);
    
    const complaint = await this.repository.createComplaint({
      userId,
      title: dto.title,
      description: dto.description,
      category: dto.category,
      priority: slaDetails.priority,
      bookingId: dto.bookingId,
    });

    // Fire Kafka event: complaint.created -> Triggers Notification Service
    return complaint;
  }

  async getComplaintForPassenger(id: string, userId: string) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');
    if (complaint.userId !== userId) throw new UnauthorizedException('Access denied');

    // Filter out internal comments before returning to passenger
    complaint.comments = complaint.comments.filter(c => !c.isInternal);
    return complaint;
  }

  async addComment(id: string, authorId: string, dto: ComplaintCommentDto) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');
    
    if (complaint.status === ComplaintStatus.CLOSED) {
      throw new BadRequestException('Cannot comment on a closed complaint');
    }

    return this.repository.addComment(id, authorId, dto.content, !!dto.isInternal);
  }

  async resolveComplaint(id: string) {
    const complaint = await this.repository.findById(id);
    if (!complaint) throw new NotFoundException('Complaint not found');

    if (complaint.status === ComplaintStatus.CLOSED) {
      throw new BadRequestException('Complaint is already closed');
    }

    return this.repository.updateStatus(id, ComplaintStatus.RESOLVED);
  }
}
