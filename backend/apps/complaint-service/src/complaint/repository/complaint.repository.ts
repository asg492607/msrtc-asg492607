import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { ComplaintStatus, ComplaintPriority } from '../enums/complaint.enums';

@Injectable()
export class ComplaintRepository {
  constructor(private prisma: PrismaService) {}

  async createComplaint(data: any) {
    // Generate a reference number e.g. CMP-168923482
    const referenceId = `CMP-${Math.floor(Date.now() / 1000)}`;
    return this.prisma.complaint.create({
      data: {
        ...data,
        referenceId,
        status: ComplaintStatus.OPEN,
        priority: ComplaintPriority.MEDIUM, // Default, updated by SLA engine later
      }
    });
  }

  async findById(id: string) {
    return this.prisma.complaint.findUnique({
      where: { id },
      include: { comments: true }
    });
  }

  async updateStatus(id: string, status: ComplaintStatus) {
    return this.prisma.complaint.update({
      where: { id },
      data: { status }
    });
  }

  async addComment(complaintId: string, authorId: string, content: string, isInternal: boolean) {
    return this.prisma.complaintComment.create({
      data: { complaintId, authorId, content, isInternal }
    });
  }
}
