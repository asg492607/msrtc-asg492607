# Secure Development Guide

## 1. Credentials & Secrets
* **NEVER** hardcode AWS Keys, Database Passwords, or JWT Secrets in the source code.
* Use environment variables mapped via Terraform/Kubernetes ConfigMaps.
* Our CI/CD pipeline runs `TruffleHog`; any committed secret will instantly fail the build.

## 2. Dependency Management
* Run `npm audit` locally before committing.
* Do not use outdated packages. `Snyk` checks run on every PR.
* Only pull Docker base images from official verified publishers.

## 3. Data Validation
* Always use `@nestjs/class-validator` DTOs.
* Never trust incoming JSON structures without validation to prevent NoSQL/SQL injection attacks.
