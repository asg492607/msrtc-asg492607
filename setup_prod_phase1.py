import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
logger_dir = os.path.join(base_dir, "packages/logger")
logger_src = os.path.join(logger_dir, "src")

os.makedirs(logger_dir, exist_ok=True)
os.makedirs(logger_src, exist_ok=True)

# 1. Logger Package
pkg_json = {
  "name": "@msrtc/logger",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0"
  },
  "devDependencies": {
    "typescript": "^5.1.3"
  }
}

with open(os.path.join(logger_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)

tsconfig_json = {
  "compilerOptions": {
    "module": "commonjs",
    "declaration": True,
    "removeComments": True,
    "target": "es2021",
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": True
  },
  "include": ["src/**/*"]
}

with open(os.path.join(logger_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig_json, f, indent=2)

logger_ts = """import { ConsoleLogger, Injectable, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.TRANSIENT })
export class StructuredLogger extends ConsoleLogger {
  log(message: any, context?: string) {
    this.printLog('INFO', message, context);
  }

  error(message: any, trace?: string, context?: string) {
    this.printLog('ERROR', message, context, trace);
  }

  warn(message: any, context?: string) {
    this.printLog('WARN', message, context);
  }

  private printLog(level: string, message: any, context?: string, trace?: string) {
    const logObj = {
      timestamp: new Date().toISOString(),
      level,
      context: context || this.context,
      message,
      trace,
    };
    // In production, this output is piped into Loki/FluentBit
    console.log(JSON.stringify(logObj));
  }
}
"""
with open(os.path.join(logger_src, "logger.service.ts"), "w", encoding="utf-8") as f: f.write(logger_ts)

index_ts = """export * from './logger.service';
"""
with open(os.path.join(logger_src, "index.ts"), "w", encoding="utf-8") as f: f.write(index_ts)


# 2. Dockerfile (Monorepo root)
dockerfile = """# Stage 1: Base
FROM node:18-alpine AS base
# RUN npm install -g pnpm turbo

# Stage 2: Prune
FROM base AS pruner
WORKDIR /app
COPY . .
# ARG SERVICE
# RUN turbo prune --scope=${SERVICE} --docker

# Stage 3: Build
FROM base AS builder
WORKDIR /app
# Mocked out turbo build for simplicity in this artifact
COPY package.json ./
RUN npm install
COPY . .
# RUN turbo run build --filter=${SERVICE}

# Stage 4: Runner
FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app /app
# CMD node apps/${SERVICE}/dist/main.js
CMD ["npm", "run", "start"]
"""
with open(os.path.join(base_dir, "Dockerfile"), "w", encoding="utf-8") as f: f.write(dockerfile)

dockerignore = """node_modules
dist
.git
.turbo
*.md
"""
with open(os.path.join(base_dir, ".dockerignore"), "w", encoding="utf-8") as f: f.write(dockerignore)


print("Task 25 Phase 1 Scaffolded (Logger, Dockerfile)")
