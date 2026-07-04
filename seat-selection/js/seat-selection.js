// seat-selection.js

const MAX_SEATS = 6;
let selectedSeats = [];

document.addEventListener('DOMContentLoaded', () => {
  loadSeatLayout(); // from seat-layout.js
  
  // Set summary route from local storage (if any)
  const from = localStorage.getItem('searchFrom') || 'Mumbai';
  const to = localStorage.getItem('searchTo') || 'Pune';
  const dateStr = localStorage.getItem('searchDate') || '2026-07-15';
  document.getElementById('summaryRoute').textContent = `${from} → ${to}`;
  document.getElementById('summaryDate').textContent = dateStr;
});

function initSeatSelection() {
  const seats = document.querySelectorAll('.seat:not(.booked)');
  
  seats.forEach(seat => {
    seat.addEventListener('click', () => {
      const seatId = seat.dataset.id;
      
      if (selectedSeats.includes(seatId)) {
        // Deselect
        selectedSeats = selectedSeats.filter(id => id !== seatId);
        seat.classList.remove('selected');
      } else {
        // Select
        if (selectedSeats.length >= MAX_SEATS) {
          showToast(`Maximum ${MAX_SEATS} seats can be selected`);
          return;
        }
        selectedSeats.push(seatId);
        seat.classList.add('selected');
      }
      
      updateChips();
      updateFareSummary(selectedSeats.length, window.seatData.baseFare);
    });
  });
}

function updateChips() {
  const container = document.getElementById('selectedChips');
  container.innerHTML = '';
  
  selectedSeats.forEach(id => {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.innerHTML = `${id} <span class="chip-close" onclick="removeSeat('${id}')">×</span>`;
    container.appendChild(chip);
  });
}

window.removeSeat = function(id) {
  selectedSeats = selectedSeats.filter(sId => sId !== id);
  const seatEl = document.querySelector(`.seat[data-id="${id}"]`);
  if (seatEl) {
    seatEl.classList.remove('selected');
  }
  updateChips();
  updateFareSummary(selectedSeats.length, window.seatData.baseFare);
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  if(!toast) return;
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

function continueToPassenger() {
  if (selectedSeats.length === 0) return;
  
  localStorage.setItem('selectedSeats', JSON.stringify(selectedSeats));
  localStorage.setItem('totalFare', document.getElementById('totalFare').textContent.replace('₹', ''));
  
  const toast = document.getElementById('toast');
  toast.textContent = 'Proceeding to Passenger Details...';
  toast.style.display = 'block';
  
  setTimeout(() => {
    window.location.href = '../passenger-details/passenger-details.html';
  }, 1000);
}
