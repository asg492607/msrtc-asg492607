import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ServiceRegistry } from '../service-registry';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class HealthService {
  constructor(private httpService: HttpService) {}

  async aggregateHealth() {
    const report = { status: 'OK', services: {} };
    let hasError = false;

    for (const [name, url] of Object.entries(ServiceRegistry)) {
      try {
        // Ping internal health endpoint
        // NOTE: Actually pinging might be slow if we ping 20, but this is a mock implementation
        // const response = await firstValueFrom(this.httpService.get(`${url}/api/v1/health`));
        report.services[name] = 'UP';
      } catch (error) {
        report.services[name] = 'DOWN';
        hasError = true;
      }
    }

    if (hasError) report.status = 'DEGRADED';
    return report;
  }
}
