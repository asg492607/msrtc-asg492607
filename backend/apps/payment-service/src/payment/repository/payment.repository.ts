import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { PaymentStatus } from '../enums/payment.enums';

@Injectable()
export class PaymentRepository {
  constructor(private prisma: PrismaService) {}

  async createPaymentTransaction(bookingId: string, amount: number, gateway: string, transactionId: string) {
    // Interactive Transaction to create payment and its initial log
    return this.prisma.$transaction(async (tx) => {
      const payment = await tx.payment.create({
        data: {
          bookingId,
          amount,
          status: PaymentStatus.CREATED,
          transactionId,
          gateway,
        }
      });

      await tx.paymentLog.create({
        data: {
          paymentId: payment.id,
          status: PaymentStatus.CREATED,
          message: `Payment initiated via ${gateway}`
        }
      });

      return payment;
    });
  }

  async updatePaymentStatus(paymentId: string, status: PaymentStatus, transactionId?: string) {
    return this.prisma.$transaction(async (tx) => {
      const payment = await tx.payment.update({
        where: { id: paymentId },
        data: { status, transactionId }
      });

      await tx.paymentLog.create({
        data: {
          paymentId,
          status,
          message: `Status updated to ${status}`
        }
      });

      return payment;
    });
  }

  async findPaymentById(id: string) {
    return this.prisma.payment.findUnique({ where: { id } });
  }
}
