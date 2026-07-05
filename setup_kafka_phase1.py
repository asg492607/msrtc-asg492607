import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\kafka"
src_dir = os.path.join(base_dir, "src")

os.makedirs(base_dir, exist_ok=True)
os.makedirs(src_dir, exist_ok=True)

pkg_json = {
  "name": "@msrtc/kafka",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/microservices": "^10.0.0",
    "kafkajs": "^2.2.4",
    "uuid": "^9.0.0"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/uuid": "^9.0.0"
  }
}

with open(os.path.join(base_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)

tsconfig_json = {
  "compilerOptions": {
    "module": "commonjs",
    "declaration": True,
    "removeComments": True,
    "emitDecoratorMetadata": True,
    "experimentalDecorators": True,
    "allowSyntheticDefaultImports": True,
    "target": "es2021",
    "sourceMap": True,
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": True
  },
  "include": ["src/**/*"]
}

with open(os.path.join(base_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig_json, f, indent=2)


dirs = [
    "interfaces",
    "constants"
]

for d in dirs:
    os.makedirs(os.path.join(src_dir, d), exist_ok=True)

# 1. Interfaces
event_interface = """export interface EventEnvelope<T = any> {
  eventId: string;
  eventType: string;
  eventVersion: string;
  occurredAt: string;
  correlationId: string;
  producer: string;
  payload: T;
}

export interface PublishOptions {
  correlationId?: string;
  producer?: string;
  version?: string;
}
"""
with open(os.path.join(src_dir, "interfaces/event.interface.ts"), "w", encoding="utf-8") as f: f.write(event_interface)

# 2. Constants
topic_constants = """export const Topics = {
  BOOKING: 'booking.events',
  PAYMENT: 'payment.events',
  SEAT: 'seat.events',
  TICKET: 'ticket.events',
  GPS: 'gps.events',
  NOTIFICATION: 'notification.events',
  COMPLAINT: 'complaint.events',
  PASS: 'pass.events',
  PARCEL: 'parcel.events',
  CREW: 'crew.events',
  DEPOT: 'depot.events',
  MAINTENANCE: 'maintenance.events',
  FINANCE: 'finance.events',
  HQ: 'hq.events',
  AUDIT: 'audit.events',
};
"""
with open(os.path.join(src_dir, "constants/topics.ts"), "w", encoding="utf-8") as f: f.write(topic_constants)

print("Kafka Package Phase 1 Scaffolded (Interfaces, Constants, Configs)")
