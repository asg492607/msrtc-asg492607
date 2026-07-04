import os

portals = {
    'workshop-portal': {
        'pages': ['dashboard.html', 'vehicle-queue.html', 'job-cards.html', 'preventive-maintenance.html', 'breakdowns.html', 'inspections.html', 'spare-parts.html', 'inventory.html', 'mechanics.html', 'reports.html', 'settings.html'],
        'css': "css/workshop.css",
        'js': "js/workshop.js",
        'title_prefix': "Workshop Portal",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="vehicle-queue.html" class="nav-item">🚌 Vehicle Queue</a>
      <a href="job-cards.html" class="nav-item">📋 Job Cards</a>
      <a href="preventive-maintenance.html" class="nav-item">🔧 Preventive Maint.</a>
      <a href="breakdowns.html" class="nav-item">⚠️ Breakdowns</a>
      <a href="inspections.html" class="nav-item">🔍 Inspections</a>
      <a href="spare-parts.html" class="nav-item">⚙️ Spare Parts</a>
      <a href="mechanics.html" class="nav-item">👨‍🔧 Mechanics</a>
      <a href="reports.html" class="nav-item">📄 Reports</a>"""
    },
    'vendor-portal': {
        'pages': ['dashboard.html', 'vendors.html', 'tenders.html', 'purchase-orders.html', 'quotations.html', 'contracts.html', 'invoices.html', 'warehouse.html', 'inventory.html', 'payments.html', 'reports.html'],
        'css': "css/vendor.css",
        'js': "js/vendor.js",
        'title_prefix': "Vendor & Procurement",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="vendors.html" class="nav-item">🏢 Vendors</a>
      <a href="tenders.html" class="nav-item">📄 Tenders</a>
      <a href="purchase-orders.html" class="nav-item">🛒 Purchase Orders</a>
      <a href="contracts.html" class="nav-item">📜 Contracts</a>
      <a href="invoices.html" class="nav-item">🧾 Invoices</a>
      <a href="warehouse.html" class="nav-item">🏭 Warehouse</a>
      <a href="payments.html" class="nav-item">💳 Payments</a>"""
    },
    'ai-platform': {
        'pages': ['chatbot.html', 'citizen-ai.html', 'employee-ai.html', 'executive-ai.html', 'ai-settings.html'],
        'css': "css/ai.css",
        'js': "js/ai.js",
        'title_prefix': "AI Assistant",
        'nav': """      <a href="citizen-ai.html" class="nav-item">👨‍👩‍👧‍👦 Citizen AI</a>
      <a href="employee-ai.html" class="nav-item">👨‍💼 Employee AI</a>
      <a href="executive-ai.html" class="nav-item">📈 Executive AI</a>
      <a href="chatbot.html" class="nav-item">💬 Chat Widget Demo</a>
      <a href="ai-settings.html" class="nav-item">⚙️ Settings</a>"""
    },
    'command-center': {
        'pages': ['dashboard.html', 'live-map.html', 'fleet.html', 'delays.html', 'emergencies.html', 'occupancy.html', 'analytics.html', 'alerts.html'],
        'css': "css/command.css",
        'js': "js/command.js",
        'title_prefix': "Command Center",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Overview</a>
      <a href="live-map.html" class="nav-item">🗺️ Live Map</a>
      <a href="fleet.html" class="nav-item">🚌 Fleet Tracking</a>
      <a href="delays.html" class="nav-item">⏳ Delay Mgmt</a>
      <a href="emergencies.html" class="nav-item">🚨 Emergencies</a>
      <a href="occupancy.html" class="nav-item">👥 Occupancy Map</a>
      <a href="analytics.html" class="nav-item">📈 Analytics</a>"""
    }
}

css_template = """@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
:root { --primary: #FF6B00; --secondary: #0B3C5D; --bg-color: #F4F7FE; --card-bg: #FFFFFF; --text-dark: #2B3674; --text-light: #A3AED0; --border: #E0E5F2; --sidebar-w: 280px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Poppins', sans-serif; background-color: var(--bg-color); color: var(--text-dark); display: flex; min-height: 100vh; }
.sidebar { width: var(--sidebar-w); background: var(--card-bg); border-right: 1px solid var(--border); display: flex; flex-direction: column; }
.brand { height: 80px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--border); }
.brand img { height: 40px; }
.nav-menu { padding: 20px; display: flex; flex-direction: column; gap: 8px; }
.nav-item { padding: 12px 16px; text-decoration: none; color: var(--text-light); font-weight: 500; border-radius: 8px; }
.nav-item.active { background: var(--primary); color: white; }
.main-content { flex: 1; padding: 30px; }
.card { background: var(--card-bg); padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.btn { padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-family: 'Poppins', sans-serif; font-weight: 600; }
.btn-primary { background: var(--primary); color: white; }
"""

js_template = """document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    if (path.includes(item.getAttribute('href'))) {
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    }
  });
});
"""

def generate_html(title, config):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{config['title_prefix']} | {title}</title>
  <link rel="stylesheet" href="{config['css']}">
</head>
<body>
  <aside class="sidebar">
    <div class="brand"><img src="../msrtc_new_logo.png" alt="MSRTC Logo" style="height: 40px;"></div>
    <nav class="nav-menu">
{config['nav']}
    </nav>
  </aside>
  <main class="main-content">
    <div class="topbar" style="margin-bottom: 30px;">
      <div class="page-title">
        <h1 style="font-size: 28px; color: var(--secondary);">{title}</h1>
      </div>
    </div>
    <div class="card">
      <h2 style="color: var(--secondary); margin-bottom: 12px;">{title} Module</h2>
      <p style="color: var(--text-light);">This enterprise interface is a structural placeholder. Integration with NestJS backend is pending.</p>
      
      <!-- Back to Presentation Launcher -->
      <button class="btn btn-primary" style="margin-top: 24px;" onclick="window.location.href='../integration/launcher.html'">Return to Central Launcher</button>
    </div>
  </main>
  <script src="{config['js']}"></script>
</body>
</html>"""

for folder, config in portals.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    css_dir = os.path.join(folder, 'css')
    js_dir = os.path.join(folder, 'js')
    
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)

    css_file = os.path.join(folder, config['css'])
    if not os.path.exists(css_file):
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_template)

    js_file = os.path.join(folder, config['js'])
    if not os.path.exists(js_file):
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_template)

    for page in config['pages']:
        page_path = os.path.join(folder, page)
        if not os.path.exists(page_path):
            title = page.split('.')[0].replace('-', ' ').title()
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(generate_html(title, config))

print("Enterprise Shells generated successfully.")
