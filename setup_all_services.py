import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\backend\apps"

services = [
    {"dir": "master-data-service", "name": "master-data", "port": 3002},
    {"dir": "fleet-service", "name": "fleet", "port": 3003},
    {"dir": "route-service", "name": "route", "port": 3004},
    {"dir": "booking-service", "name": "booking", "port": 3005},
    {"dir": "seat-service", "name": "seat", "port": 3006},
    {"dir": "payment-service", "name": "payment", "port": 3007},
    {"dir": "ticket-service", "name": "ticket", "port": 3008},
    {"dir": "passenger-service", "name": "passenger", "port": 3009},
    {"dir": "gps-service", "name": "gps", "port": 3010},
    {"dir": "notification-service", "name": "notification", "port": 3011},
    {"dir": "complaint-service", "name": "complaint", "port": 3012},
    {"dir": "pass-service", "name": "pass", "port": 3013},
    {"dir": "parcel-service", "name": "parcel", "port": 3014},
    {"dir": "crew-service", "name": "crew", "port": 3015},
    {"dir": "depot-service", "name": "depot", "port": 3016},
    {"dir": "maintenance-service", "name": "maintenance", "port": 3017},
    {"dir": "finance-service", "name": "finance", "port": 3018},
    {"dir": "hq-service", "name": "hq", "port": 3019}
]

def title_case(s):
    return ''.join(word.capitalize() for word in s.split('-'))

for svc in services:
    svc_dir = os.path.join(base_dir, svc["dir"])
    src_dir = os.path.join(svc_dir, "src")
    feature_dir = os.path.join(src_dir, svc["name"])
    
    os.makedirs(feature_dir, exist_ok=True)
    
    # 1. package.json
    pkg = f"""{{
  "name": "{svc['dir']}",
  "version": "1.0.0",
  "private": true,
  "scripts": {{
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch"
  }},
  "dependencies": {{
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/swagger": "^7.0.0",
    "@msrtc/database": "workspace:*"
  }}
}}
"""
    with open(os.path.join(svc_dir, "package.json"), "w") as f: f.write(pkg)
    
    # 2. tsconfig.json
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
    "strictNullChecks": false,
    "noImplicitAny": false
  }
}
"""
    with open(os.path.join(svc_dir, "tsconfig.json"), "w") as f: f.write(ts_config)
    
    # 3. main.ts
    main_ts = f"""import {{ NestFactory }} from '@nestjs/core';
import {{ AppModule }} from './app.module';
import {{ ValidationPipe }} from '@nestjs/common';
import {{ DocumentBuilder, SwaggerModule }} from '@nestjs/swagger';

async function bootstrap() {{
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({{ whitelist: true, transform: true }}));
  app.setGlobalPrefix('api/v1/{svc['name']}');

  const config = new DocumentBuilder()
    .setTitle('MSRTC {title_case(svc['name'])} Service')
    .setDescription('The {title_case(svc['name'])} API for MSRTC Platform')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs/{svc['name']}', app, document);

  await app.listen({svc['port']});
  console.log('{title_case(svc['name'])} Service is running on http://localhost:{svc['port']}');
}}
bootstrap();
"""
    with open(os.path.join(src_dir, "main.ts"), "w") as f: f.write(main_ts)

    # 4. app.module.ts
    app_module = f"""import {{ Module }} from '@nestjs/common';
import {{ {title_case(svc['name'])}Module }} from './{svc['name']}/{svc['name']}.module';

@Module({{
  imports: [{title_case(svc['name'])}Module],
}})
export class AppModule {{}}
"""
    with open(os.path.join(src_dir, "app.module.ts"), "w") as f: f.write(app_module)
    
    # 5. feature.module.ts
    feat_module = f"""import {{ Module }} from '@nestjs/common';
import {{ {title_case(svc['name'])}Service }} from './{svc['name']}.service';
import {{ {title_case(svc['name'])}Controller }} from './{svc['name']}.controller';

@Module({{
  controllers: [{title_case(svc['name'])}Controller],
  providers: [{title_case(svc['name'])}Service],
}})
export class {title_case(svc['name'])}Module {{}}
"""
    with open(os.path.join(feature_dir, f"{svc['name']}.module.ts"), "w") as f: f.write(feat_module)
    
    # 6. feature.service.ts
    feat_service = f"""import {{ Injectable }} from '@nestjs/common';

@Injectable()
export class {title_case(svc['name'])}Service {{
  getHello(): string {{
    return 'Hello from {title_case(svc['name'])} Service!';
  }}
}}
"""
    with open(os.path.join(feature_dir, f"{svc['name']}.service.ts"), "w") as f: f.write(feat_service)
    
    # 7. feature.controller.ts
    feat_controller = f"""import {{ Controller, Get }} from '@nestjs/common';
import {{ {title_case(svc['name'])}Service }} from './{svc['name']}.service';
import {{ ApiTags, ApiOperation }} from '@nestjs/swagger';

@ApiTags('{title_case(svc['name'])}')
@Controller()
export class {title_case(svc['name'])}Controller {{
  constructor(private readonly service: {title_case(svc['name'])}Service) {{}}

  @Get()
  @ApiOperation({{ summary: 'Health check endpoint' }})
  getHello(): string {{
    return this.service.getHello();
  }}
}}
"""
    with open(os.path.join(feature_dir, f"{svc['name']}.controller.ts"), "w") as f: f.write(feat_controller)

print("Massive code generation complete!")
