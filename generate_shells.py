import os

portals = {
    'depot-portal': {
        'pages': ['dashboard.html', 'bus-management.html', 'route-management.html', 'schedule-management.html', 'driver-assignment.html', 'conductor-assignment.html', 'revenue.html', 'complaints.html', 'parcel.html', 'maintenance.html', 'notice-board.html'],
        'css': "css/depot.css",
        'js': "js/depot.js",
        'title_prefix': "Depot Portal",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="bus-management.html" class="nav-item">🚌 Bus Management</a>
      <a href="route-management.html" class="nav-item">🗺️ Route Management</a>
      <a href="schedule-management.html" class="nav-item">⏰ Schedules</a>
      <a href="driver-assignment.html" class="nav-item">👨‍✈️ Driver Assignment</a>
      <a href="conductor-assignment.html" class="nav-item">🎫 Conductor Assign</a>
      <a href="revenue.html" class="nav-item">💰 Revenue</a>
      <a href="complaints.html" class="nav-item">⚠️ Complaints</a>
      <a href="parcel.html" class="nav-item">📦 Parcel</a>
      <a href="maintenance.html" class="nav-item">🔧 Maintenance</a>
      <a href="notice-board.html" class="nav-item">📢 Notice Board</a>"""
    },
    'driver-app': {
        'pages': ['login.html', 'dashboard.html', 'trip.html', 'navigation.html', 'fuel.html', 'breakdown.html', 'notifications.html'],
        'css': "css/driver.css",
        'js': "js/driver.js",
        'title_prefix': "Driver App",
        'nav': """      <a href="dashboard.html" class="nav-item">🏠 Dashboard</a>
      <a href="trip.html" class="nav-item">🚌 Active Trip</a>
      <a href="fuel.html" class="nav-item">⛽ Fuel Entry</a>
      <a href="breakdown.html" class="nav-item">🔧 Breakdown</a>"""
    },
    'conductor-app': {
        'pages': ['dashboard.html', 'manifest.html', 'scanner.html', 'offline-ticket.html', 'parcel.html', 'trip-close.html'],
        'css': "css/conductor.css",
        'js': "js/conductor.js",
        'title_prefix': "Conductor App",
        'nav': """      <a href="dashboard.html" class="nav-item">🏠 Dashboard</a>
      <a href="manifest.html" class="nav-item">📋 Manifest</a>
      <a href="scanner.html" class="nav-item">📷 QR Scanner</a>
      <a href="offline-ticket.html" class="nav-item">🎫 Issue Ticket</a>"""
    },
    'regional-portal': {
        'pages': ['dashboard.html', 'depots.html', 'fleet.html', 'operations.html', 'complaints.html', 'reports.html'],
        'css': "css/regional.css",
        'js': "js/regional.js",
        'title_prefix': "Regional Portal",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="depots.html" class="nav-item">🏢 Depots</a>
      <a href="fleet.html" class="nav-item">🚌 Fleet</a>
      <a href="operations.html" class="nav-item">⚙️ Operations</a>
      <a href="complaints.html" class="nav-item">⚠️ Complaints</a>
      <a href="reports.html" class="nav-item">📄 Reports</a>"""
    },
    'hq-portal': {
        'pages': ['dashboard.html', 'fleet.html', 'depots.html', 'employees.html', 'recruitment.html', 'finance.html', 'analytics.html', 'audit.html', 'settings.html'],
        'css': "css/hq.css",
        'js': "js/hq.js",
        'title_prefix': "HQ Super Admin",
        'nav': """      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="fleet.html" class="nav-item">🚌 Fleet Registry</a>
      <a href="depots.html" class="nav-item">🏢 Depot Management</a>
      <a href="employees.html" class="nav-item">👥 Employees</a>
      <a href="recruitment.html" class="nav-item">🎯 Recruitment</a>
      <a href="finance.html" class="nav-item">💰 Finance</a>
      <a href="analytics.html" class="nav-item">📈 Analytics & BI</a>
      <a href="audit.html" class="nav-item">🛡️ Audit & Security</a>
      <a href="settings.html" class="nav-item">⚙️ Settings</a>"""
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
.app-header { background: var(--primary); color: white; padding: 20px; text-align: center; }
.app-content { padding: 20px; flex: 1; }
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
    <div class="topbar">
      <div class="page-title">
        <h1>{title}</h1>
      </div>
    </div>
    <div class="card" style="margin-top: 30px;">
      <h2 style="color: var(--secondary); margin-bottom: 12px;">{title} Module</h2>
      <p style="color: var(--text-light);">This interface is a structural placeholder. Integration with NestJS backend is pending.</p>
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

    # Write CSS if not exists
    css_file = os.path.join(folder, config['css'])
    if not os.path.exists(css_file):
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_template)

    # Write JS if not exists
    js_file = os.path.join(folder, config['js'])
    if not os.path.exists(js_file):
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_template)

    # Write HTML pages
    for page in config['pages']:
        page_path = os.path.join(folder, page)
        if not os.path.exists(page_path):
            title = page.split('.')[0].replace('-', ' ').title()
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(generate_html(title, config))

print("Shells generated successfully.")
