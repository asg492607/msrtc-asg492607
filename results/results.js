// results/results.js

document.addEventListener('DOMContentLoaded', () => {
  loadSearchSummary();
  fetchBuses();
});

function loadSearchSummary() {
  const from = localStorage.getItem('searchFrom') || 'Mumbai';
  const to = localStorage.getItem('searchTo') || 'Pune';
  const dateStr = localStorage.getItem('searchDate') || new Date().toISOString().split('T')[0];
  
  const dateObj = new Date(dateStr);
  const options = { day: 'numeric', month: 'short' };
  const formattedDate = dateObj.toLocaleDateString('en-US', options);

  document.getElementById('summaryRoute').textContent = `${from} → ${to}`;
  document.getElementById('summaryDate').textContent = formattedDate;
}

const amenityIcons = {
  wifi: '📶', charging: '🔌', water: '💧', blanket: '🛌', gps: '📍', cctv: '📹', emergency_exit: '🚪'
};

async function fetchBuses() {
  try {
    const response = await fetch('buses.json');
    const buses = await response.json();
    renderBuses(buses);
    document.getElementById('busCount').textContent = `${buses.length} buses found`;
  } catch (error) {
    console.error("Error fetching buses:", error);
    document.getElementById('resultsContainer').innerHTML = '<p>Error loading buses.</p>';
  }
}

function renderBuses(buses) {
  const container = document.getElementById('resultsContainer');
  container.innerHTML = '';

  if (buses.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 40px;">
        <h2>No buses found</h2>
        <p>Try changing your search criteria</p>
      </div>`;
    return;
  }

  const from = localStorage.getItem('searchFrom') || 'Mumbai';
  const to = localStorage.getItem('searchTo') || 'Pune';

  buses.forEach(bus => {
    let iconsHtml = bus.amenities.map(a => `<span title="${a}">${amenityIcons[a] || '✨'}</span>`).join('');
    
    const card = document.createElement('div');
    card.className = 'bus-card';
    card.innerHTML = `
      <div class="bus-top">
        <div class="bus-info">
          <h4>${bus.name} <span class="rating">★ ${bus.rating}</span></h4>
          <div class="bus-number">${bus.number} | ${bus.type}</div>
        </div>
        <div class="fare">
          <div class="fare-amt">₹${bus.fare}</div>
          <div class="seats-left">${bus.seatsLeft} Seats Left</div>
        </div>
      </div>
      <div class="bus-middle">
        <div class="time-col">
          <div class="time">${bus.departure}</div>
          <div class="place">${from}</div>
        </div>
        <div class="duration">
          <span>${bus.duration}</span>
        </div>
        <div class="time-col">
          <div class="time">${bus.arrival}</div>
          <div class="place">${to}</div>
        </div>
      </div>
      <div class="bus-bottom">
        <div class="amenities">
          ${iconsHtml}
        </div>
        <button class="btn-book" onclick="bookBus(${bus.id})">Book Now</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function bookBus(busId) {
  // Save selected bus ID to localStorage to simulate passing data
  localStorage.setItem('selectedBusId', busId);
  window.location.href = '../bus-details/bus-details.html';
}
