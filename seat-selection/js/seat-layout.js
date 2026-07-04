// seat-layout.js

async function loadSeatLayout() {
  try {
    const res = await fetch('data/seats.json');
    const data = await res.json();
    window.seatData = data; // Store globally for other scripts
    renderLayout(data);
  } catch(e) {
    console.error("Failed to load seats", e);
  }
}

function renderLayout(data) {
  const container = document.getElementById('busLayout');
  container.innerHTML = '';
  
  const totalRows = data.layout.rows;
  const seats = data.seats;
  
  for (let i = 1; i <= totalRows; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'seat-row';
    
    // Left group (A, B)
    const leftGroup = document.createElement('div');
    leftGroup.className = 'seat-group';
    
    // Right group (C, D)
    const rightGroup = document.createElement('div');
    rightGroup.className = 'seat-group';
    
    // Find seats for this row
    const rowSeats = seats.filter(s => s.id.startsWith(i.toString()) && s.id.length <= i.toString().length + 1);
    
    rowSeats.forEach(seat => {
      const seatDiv = document.createElement('div');
      seatDiv.className = `seat ${seat.status} ${seat.type}`;
      seatDiv.textContent = seat.id;
      seatDiv.dataset.id = seat.id;
      
      if (seat.id.endsWith('A') || seat.id.endsWith('B')) {
        leftGroup.appendChild(seatDiv);
      } else {
        rightGroup.appendChild(seatDiv);
      }
    });
    
    rowDiv.appendChild(leftGroup);
    
    const aisle = document.createElement('div');
    aisle.className = 'aisle';
    rowDiv.appendChild(aisle);
    
    rowDiv.appendChild(rightGroup);
    
    container.appendChild(rowDiv);
  }
  
  // Initialize click handlers
  if (typeof initSeatSelection === 'function') {
    initSeatSelection();
  }
}
