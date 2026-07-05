# Stage 1: Base
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
