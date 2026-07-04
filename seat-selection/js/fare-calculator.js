// fare-calculator.js

function updateFareSummary(selectedSeatsCount, baseFare) {
  const seatFare = selectedSeatsCount * baseFare;
  const resFee = selectedSeatsCount > 0 ? 15 : 0; // Flat fee or per seat? Let's say per booking flat fee for now
  const convFee = selectedSeatsCount > 0 ? 20 : 0; // Dummy convenience fee
  const gst = Math.round(seatFare * 0.05); // 5% GST
  
  const total = seatFare + resFee + convFee + gst;

  document.getElementById('seatFare').textContent = `₹${seatFare}`;
  document.getElementById('resFee').textContent = `₹${resFee}`;
  document.getElementById('gstAmt').textContent = `₹${gst}`;
  document.getElementById('convFee').textContent = `₹${convFee}`;
  document.getElementById('totalFare').textContent = `₹${total}`;

  const btn = document.getElementById('continueBtn');
  if (selectedSeatsCount > 0) {
    btn.disabled = false;
    btn.textContent = `Continue (₹${total})`;
  } else {
    btn.disabled = true;
    btn.textContent = `Select Seats to Continue`;
  }
}
