document.addEventListener('DOMContentLoaded', () => {
  // Sidebar active state
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    if (path.includes(item.getAttribute('href'))) {
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
    }
  });

  initCharts();
});

function initCharts() {
  const revCtx = document.getElementById('revenueTrendChart');
  if (revCtx) {
    new Chart(revCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Revenue (₹ Cr)',
          data: [18.2, 19.5, 21.0, 20.5, 23.1, 24.5],
          borderColor: '#FF6B00',
          backgroundColor: 'rgba(255,107,0,0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { borderDash: [5, 5] } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  const occCtx = document.getElementById('occupancyChart');
  if (occCtx) {
    new Chart(occCtx, {
      type: 'bar',
      data: {
        labels: ['Shivneri', 'Shivshahi', 'Hirkani', 'Ordinary', 'Sleeper'],
        datasets: [{
          label: 'Occupancy %',
          data: [88, 75, 82, 90, 85],
          backgroundColor: ['#0B3C5D', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { borderDash: [5, 5] } },
          x: { grid: { display: false } }
        }
      }
    });
  }
}
