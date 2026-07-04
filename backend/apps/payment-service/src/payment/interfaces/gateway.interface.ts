export interface IPaymentGateway {
  initiatePayment(amount: number, currency: string, receiptId: string): Promise<any>;
  verifySignature(payload: any, signature: string, secret: string): boolean;
  processRefund(paymentId: string, amount: number): Promise<any>;
}
