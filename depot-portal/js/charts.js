// charts.js - Handles Chart.js initialization for dummy data

document.addEventListener('DOMContentLoaded', () => {
  initRevenueChart();
  initOccupancyChart();
});

function initRevenueChart() {
  const ctx = document.getElementById('revenueChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Revenue (₹)',
        data: [120000, 150000, 140000, 180000, 220000, 280000, 260000],
        backgroundColor: '#FF6B00',
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, grid: { borderDash: [5, 5] } },
        x: { grid: { display: false } }
      }
    }
  });
}

function initOccupancyChart() {
  const ctx = document.getElementById('occupancyChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Occupancy %',
        data: [65, 70, 68, 75, 85, 95, 92],
        borderColor: '#0B3C5D',
        backgroundColor: 'rgba(11, 60, 93, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, max: 100, grid: { borderDash: [5, 5] } },
        x: { grid: { display: false } }
      }
    }
  });
}
