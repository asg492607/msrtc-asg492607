const fs = require('fs');
const path = require('path');

const files = [
  'src/app/booking/passenger/page.tsx',
  'src/app/booking/payment/page.tsx',
  'src/app/booking/seats/page.tsx',
  'src/app/search/page.tsx',
  'src/app/tracking/page.tsx'
];

for (const relPath of files) {
  const filePath = path.join(__dirname, relPath);
  let content = fs.readFileSync(filePath, 'utf8');

  // Skip if already has Suspense wrapper
  if (content.includes('<Suspense')) {
    console.log(`Skipping ${relPath} (already has Suspense)`);
    continue;
  }

  // Find export default function Name()
  const match = content.match(/export default function (\w+)\(\)/);
  if (!match) {
    console.log(`Could not find export default in ${relPath}`);
    continue;
  }
  
  const funcName = match[1];
  
  // Replace export default function with function Content
  content = content.replace(`export default function ${funcName}()`, `function ${funcName}Content()`);
  
  // Add import { Suspense } from 'react'; after 'use client';
  if (!content.includes('import { Suspense }')) {
    content = content.replace(/'use client';\r?\n/, `'use client';\nimport { Suspense } from 'react';\n`);
  }
  
  // Append wrapper at the bottom
  content += `\nexport default function ${funcName}() {\n  return (\n    <Suspense fallback={<div style={{padding: '2rem'}}>Loading...</div>}>\n      <${funcName}Content />\n    </Suspense>\n  );\n}\n`;

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Fixed ${relPath}`);
}
