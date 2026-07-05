import { Module, Global } from '@nestjs/common';
import { EventBusService } from './event-bus.service';
import { ConsumerService } from './consumer.service';

@Global()
@Module({
  providers: [EventBusService, ConsumerService],
  exports: [EventBusService, ConsumerService],
})
export class KafkaModule {}
