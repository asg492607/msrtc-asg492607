import os

structure = {
    'documents': {
        'html': ['documents.html', 'my-certificates.html', 'downloads.html', 'upload-documents.html', 'document-preview.html'],
        'css': ['documents.css'],
        'js': ['documents.js']
    },
    'notifications': {
        'html': ['notifications.html', 'messages.html', 'announcements.html', 'email-center.html', 'sms-history.html'],
        'css': ['notifications.css'],
        'js': ['notifications.js']
    },
    'advanced-reports': {
        'html': ['reports-dashboard.html', 'revenue-report.html', 'occupancy-report.html', 'fleet-report.html', 
                 'employee-report.html', 'parcel-report.html', 'complaint-report.html'],
        'css': ['reports.css'],
        'js': ['reports.js']
    },
    'smart-command': {
        'html': ['command-center.html', 'state-map.html', 'live-operations.html', 'alerts.html', 'incident-center.html'],
        'css': ['command.css'],
        'js': ['command.js']
    },
    'design-system': {
        'html': ['design-system.html', 'components.html', 'icons.html', 'typography.html', 'color-system.html'],
        'css': ['design.css'],
        'js': ['design.js']
    }
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | MSRTC</title>
  <link rel="stylesheet" href="css/{css_file}">
  <style>
    body {{ font-family: 'Outfit', sans-serif; background: #F8FAFC; color: #1E293B; margin: 0; padding: 0; display: flex; min-height: 100vh; }}
    .sidebar {{ width: 260px; background: #0F172A; color: white; display: flex; flex-direction: column; }}
    .brand {{ height: 70px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    .brand img {{ height: 35px; filter: brightness(0) invert(1); }}
    .nav-menu {{ padding: 20px 10px; display: flex; flex-direction: column; gap: 4px; flex: 1; }}
    .nav-item {{ padding: 12px 16px; color: #94A3B8; text-decoration: none; font-weight: 500; border-radius: 6px; }}
    .nav-item:hover, .nav-item.active {{ background: rgba(255,255,255,0.1); color: white; }}
    .main-content {{ flex: 1; padding: 30px; display: flex; flex-direction: column; gap: 24px; overflow-y: auto; }}
    .topbar {{ display: flex; justify-content: space-between; align-items: center; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  </style>
</head>
<body>

  <aside class="sidebar">
    <div class="brand"><img src="../msrtc_new_logo.png" alt="Logo"></div>
    <nav class="nav-menu">
      <a href="{html_file}" class="nav-item active">📄 {title}</a>
      <a href="../admin.html" class="nav-item" style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.1); border-radius: 0; padding-top: 15px;">⬅️ Admin Home</a>
    </nav>
  </aside>

  <main class="main-content">
    <div class="topbar">
      <h1 style="font-size: 20px; margin: 0;">{title}</h1>
    </div>
    <div class="card">
      <h2 style="margin-bottom: 15px;">{title} Content</h2>
      <p style="color: #64748B;">This is a generated placeholder for the enterprise {title} module.</p>
    </div>
  </main>

  <script src="js/{js_file}"></script>
</body>
</html>"""

for folder, contents in structure.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # css dir
    css_dir = os.path.join(folder, 'css')
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    for css_file in contents.get('css', []):
        open(os.path.join(css_dir, css_file), 'w').close()
        
    # js dir
    js_dir = os.path.join(folder, 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
    for js_file in contents.get('js', []):
        open(os.path.join(js_dir, js_file), 'w').close()
            
    # html files
    css_name = contents['css'][0] if contents.get('css') else ''
    js_name = contents['js'][0] if contents.get('js') else ''
    
    for html_file in contents.get('html', []):
        title = html_file.replace('.html', '').replace('-', ' ').title()
        content = html_template.format(title=title, css_file=css_name, js_file=js_name, html_file=html_file)
        with open(os.path.join(folder, html_file), 'w', encoding='utf-8') as f:
            f.write(content)

print("Phase 4 structure created successfully.")
