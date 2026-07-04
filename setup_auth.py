import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend"

# Scaffold directories
directories = [
    "packages/database/src",
    "apps/auth-service/src/prisma",
    "apps/auth-service/src/auth/dto",
    "apps/auth-service/src/auth/guards",
    "apps/auth-service/src/auth/decorators",
    "apps/auth-service/src/auth/strategies"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. packages/database/package.json
db_pkg = """{
  "name": "@msrtc/database",
  "version": "1.0.0",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "dependencies": {
    "@prisma/client": "^5.0.0"
  }
}
"""
with open(os.path.join(base_dir, "packages/database/package.json"), "w") as f:
    f.write(db_pkg)

# 2. apps/auth-service/package.json
auth_pkg = """{
  "name": "auth-service",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch"
  },
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/jwt": "^10.0.0",
    "@nestjs/passport": "^10.0.0",
    "@nestjs/swagger": "^7.0.0",
    "@msrtc/database": "workspace:*",
    "argon2": "^0.31.0",
    "class-transformer": "^0.5.1",
    "class-validator": "^0.14.0",
    "passport": "^0.6.0",
    "passport-jwt": "^4.0.1",
    "reflect-metadata": "^0.1.13",
    "rxjs": "^7.8.1"
  }
}
"""
with open(os.path.join(base_dir, "apps/auth-service/package.json"), "w") as f:
    f.write(auth_pkg)

# 3. apps/auth-service/tsconfig.json
ts_config = """{
  "compilerOptions": {
    "module": "commonjs",
    "declaration": true,
    "removeComments": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true,
    "target": "es2021",
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": true,
    "skipLibCheck": true,
    "strictNullChecks": false,
    "noImplicitAny": false,
    "strictBindCallApply": false,
    "forceConsistentCasingInFileNames": false,
    "noFallthroughCasesInSwitch": false
  }
}
"""
with open(os.path.join(base_dir, "apps/auth-service/tsconfig.json"), "w") as f:
    f.write(ts_config)

# 4. apps/auth-service/src/main.ts
main_ts = """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setGlobalPrefix('api/v1/auth');

  const config = new DocumentBuilder()
    .setTitle('MSRTC Auth Service')
    .setDescription('The Authentication API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/auth', app, document);

  await app.listen(3001);
  console.log('Auth Service is running on http://localhost:3001');
}
bootstrap();
"""
with open(os.path.join(base_dir, "apps/auth-service/src/main.ts"), "w") as f:
    f.write(main_ts)

# 5. apps/auth-service/src/app.module.ts
app_mod = """import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [AuthModule, PrismaModule],
})
export class AppModule {}
"""
with open(os.path.join(base_dir, "apps/auth-service/src/app.module.ts"), "w") as f:
    f.write(app_mod)

print("Auth Service scaffold created.")
