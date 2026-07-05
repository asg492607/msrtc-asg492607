import { Injectable, NotFoundException } from '@nestjs/common';
import { CrewRepository } from './repository/crew.repository';
import { CreateEmployeeDto } from './dto/crew.dto';

@Injectable()
export class CrewService {
  constructor(private repository: CrewRepository) {}

  async createProfile(dto: CreateEmployeeDto) {
    return this.repository.createEmployee(dto);
  }

  async getProfile(id: string) {
    const profile = await this.repository.findById(id);
    if (!profile) throw new NotFoundException('Crew not found');
    return profile;
  }
}
