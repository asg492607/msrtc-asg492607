export interface INotificationProvider {
  send(to: string, content: string, subject?: string): Promise<boolean>;
}
