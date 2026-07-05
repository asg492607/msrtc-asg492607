import { Injectable } from '@nestjs/common';

@Injectable()
export class ExportService {
  generateCsv(data: any[]): Buffer {
    if (!data || data.length === 0) return Buffer.from('');
    
    // Extract headers
    const headers = Object.keys(data[0]).join(',');
    
    // Map rows
    const rows = data.map(row => 
      Object.values(row)
        .map(value => `"${String(value).replace(/"/g, '""')}"`)
        .join(',')
    );

    const csvContent = [headers, ...rows].join('\n');
    return Buffer.from(csvContent, 'utf-8');
  }
}
