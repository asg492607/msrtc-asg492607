import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
resilience_dir = os.path.join(base_dir, "packages/resilience")
resilience_src = os.path.join(resilience_dir, "src")

os.makedirs(resilience_dir, exist_ok=True)
os.makedirs(resilience_src, exist_ok=True)
os.makedirs(os.path.join(resilience_src, "decorators"), exist_ok=True)

# 1. Package.json
pkg_json = {
  "name": "@msrtc/resilience",
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
    "opossum": "^7.1.0",
    "rxjs": "^7.8.1"
  },
  "devDependencies": {
    "typescript": "^5.1.3",
    "@types/opossum": "^6.2.1"
  }
}

with open(os.path.join(resilience_dir, "package.json"), "w", encoding="utf-8") as f:
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
with open(os.path.join(resilience_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
    json.dump(tsconfig_json, f, indent=2)

print("Resilience Package Phase 1 Scaffolded (Package)")
