import { Module } from '@nestjs/common';
import { MasterDataModule } from './master-data/master-data.module';

@Module({
  imports: [MasterDataModule],
})
export class AppModule {}
