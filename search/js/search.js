// search/js/search.js

document.addEventListener("DOMContentLoaded", () => {
  // Swap button logic
  const swapBtn = document.getElementById('swapBtn');
  if (swapBtn) {
    swapBtn.addEventListener('click', () => {
      const fromInput = document.getElementById('fromCity');
      const toInput = document.getElementById('toCity');
      const temp = fromInput.value;
      fromInput.value = toInput.value;
      toInput.value = temp;
    });
  }

  // Search button logic
  const searchBtn = document.getElementById('searchBtn');
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const from = document.getElementById('fromCity').value;
      const to = document.getElementById('toCity').value;
      const date = document.getElementById('journeyDate').value;
      
      if (validateSearch(from, to, date)) {
        // Save to local storage to show in results page
        localStorage.setItem('searchFrom', from);
        localStorage.setItem('searchTo', to);
        localStorage.setItem('searchDate', date);
        
        searchBtn.innerHTML = 'Searching...';
        setTimeout(() => {
          window.location.href = '../results/search-results.html';
        }, 800);
      }
    });
  }

  // Popular routes click logic
  const routeCards = document.querySelectorAll('.card');
  routeCards.forEach(card => {
    card.addEventListener('click', function() {
      const title = this.querySelector('.card-title').textContent;
      if (title.includes('→')) {
        const parts = title.split('→');
        document.getElementById('fromCity').value = parts[0].trim();
        document.getElementById('toCity').value = parts[1].trim();
        
        // Auto select tomorrow's date
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        document.getElementById('journeyDate').value = tomorrow.toISOString().split('T')[0];
        
        showToast("Route selected! Click Search.");
      }
    });
  });
});
