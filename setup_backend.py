import os
import json

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend"

directories = [
    "apps/api-gateway",
    "apps/auth-service",
    "apps/master-data-service",
    "apps/fleet-service",
    "apps/route-service",
    "packages/shared",
    "packages/config",
    "packages/database",
    "packages/types",
    "packages/utils",
    "docker",
    "kubernetes",
    "scripts",
    "docs"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. pnpm-workspace.yaml
with open(os.path.join(base_dir, "pnpm-workspace.yaml"), "w") as f:
    f.write("packages:\n  - 'apps/*'\n  - 'packages/*'\n")

# 2. package.json (root)
package_json = {
    "name": "msrtc-backend",
    "version": "1.0.0",
    "private": True,
    "scripts": {
        "build": "turbo run build",
        "dev": "turbo run dev",
        "lint": "turbo run lint",
        "format": "prettier --write \"**/*.{ts,tsx,md}\"",
        "prepare": "husky install",
        "docker:up": "docker-compose -f docker/docker-compose.yml up -d",
        "docker:down": "docker-compose -f docker/docker-compose.yml down"
    },
    "devDependencies": {
        "turbo": "^2.0.0",
        "husky": "^9.0.0",
        "prettier": "^3.0.0",
        "eslint": "^8.0.0"
    }
}
with open(os.path.join(base_dir, "package.json"), "w") as f:
    json.dump(package_json, f, indent=2)

# 3. turbo.json
turbo_json = {
    "$schema": "https://turbo.build/schema.json",
    "pipeline": {
        "build": {
            "dependsOn": ["^build"],
            "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
        },
        "dev": {
            "cache": False,
            "persistent": True
        },
        "lint": {}
    }
}
with open(os.path.join(base_dir, "turbo.json"), "w") as f:
    json.dump(turbo_json, f, indent=2)

# 4. docker-compose.yml
docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: msrtc_postgres
    restart: always
    environment:
      POSTGRES_USER: msrtc_user
      POSTGRES_PASSWORD: msrtc_password
      POSTGRES_DB: msrtc_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - msrtc_network

  redis:
    image: redis:7-alpine
    container_name: msrtc_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - msrtc_network

  pgadmin:
    image: dpage/pgadmin4
    container_name: msrtc_pgadmin
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@msrtc.gov.in
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    networks:
      - msrtc_network

volumes:
  postgres_data:
  redis_data:

networks:
  msrtc_network:
    driver: bridge
"""
with open(os.path.join(base_dir, "docker", "docker-compose.yml"), "w") as f:
    f.write(docker_compose)

print("Backend workspace initialized.")
