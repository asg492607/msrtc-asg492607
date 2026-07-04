// payment.js

let finalTotal = 0;

document.addEventListener('DOMContentLoaded', () => {
  loadSummary();
  initTabs();
  
  document.getElementById('applyPromoBtn').addEventListener('click', applyPromo);
  document.getElementById('payBtn').addEventListener('click', processPayment);
});

function loadSummary() {
  const baseTotal = parseInt(localStorage.getItem('totalFare') || '620');
  const seatsStr = localStorage.getItem('selectedSeats');
  const seats = seatsStr ? JSON.parse(seatsStr) : ['A1'];
  
  document.getElementById('sumSeats').textContent = seats.join(', ');
  document.getElementById('sumPax').textContent = seats.length;
  
  finalTotal = baseTotal;
  updateTotalDisplay();
}

function initTabs() {
  const btns = document.querySelectorAll('.tab-btn');
  const contents = document.querySelectorAll('.tab-content');
  
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      document.getElementById(btn.dataset.target).classList.add('active');
    });
  });
}

function applyPromo() {
  const code = document.getElementById('promoCode').value.trim().toUpperCase();
  const discRow = document.getElementById('discountRow');
  const toast = document.getElementById('toast');
  
  if (code === 'MSRTC50') {
    const discount = 50;
    finalTotal -= discount;
    discRow.style.display = 'flex';
    document.getElementById('discAmt').textContent = `-₹${discount}`;
    
    toast.style.background = 'var(--success)';
    toast.textContent = 'Promo code applied successfully!';
    updateTotalDisplay();
  } else {
    toast.style.background = 'var(--error)';
    toast.textContent = 'Invalid promo code';
  }
  
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

function updateTotalDisplay() {
  const btn = document.getElementById('payBtn');
  const sumTotal = document.getElementById('sumTotal');
  
  sumTotal.textContent = `₹${finalTotal}`;
  btn.textContent = `Proceed to Pay ₹${finalTotal}`;
}

function processPayment() {
  const overlay = document.getElementById('loaderOverlay');
  overlay.style.display = 'flex';
  
  setTimeout(() => {
    // Generate dummy PNR and save details
    const pnr = 'MH' + Math.floor(Math.random() * 90000 + 10000);
    localStorage.setItem('pnr', pnr);
    localStorage.setItem('bookingDate', new Date().toLocaleDateString());
    
    window.location.href = '../booking-success/success.html';
  }, 3000);
}
