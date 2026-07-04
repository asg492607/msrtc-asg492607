// search/js/autocomplete.js

const cities = [
  "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", 
  "Solapur", "Amravati", "Kolhapur", "Satara", "Jalgaon",
  "Thane", "Kalyan", "Navi Mumbai", "Latur", "Dhule"
];

function initAutocomplete(inputId, listId) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);

  input.addEventListener('input', function() {
    const val = this.value;
    list.innerHTML = '';
    if (!val) { list.style.display = 'none'; return; }
    
    let hasMatches = false;
    cities.forEach(city => {
      if (city.toLowerCase().includes(val.toLowerCase())) {
        hasMatches = true;
        const item = document.createElement('div');
        item.innerHTML = `📍 ${city}`;
        item.addEventListener('click', () => {
          input.value = city;
          list.style.display = 'none';
        });
        list.appendChild(item);
      }
    });

    if (hasMatches) {
      list.style.display = 'block';
    } else {
      list.style.display = 'none';
    }
  });

  // Hide list when clicking outside
  document.addEventListener('click', (e) => {
    if (e.target !== input && e.target !== list) {
      list.style.display = 'none';
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initAutocomplete('fromCity', 'fromList');
  initAutocomplete('toCity', 'toList');
});
