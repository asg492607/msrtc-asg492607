import { Controller, Get } from '@nestjs/common';
import axios from 'axios';

@Controller('swagger-json')
export class SwaggerAggregatorController {
  
  @Get()
  async getAggregatedSwagger() {
    // In production, these would be fetched from internal Docker DNS names
    const services = [
      { name: 'Auth', url: 'http://localhost:3001/api/docs/auth-json' },
      { name: 'Booking', url: 'http://localhost:3002/api/docs/bookings-json' }
    ];

    const aggregated = {
      openapi: '3.0.0',
      info: { title: 'MSRTC Enterprise API Gateway', version: '1.0.0' },
      paths: {},
      components: { schemas: {} }
    };

    for (const s of services) {
      try {
        const res = await axios.get(s.url);
        // Merge paths
        for (const [path, methods] of Object.entries(res.data.paths || {})) {
           aggregated.paths[path] = methods;
        }
        // Merge schemas
        for (const [schema, def] of Object.entries(res.data.components?.schemas || {})) {
           aggregated.components.schemas[schema] = def;
        }
      } catch (e) {
        console.error(`Failed to fetch swagger from ${s.name}: ${e.message}`);
      }
    }

    return aggregated;
  }
}
