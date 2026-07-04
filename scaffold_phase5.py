import os
import json

root_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"

# 1. Manifest
manifest = {
    "name": "MSRTC Smart Digital Platform",
    "short_name": "MSRTC App",
    "description": "Unified Digital Mobility Platform for Maharashtra.",
    "start_url": "/index.html",
    "display": "standalone",
    "background_color": "#F4F7FE",
    "theme_color": "#FF6B00",
    "icons": [
        {
            "src": "msrtc_new_logo.png",
            "sizes": "192x192",
            "type": "image/png"
        }
    ]
}
with open(os.path.join(root_dir, 'manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=2)

# 2. Service Worker
sw_content = """const CACHE_NAME = 'msrtc-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  '/msrtc_new_logo.png',
  '/offline.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) return response;
        return fetch(event.request).catch(() => caches.match('/offline.html'));
      })
  );
});
"""
with open(os.path.join(root_dir, 'service-worker.js'), 'w') as f:
    f.write(sw_content)

# 3. Scaffold Folders & HTML
structure = {
    'pwa': ['offline-ticket.html', 'offline-schedule.html', 'install-guide.html'],
    'errors': ['404.html', '500.html', 'no-internet.html', 'empty.html', 'maintenance.html'],
    'settings': ['general.html', 'theme.html', 'notifications.html', 'language.html', 'privacy.html', 'security.html'],
    'presentation-mode': ['executive-demo.html', 'tour.html', 'architecture.html']
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | MSRTC</title>
  <style>
    body {{ font-family: 'Outfit', sans-serif; background: #F8FAFC; color: #1E293B; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center; }}
    h1 {{ color: #0B3C5D; font-size: 32px; margin-bottom: 10px; }}
    p {{ color: #64748B; max-width: 500px; margin-bottom: 30px; line-height: 1.6; }}
    .btn {{ padding: 12px 24px; background: #FF6B00; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; box-shadow: 0 4px 10px rgba(255,107,0,0.3); }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>This is a scaffolded page for the final {title} feature.</p>
  <a href="../admin.html" class="btn">Return to Admin Home</a>
</body>
</html>"""

# Offline root
with open(os.path.join(root_dir, 'offline.html'), 'w', encoding='utf-8') as f:
    f.write(html_template.format(title='No Internet Connection'))

for folder, files in structure.items():
    folder_path = os.path.join(root_dir, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for file in files:
        title = file.replace('.html', '').replace('-', ' ').title()
        with open(os.path.join(folder_path, file), 'w', encoding='utf-8') as f:
            f.write(html_template.format(title=title))

# 4. Demo Data & Documentation
with open(os.path.join(root_dir, 'demo-data.js'), 'w') as f:
    f.write("const DEMO_DATA = { buses: [], routes: [], users: [] };\n// Massive simulated dataset goes here")

with open(os.path.join(root_dir, 'handoff.md'), 'w') as f:
    f.write("# MSRTC Frontend Developer Handoff\n\nThis document outlines the architecture for the backend integration team.")

with open(os.path.join(root_dir, 'style-guide.md'), 'w') as f:
    f.write("# MSRTC UI Style Guide\n\nRefer to `design-system.html` for live components.")

print("Phase 5 structure created successfully.")
