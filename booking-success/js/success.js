// success.js

document.addEventListener('DOMContentLoaded', () => {
  loadTicketData();
});

function loadTicketData() {
  const pnr = localStorage.getItem('pnr') || 'MH98765';
  const from = localStorage.getItem('searchFrom') || 'Mumbai';
  const to = localStorage.getItem('searchTo') || 'Pune';
  const dateStr = localStorage.getItem('searchDate') || '2026-07-15';
  
  const seatsStr = localStorage.getItem('selectedSeats');
  const seats = seatsStr ? JSON.parse(seatsStr) : ['A1'];
  
  const paxStr = localStorage.getItem('paxNames');
  const paxNames = paxStr ? JSON.parse(paxStr) : ['Guest User'];

  document.getElementById('tktPnr').textContent = pnr;
  document.getElementById('tktFrom').textContent = from.substring(0,3).toUpperCase();
  document.getElementById('tktFromName').textContent = from;
  document.getElementById('tktTo').textContent = to.substring(0,3).toUpperCase();
  document.getElementById('tktToName').textContent = to;
  
  document.getElementById('tktDate').textContent = dateStr;
  document.getElementById('tktSeats').textContent = seats.join(', ');
  document.getElementById('tktPaxNames').innerHTML = paxNames.join('<br>');
}

function triggerDownload() {
  showToast("Downloading digital ticket (PDF)...");
}

function triggerShare() {
  showToast("Opening sharing options...");
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}
