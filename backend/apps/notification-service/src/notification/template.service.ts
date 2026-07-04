import { Injectable } from '@nestjs/common';

@Injectable()
export class TemplateService {
  private templates = {
    'booking.confirmed': {
      en: 'Dear {{name}}, your booking is confirmed. PNR: {{pnr}}.',
      mr: 'प्रिय {{name}}, तुमचे बुकिंग निश्चित झाले आहे. PNR: {{pnr}}.'
    }
  };

  compile(templateCode: string, lang: string, payload: any): string {
    const template = this.templates[templateCode]?.[lang] || this.templates[templateCode]?.['en'];
    if (!template) return 'Notification content unavailable.';

    return template.replace(/{{(.*?)}}/g, (_, key) => payload[key.trim()] || '');
  }
}
