import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\packages\redis"
src_dir = os.path.join(base_dir, "src")

os.makedirs(base_dir, exist_ok=True)
os.makedirs(src_dir, exist_ok=True)

pkg_json = {
  "name": "@msrtc/redis",
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
    "ioredis": "^5.3.2",
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

# 1. Constants (Keys)
redis_keys = """export const CacheKeys = {
  AUTH_OTP: (mobile: string) => `auth:otp:${mobile}`,
  AUTH_REFRESH: (userId: string) => `auth:refresh:${userId}`,
  BOOKING_SEARCH: (hash: string) => `booking:search:${hash}`,
  SEAT_LOCK: (tripId: string, seatNo: string) => `seat:lock:${tripId}:${seatNo}`,
  GPS_BUS: (vehicleId: string) => `gps:bus:${vehicleId}`,
  HQ_KPI_TODAY: 'hq:kpi:today',
  FINANCE_SUMMARY: (date: string) => `finance:summary:${date}`,
  NOTIFICATION_RATE: (userId: string) => `notification:rate:${userId}`,
};
"""
with open(os.path.join(src_dir, "constants/keys.ts"), "w", encoding="utf-8") as f: f.write(redis_keys)


print("Redis Package Phase 1 Scaffolded (Package.json, Keys)")
