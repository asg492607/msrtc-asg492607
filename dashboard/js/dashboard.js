// dashboard.js

document.addEventListener('DOMContentLoaded', () => {
  // Highlight active sidebar item
  const path = window.location.pathname;
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    if (path.includes(item.getAttribute('href'))) {
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    }
  });

  // Handle Tabs if they exist
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tab-content');
  
  if (tabs.length > 0) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.style.display = 'none');
        
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).style.display = 'block';
      });
    });
  }

  // Load upcoming journey data from local storage if on main dashboard
  const upcomingCard = document.getElementById('upcomingJourney');
  if (upcomingCard) {
    const pnr = localStorage.getItem('pnr');
    const from = localStorage.getItem('searchFrom');
    const to = localStorage.getItem('searchTo');
    const date = localStorage.getItem('searchDate');
    
    if (pnr) {
      upcomingCard.innerHTML = `
        <div class="ticket-card">
          <div>
            <div class="tkt-route">${from} → ${to}</div>
            <div class="tkt-meta">
              <span>📅 ${date}</span>
              <span>🎫 PNR: ${pnr}</span>
            </div>
          </div>
          <div class="tkt-actions">
            <span class="status-badge status-upcoming">Upcoming</span>
          </div>
        </div>
      `;
    } else {
      upcomingCard.innerHTML = `<p style="color: var(--text-light); text-align: center; padding: 20px;">No upcoming journeys.</p>`;
    }
  }
});

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

function handleLogout() {
  localStorage.clear();
  window.location.href = '../index.html';
}

function saveProfile(e) {
  e.preventDefault();
  showToast("Profile updated successfully!");
}
