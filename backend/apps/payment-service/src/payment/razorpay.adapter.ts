import { Injectable, NotImplementedException } from '@nestjs/common';
import { IPaymentGateway } from '../interfaces/gateway.interface';

@Injectable()
export class RazorpayAdapter implements IPaymentGateway {
  // In a real app, inject Razorpay SDK here

  async initiatePayment(amount: number, currency: string, receiptId: string): Promise<any> {
    // Mock Razorpay Order Creation
    return {
      id: `order_${Date.now()}`,
      amount: amount * 100, // Razorpay expects paise
      currency,
      receipt: receiptId,
      status: 'created'
    };
  }

  verifySignature(payload: any, signature: string, secret: string): boolean {
    // Mock signature verification (Normally uses crypto.createHmac)
    return true; 
  }

  async processRefund(paymentId: string, amount: number): Promise<any> {
    throw new NotImplementedException('Refunds not mocked yet');
  }
}
