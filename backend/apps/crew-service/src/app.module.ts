import { Module } from '@nestjs/common';
import { CrewModule } from './crew/crew.module';

@Module({
  imports: [CrewModule],
})
export class AppModule {}
