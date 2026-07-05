import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
tenant_dir = os.path.join(base_dir, "packages/tenant")
tenant_src = os.path.join(tenant_dir, "src")

# 1. Update schema.prisma
schema_path = os.path.join(base_dir, "packages/database/prisma/schema.prisma")
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        schema_content = f.read()
    
    # Check if Tenant model already exists
    if "model Tenant" not in schema_content:
        tenant_models = """
model Tenant {
  id          String   @id @default(uuid())
  name        String
  domain      String?  @unique
  config      Json?
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
}
"""
        schema_content += tenant_models
        with open(schema_path, "w") as f:
            f.write(schema_content)

os.makedirs(tenant_dir, exist_ok=True)
os.makedirs(tenant_src, exist_ok=True)

# 2. Package.json
pkg_json = {
  "name": "@msrtc/tenant",
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
    "nestjs-cls": "^3.5.0",
    "@prisma/client": "^5.0.0"
  },
  "devDependencies": {
    "typescript": "^5.1.3"
  }
}

with open(os.path.join(tenant_dir, "package.json"), "w", encoding="utf-8") as f:
    json.dump(pkg_json, f, indent=2)

tsconfig_json = {
  "compilerOptions": {
    "module": "commonjs",
    "declaration": True,
    "removeComments": True,
    "target": "es2021",
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": True,
    "experimentalDecorators": True,
    "emitDecoratorMetadata": True
  },
  "include": ["src/**/*"]
}
with open(os.path.join(tenant_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig_json, f, indent=2)

print("Tenant Package Phase 1 Scaffolded (Schema, Package)")
