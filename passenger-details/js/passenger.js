// js/passenger.js

document.addEventListener('DOMContentLoaded', () => {
  loadJourneySummary();
  generatePassengerForms();
  
  document.getElementById('passengerForm').addEventListener('submit', handleContinue);
});

function loadJourneySummary() {
  const from = localStorage.getItem('searchFrom') || 'Mumbai';
  const to = localStorage.getItem('searchTo') || 'Pune';
  const dateStr = localStorage.getItem('searchDate') || '2026-07-15';
  
  document.getElementById('summaryRoute').textContent = `${from} → ${to}`;
  document.getElementById('summaryDate').textContent = dateStr;

  const totalFare = localStorage.getItem('totalFare') || '0';
  document.getElementById('reviewFare').textContent = `₹${totalFare}`;
  
  const seatsStr = localStorage.getItem('selectedSeats');
  const seats = seatsStr ? JSON.parse(seatsStr) : ['A1']; // Fallback for dev
  document.getElementById('reviewSeats').textContent = seats.join(', ');
}

function generatePassengerForms() {
  const container = document.getElementById('passengersContainer');
  const seatsStr = localStorage.getItem('selectedSeats');
  const seats = seatsStr ? JSON.parse(seatsStr) : ['A1']; 
  
  seats.forEach((seat, idx) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div class="card-header">
        <span>Passenger ${idx + 1}</span>
        <span class="seat-badge">Seat ${seat}</span>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label>Full Name</label>
          <input type="text" class="form-control pax-name" placeholder="Enter name">
        </div>
        <div class="form-group">
          <label>Age</label>
          <input type="number" class="form-control pax-age" placeholder="Age">
        </div>
        <div class="form-group">
          <label>Gender</label>
          <select class="form-control pax-gender">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Special Assistance</label>
          <select class="form-control pax-assist">
            <option value="None">None</option>
            <option value="Senior Citizen">Senior Citizen</option>
            <option value="Wheelchair">Wheelchair</option>
            <option value="Pregnant">Pregnant</option>
          </select>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

function handleContinue(e) {
  e.preventDefault();
  let isValid = true;
  
  // Validate passengers
  const names = document.querySelectorAll('.pax-name');
  const ages = document.querySelectorAll('.pax-age');
  
  names.forEach(n => { if (!valRequired(n)) isValid = false; });
  ages.forEach(a => { if (!valAge(a)) isValid = false; });
  
  // Validate contact
  const mobile = document.getElementById('contactMobile');
  const email = document.getElementById('contactEmail');
  if (!valRegex(mobile, 'mobile', 'Must be 10 digits')) isValid = false;
  if (!valRegex(email, 'email', 'Invalid email')) isValid = false;
  
  // Validate emergency
  const emName = document.getElementById('emName');
  const emMobile = document.getElementById('emMobile');
  if (!valRequired(emName)) isValid = false;
  if (!valRegex(emMobile, 'mobile', 'Must be 10 digits')) isValid = false;

  const terms = document.getElementById('termsCb');
  if (!terms.checked) {
    showToast("Please accept Terms & Conditions");
    isValid = false;
  }

  if (isValid) {
    // Collect passenger names for success ticket
    const paxData = Array.from(names).map(n => n.value);
    localStorage.setItem('paxNames', JSON.stringify(paxData));
    
    document.getElementById('btnSubmit').textContent = 'Processing...';
    setTimeout(() => {
      window.location.href = '../payment/payment.html';
    }, 1000);
  } else {
    showToast("Please fill all required fields correctly");
  }
}
