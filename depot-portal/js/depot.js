// depot.js

document.addEventListener('DOMContentLoaded', () => {
  // Sidebar active state matching
  const path = window.location.pathname;
  const navItems = document.querySelectorAll('.nav-item');
  
  // Set default active if root
  let found = false;
  navItems.forEach(item => {
    if (path.includes(item.getAttribute('href'))) {
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      found = true;
    }
  });
  if (!found && navItems.length > 0 && path.endsWith('/')) {
    navItems[0].classList.add('active');
  }

  // Load generic data if needed
  console.log("Depot Portal JS Initialized");
});

function handleLogout() {
  window.location.href = '../index.html';
}

function showToast(msg) {
  // Simple toast generator
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = 'position:fixed;bottom:20px;right:20px;background:var(--success);color:white;padding:12px 24px;border-radius:8px;z-index:1000;display:none;';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}
