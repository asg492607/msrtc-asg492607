import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"

# 1. Master docker-compose.yml
docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: msrtc
      POSTGRES_PASSWORD: password
      POSTGRES_DB: msrtc_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U msrtc"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  api-gateway:
    build: 
      context: .
      args:
        SERVICE: api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - redis

  # Example of one microservice in the compose stack
  booking-service:
    build:
      context: .
      args:
        SERVICE: booking-service
    environment:
      - DATABASE_URL=postgresql://msrtc:password@postgres:5432/msrtc_db?schema=public
      - REDIS_HOST=redis
      - KAFKA_BROKERS=kafka:29092
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_started

volumes:
  postgres_data:
"""
with open(os.path.join(base_dir, "docker-compose.yml"), "w", encoding="utf-8") as f: f.write(docker_compose)


# 2. GitHub Actions CI/CD Pipeline
github_dir = os.path.join(base_dir, ".github/workflows")
os.makedirs(github_dir, exist_ok=True)

deploy_yml = """name: MSRTC CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci

    - name: Run Linter
      run: npx turbo run lint

    - name: Run Unit Tests
      run: npx turbo run test

  docker-build:
    needs: lint-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    # In a real pipeline, we would matrix this across all 20 services
    - name: Build API Gateway Docker Image
      run: |
        docker build --build-arg SERVICE=api-gateway -t msrtc/api-gateway:${{ github.sha }} .
        # docker push msrtc/api-gateway:${{ github.sha }}
"""
with open(os.path.join(github_dir, "deploy.yml"), "w", encoding="utf-8") as f: f.write(deploy_yml)


print("Task 25 Phase 2 Scaffolded (Docker Compose, CI/CD)")
