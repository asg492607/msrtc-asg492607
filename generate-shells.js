const fs = require('fs');
const path = require('path');

const portals = {
  'depot-portal': {
    pages: ['bus-management.html', 'route-management.html', 'schedule-management.html', 'driver-assignment.html', 'conductor-assignment.html', 'revenue.html', 'complaints.html', 'parcel.html', 'maintenance.html', 'notice-board.html'],
    template: (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Depot Portal | ${title}</title>
  <link rel="stylesheet" href="css/depot.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand"><img src="../msrtc_new_logo.png" alt="MSRTC Logo"></div>
    <nav class="nav-menu">
      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="bus-management.html" class="nav-item">🚌 Bus Management</a>
      <a href="route-management.html" class="nav-item">🗺️ Route Management</a>
      <a href="schedule-management.html" class="nav-item">⏰ Schedules</a>
      <a href="driver-assignment.html" class="nav-item">👨‍✈️ Driver Assignment</a>
      <a href="conductor-assignment.html" class="nav-item">🎫 Conductor Assign</a>
      <a href="revenue.html" class="nav-item">💰 Revenue</a>
      <a href="complaints.html" class="nav-item">⚠️ Complaints</a>
      <a href="parcel.html" class="nav-item">📦 Parcel</a>
      <a href="maintenance.html" class="nav-item">🔧 Maintenance</a>
      <a href="notice-board.html" class="nav-item">📢 Notice Board</a>
    </nav>
  </aside>
  <main class="main-content">
    <div class="topbar">
      <div class="page-title">
        <h1>${title}</h1>
        <p>Swargate Depot Operations</p>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><div class="card-title">${title} Module</div></div>
      <p>This module is under construction. It will integrate with the NestJS backend.</p>
    </div>
  </main>
  <script src="js/depot.js"></script>
</body>
</html>`
  },
  'driver-app': {
    pages: ['login.html', 'dashboard.html', 'trip.html', 'navigation.html', 'fuel.html', 'breakdown.html', 'notifications.html'],
    template: (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Driver App | ${title}</title>
  <link rel="stylesheet" href="css/driver.css">
</head>
<body>
  <header class="app-header"><h1>${title}</h1></header>
  <main class="app-content">
    <div class="card">
      <h2>${title}</h2>
      <p>Module coming soon.</p>
      <button class="btn btn-primary" onclick="window.location.href='dashboard.html'">Back to Dashboard</button>
    </div>
  </main>
  <script src="js/driver.js"></script>
</body>
</html>`
  },
  'conductor-app': {
    pages: ['dashboard.html', 'manifest.html', 'scanner.html', 'offline-ticket.html', 'parcel.html', 'trip-close.html'],
    template: (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Conductor App | ${title}</title>
  <link rel="stylesheet" href="css/conductor.css">
</head>
<body>
  <header class="app-header"><h1>${title}</h1></header>
  <main class="app-content">
    <div class="card">
      <h2>${title}</h2>
      <p>Module coming soon.</p>
      <button class="btn btn-primary" onclick="window.location.href='dashboard.html'">Back to Dashboard</button>
    </div>
  </main>
  <script src="js/conductor.js"></script>
</body>
</html>`
  },
  'regional-portal': {
    pages: ['dashboard.html', 'depots.html', 'fleet.html', 'operations.html', 'complaints.html', 'reports.html'],
    template: (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Regional Portal | ${title}</title>
  <link rel="stylesheet" href="css/regional.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand"><img src="../msrtc_new_logo.png" alt="MSRTC Logo"></div>
    <nav class="nav-menu">
      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="depots.html" class="nav-item">🏢 Depots</a>
      <a href="fleet.html" class="nav-item">🚌 Fleet</a>
      <a href="operations.html" class="nav-item">⚙️ Operations</a>
      <a href="complaints.html" class="nav-item">⚠️ Complaints</a>
      <a href="reports.html" class="nav-item">📄 Reports</a>
    </nav>
  </aside>
  <main class="main-content">
    <div class="topbar">
      <div class="page-title"><h1>${title}</h1></div>
    </div>
    <div class="card"><p>Module coming soon.</p></div>
  </main>
  <script src="js/regional.js"></script>
</body>
</html>`
  },
  'hq-portal': {
    pages: ['dashboard.html', 'fleet.html', 'depots.html', 'employees.html', 'recruitment.html', 'finance.html', 'analytics.html', 'audit.html', 'settings.html'],
    template: (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HQ Super Admin | ${title}</title>
  <link rel="stylesheet" href="css/hq.css">
</head>
<body>
  <aside class="sidebar">
    <div class="brand"><img src="../msrtc_new_logo.png" alt="MSRTC Logo"></div>
    <nav class="nav-menu">
      <a href="dashboard.html" class="nav-item">📊 Dashboard</a>
      <a href="fleet.html" class="nav-item">🚌 Fleet Registry</a>
      <a href="depots.html" class="nav-item">🏢 Depot Management</a>
      <a href="employees.html" class="nav-item">👥 Employees</a>
      <a href="recruitment.html" class="nav-item">🎯 Recruitment</a>
      <a href="finance.html" class="nav-item">💰 Finance</a>
      <a href="analytics.html" class="nav-item">📈 Analytics & BI</a>
      <a href="audit.html" class="nav-item">🛡️ Audit & Security</a>
      <a href="settings.html" class="nav-item">⚙️ Settings</a>
    </nav>
  </aside>
  <main class="main-content">
    <div class="topbar">
      <div class="page-title"><h1>${title}</h1></div>
    </div>
    <div class="card"><p>Module coming soon.</p></div>
  </main>
  <script src="js/hq.js"></script>
</body>
</html>`
  }
};

for (const [folder, config] of Object.entries(portals)) {
  const dir = path.join(__dirname, folder);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  
  const cssDir = path.join(dir, 'css');
  const jsDir = path.join(dir, 'js');
  if (!fs.existsSync(cssDir)) fs.mkdirSync(cssDir);
  if (!fs.existsSync(jsDir)) fs.mkdirSync(jsDir);

  // Write dummy css and js if they don't exist
  const cssFile = path.join(cssDir, folder.split('-')[0] + '.css');
  if (!fs.existsSync(cssFile)) {
    // Just a basic copy of depot.css styling for structure
    fs.writeFileSync(cssFile, \`@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
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
\`);
  }

  const jsFile = path.join(jsDir, folder.split('-')[0] + '.js');
  if (!fs.existsSync(jsFile)) {
    fs.writeFileSync(jsFile, \`
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    if (path.includes(item.getAttribute('href'))) {
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    }
  });
});
\`);
  }

  // Write pages
  config.pages.forEach(page => {
    const filePath = path.join(dir, page);
    if (!fs.existsSync(filePath)) {
      const titleName = page.split('.')[0].split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
      fs.writeFileSync(filePath, config.template(titleName));
    }
  });
}
console.log("Shells generated successfully.");
