// bus-details/details.js

document.addEventListener('DOMContentLoaded', () => {
  fetchBusDetails();
  initAccordions();
});

async function fetchBusDetails() {
  try {
    const res = await fetch('dummy-data.json');
    const data = await res.json();
    renderDetails(data);
  } catch (e) {
    console.error("Failed to load bus details", e);
  }
}

function renderDetails(data) {
  // Title & Header
  document.getElementById('busName').textContent = data.name;
  document.getElementById('busNumber').textContent = `${data.number} | ${data.operator}`;
  document.getElementById('busType').textContent = data.type;
  document.getElementById('busRating').textContent = `★ ${data.rating}`;
  document.getElementById('busFare').textContent = `₹${data.fare}`;

  // Timeline
  const tlContainer = document.getElementById('timelineContainer');
  data.timeline.forEach(t => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = `<div class="time-place">${t.place}</div><div class="time-stamp">${t.time}</div>`;
    tlContainer.appendChild(item);
  });

  // Boarding & Dropping
  renderRadioGrid('boardingGrid', data.boardingPoints, 'boarding');
  renderRadioGrid('droppingGrid', data.droppingPoints, 'dropping');

  // Seats
  const percentage = Math.round((data.seats.booked / data.seats.total) * 100);
  document.getElementById('progressFill').style.width = `${percentage}%`;
  document.getElementById('seatTotal').textContent = `${data.seats.total} Seats`;
  document.getElementById('seatAvailable').textContent = `${data.seats.available} Available`;
  document.getElementById('seatBooked').textContent = `${data.seats.booked} Booked`;

  // Amenities
  const amContainer = document.getElementById('amenitiesGrid');
  data.amenities.forEach(am => {
    const div = document.createElement('div');
    div.className = 'amenity-item';
    div.innerHTML = `<span>✨</span> ${am}`; // Dummy icon for now
    amContainer.appendChild(div);
  });

  // Reviews
  const revContainer = document.getElementById('reviewsContainer');
  data.reviews.forEach(r => {
    const div = document.createElement('div');
    div.className = 'review';
    div.innerHTML = `
      <div class="rev-header">
        <span class="rev-name">${r.name}</span>
        <span class="rev-date">${r.date}</span>
      </div>
      <div class="rev-stars">${'★'.repeat(r.stars)}${'☆'.repeat(5 - r.stars)}</div>
      <div class="rev-comment">${r.comment}</div>
    `;
    revContainer.appendChild(div);
  });

  // Fare Summary
  document.getElementById('baseFare').textContent = `₹${data.fare}`;
  const gst = Math.round(data.fare * 0.05);
  document.getElementById('gstAmt').textContent = `₹${gst}`;
  document.getElementById('resFee').textContent = `₹15`;
  document.getElementById('totalFare').textContent = `₹${data.fare + gst + 15}`;
}

function renderRadioGrid(containerId, points, groupName) {
  const container = document.getElementById(containerId);
  points.forEach((p, index) => {
    const card = document.createElement('label');
    card.className = 'radio-card';
    const checked = index === 0 ? 'checked' : '';
    card.innerHTML = `
      <input type="radio" name="${groupName}" value="${p.id}" ${checked}>
      <div>
        <div class="point-name">${p.name}</div>
        <div class="point-time">${p.time}</div>
      </div>
    `;
    container.appendChild(card);
  });

  // Add click listeners to toggle 'selected' class for styling
  container.querySelectorAll('.radio-card input').forEach(input => {
    input.addEventListener('change', () => {
      container.querySelectorAll('.radio-card').forEach(c => c.classList.remove('selected'));
      input.closest('.radio-card').classList.add('selected');
    });
    // Trigger initial select
    if (input.checked) input.closest('.radio-card').classList.add('selected');
  });
}

function initAccordions() {
  const headers = document.querySelectorAll('.acc-header');
  headers.forEach(h => {
    h.addEventListener('click', () => {
      const content = h.nextElementSibling;
      const icon = h.querySelector('.icon');
      if (content.style.display === 'block') {
        content.style.display = 'none';
        icon.textContent = '+';
      } else {
        content.style.display = 'block';
        icon.textContent = '-';
      }
    });
  });
}

function continueToSeatSelection() {
  const toast = document.getElementById('toast');
  toast.textContent = 'Navigating to Seat Selection...';
  toast.style.display = 'block';
  
  setTimeout(() => {
    toast.style.display = 'none';
    // Dummy navigation since Seat Selection module isn't built yet
    alert("Seat Selection Module (Task 6) will be triggered here!");
  }, 1000);
}
