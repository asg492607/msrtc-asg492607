// search/js/validation.js

function showToast(msg) {
  const toast = document.getElementById('toast');
  if(!toast) return;
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

function validateSearch(from, to, date) {
  if (!from) { showToast("Please select a departure city"); return false; }
  if (!to) { showToast("Please select a destination city"); return false; }
  if (from.toLowerCase() === to.toLowerCase()) { showToast("Choose different cities for From and To"); return false; }
  if (!date) { showToast("Please select a journey date"); return false; }
  return true;
}

// Set min date to today for date pickers
document.addEventListener("DOMContentLoaded", () => {
  const dateInputs = document.querySelectorAll('input[type="date"]');
  const today = new Date().toISOString().split('T')[0];
  dateInputs.forEach(input => {
    input.setAttribute('min', today);
  });
});
