// MSRTC State and Logic Engine
let currentLang = 'en';
let fontSizeState = 2; 
let userSession = null; 
let activeSection = 'home';
let currentSearchBuses = [];
let currentSelectedBus = null;
let selectedSeats = [];
let voiceActive = false;
let discountApplied = false;
let currentUpdateCategory = 'All';

// Simulated State (In-Memory Database)
let myBookings = [
  { pnr: "PNR9938210", from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", busNo: "MSR-101", seats: ["A1", "A2"], date: "2026-07-15", fare: 1100, status: "Active" }
];

let myPasses = [
  { id: "PASS-S881", name: "Atharva K.", type: "Student Concession (Monthly)", proof: "Aadhaar: 9931-2918-1123", status: "Approved" }
];

let myComplaints = [
  { id: "COMP-229", category: "Cleanliness", busNo: "MH-12-AQ-9932", desc: "AC vents in Shivneri bus were blocked.", status: "Pending" }
];

let allParcels = [
  { id: "MSR-P-992", sender: "Ramesh P.", receiver: "Sunita S.", status: "transit", details: "Departed from Pune (Shivajinagar) cargo hub at 09:30 AM" }
];

let savedPassengers = [
  { name: "Atharva K.", age: 24, gender: "Male" },
  { name: "Sunita K.", age: 52, gender: "Female" }
];

let favoriteRoutes = [
  { from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)" },
  { from: "Pune (Swargate)", to: "Kolhapur (CBS)" }
];

// Initial Setup
window.addEventListener('DOMContentLoaded', () => {
  renderAnnouncements();
  renderNews();
  renderPopularRoutes();
  renderAboutSection();
  renderDepotsList();
  renderConcessionsList();
  renderPublicTenders();
  renderPublicRecruitments();
  renderPublicCirculars();
  updateLangStrings();
  
  const dateInput = document.getElementById('searchDate');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
    dateInput.value = today;
  }
});

// Toast notification helper
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>💬</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

// View Router
function showSection(sectionId) {
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(link => link.classList.remove('active'));
  document.querySelectorAll('.bottom-nav-item').forEach(link => link.classList.remove('active'));
  
  const targetSec = document.getElementById(`view-${sectionId}`);
  if (targetSec) {
    targetSec.classList.add('active');
    activeSection = sectionId;
  }

  // Toggle Header Highlight
  document.querySelectorAll('.nav-item').forEach(link => {
    if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(sectionId)) {
      link.classList.add('active');
    }
  });

  // Highlight mobile bottom tabs matching routing
  if (sectionId === 'home') document.getElementById('bnav-home').classList.add('active');
  if (sectionId === 'booking') document.getElementById('bnav-book').classList.add('active');
  if (sectionId === 'dashboard') document.getElementById('bnav-profile').classList.add('active');

  const heroBanner = document.getElementById('hero-banner');
  if (heroBanner) {
    heroBanner.style.display = (sectionId === 'home') ? 'flex' : 'none';
  }

  // Reload views dynamically
  if (sectionId === 'dashboard') {
    renderDashboard();
  } else if (sectionId === 'admin') {
    renderAdminPortal();
  } else if (sectionId === 'schedule') {
    renderSchedulesList();
  }
}

// Accessibility
function toggleHighContrast() {
  const body = document.body;
  const current = body.getAttribute('data-theme');
  body.setAttribute('data-theme', current === 'high-contrast' ? 'light' : 'high-contrast');
  showToast("Contrast Theme Toggled", "success");
}

function changeFontSize() {
  const body = document.body;
  body.classList.remove('text-scale-1', 'text-scale-2', 'text-scale-3');
  fontSizeState = (fontSizeState % 3) + 1;
  body.classList.add(`text-scale-${fontSizeState}`);
  showToast("Font size adjusted", "success");
}

function dismissBanner() {
  document.getElementById('systemBanner').style.display = 'none';
}

// Language Translation Switch
function changeLanguage(langCode) {
  currentLang = langCode;
  const langSel = document.getElementById('languageSelect');
  if (langSel) langSel.value = langCode;
  const setLangSel = document.getElementById('settingLanguageSelect');
  if (setLangSel) setLangSel.value = langCode;
  updateLangStrings();
  showToast(`Language switched to: ${langCode.toUpperCase()}`, "success");
}

function updateLangStrings() {
  const dictionary = MSRTC_DATA.translations[currentLang];
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    if (dictionary[key]) {
      if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
        el.placeholder = dictionary[key];
      } else {
        el.textContent = dictionary[key];
      }
    }
  });
}

// Category filter updates triggers
function filterUpdatesByCategory(cat, buttonEl) {
  currentUpdateCategory = cat;
  buttonEl.parentElement.querySelectorAll('.filter-chip').forEach(btn => btn.classList.remove('active'));
  buttonEl.classList.add('active');
  renderAnnouncements();
}

// Data Renderers
function renderAnnouncements() {
  const container = document.getElementById('announcementsList');
  if (!container) return;
  
  let items = MSRTC_DATA.announcements;
  if (currentUpdateCategory !== 'All') {
    items = items.filter(ann => ann.category === currentUpdateCategory);
  }

  if (items.length === 0) {
    container.innerHTML = `<p style="padding:1rem; color:var(--text-secondary);">No updates under category: ${currentUpdateCategory}</p>`;
    return;
  }

  container.innerHTML = items.map(ann => `
    <div class="announcement-card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.25rem;">
        <strong style="color:var(--primary);">${ann.title}</strong>
        <span style="background:rgba(255,107,0,0.1); color:var(--primary); padding:0.15rem 0.4rem; border-radius:4px; font-size:0.7rem; font-weight:700;">${ann.category}</span>
      </div>
      <p style="font-size:0.9rem;">${ann.desc}</p>
      <small style="color:var(--text-secondary); display:block; margin-top:0.4rem;">Published: ${ann.date}</small>
    </div>
  `).join('');
}

function renderNews() {
  const container = document.getElementById('newsList');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.news.map(n => `
    <div class="announcement-card" style="border-left-color: var(--secondary);">
      <strong>${n.title}</strong>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.25rem;">${n.desc}</p>
    </div>
  `).join('');
}

function renderPopularRoutes() {
  const container = document.getElementById('popularRoutesContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.popularRoutes.map(route => `
    <div class="shortcut-card" onclick="bookPopularRoute('${route.from}', '${route.to}')">
      <span style="color:var(--primary); font-weight:800;">📍 Route</span>
      <h4 style="margin: 0.5rem 0; font-size:1rem;">${route.from.split(' ')[0]} to ${route.to.split(' ')[0]}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary);">${route.time} | <strong>${route.fare}</strong></p>
    </div>
  `).join('');
}

function bookPopularRoute(from, to) {
  document.getElementById('searchFrom').value = from;
  document.getElementById('searchTo').value = to;
  showSection('home');
  document.getElementById('searchCard').scrollIntoView({ behavior: 'smooth' });
}

// Autocomplete suggestions
function showSuggestions(inputEl, fieldType) {
  const query = inputEl.value.toLowerCase();
  const dropdown = document.getElementById(`${fieldType}Suggestions`);
  if (!dropdown) return;
  
  if (query.length < 2) {
    dropdown.style.display = 'none';
    return;
  }
  
  const matches = MSRTC_DATA.locations.filter(loc => loc.toLowerCase().includes(query));
  if (matches.length === 0) {
    dropdown.style.display = 'none';
    return;
  }
  
  dropdown.innerHTML = matches.map(match => `
    <div class="suggestion-item" onclick="selectSuggestion('${match}', '${inputEl.id}', '${dropdown.id}')">${match}</div>
  `).join('');
  dropdown.style.display = 'block';
}

function selectSuggestion(val, inputId, dropdownId) {
  document.getElementById(inputId).value = val;
  document.getElementById(dropdownId).style.display = 'none';
}

function swapFromTo() {
  const fromVal = document.getElementById('searchFrom').value;
  const toVal = document.getElementById('searchTo').value;
  document.getElementById('searchFrom').value = toVal;
  document.getElementById('searchTo').value = fromVal;
  showToast("Locations Swapped", "success");
}

// Search Buses Flow
function handleBusSearch(event) {
  if (event) event.preventDefault();
  const from = document.getElementById('searchFrom').value;
  const to = document.getElementById('searchTo').value;
  const date = document.getElementById('searchDate').value;
  const filterType = document.getElementById('searchBusType').value;
  
  let results = MSRTC_DATA.buses.filter(bus => 
    bus.from.toLowerCase().includes(from.toLowerCase()) && 
    bus.to.toLowerCase().includes(to.toLowerCase())
  );

  if (filterType !== 'all') {
    results = results.filter(bus => bus.type === filterType);
  }
  
  currentSearchBuses = results;
  showSection('booking');
  goBackToStep(1);

  document.getElementById('searchResultsTitle').innerHTML = `Buses from <span style="color:var(--primary);">${from}</span> to <span style="color:var(--primary);">${to}</span> on ${date}`;
  
  // Show Skeleton loading simulation
  const skeleton = document.getElementById('busSkeletonLoader');
  const busResults = document.getElementById('busResultsList');
  
  busResults.innerHTML = '';
  skeleton.style.display = 'flex';
  
  setTimeout(() => {
    skeleton.style.display = 'none';
    renderBusResults();
  }, 1000);
}

// Bus cards result render
function renderBusResults() {
  const container = document.getElementById('busResultsList');
  if (currentSearchBuses.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding: 3rem;"><p style="font-size: 1.2rem; color: var(--text-secondary);">No buses matching criteria found. Adjust search filters.</p></div>`;
    return;
  }
  
  container.innerHTML = currentSearchBuses.map(bus => {
    const amenities = MSRTC_DATA.busTypes.find(t => t.id === bus.type).amenities;
    return `
      <div class="bus-card">
        <div class="bus-info">
          <h3>${bus.name}</h3>
          <p style="color:var(--text-secondary); font-size:0.9rem;">Runs: ${bus.runsOn} | ID: ${bus.id}</p>
          <span class="bus-tag">${MSRTC_DATA.busTypes.find(t => t.id === bus.type).name}</span>
          <div style="margin-top: 0.5rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
            ${amenities.map(am => `<small style="background:rgba(0,0,0,0.03); padding:0.1rem 0.4rem; border-radius:4px; border:1px solid var(--border); font-size:0.75rem;">${am}</small>`).join('')}
          </div>
        </div>
        <div class="bus-timing">
          <h4>${bus.dept}</h4>
          <p>Departure</p>
          <span style="font-size: 0.8rem; color:var(--text-secondary);">${bus.from.split(' ')[0]}</span>
        </div>
        <div class="bus-timing">
          <h4>${bus.arr}</h4>
          <p>${bus.duration} (${bus.distance})</p>
          <span style="font-size: 0.8rem; color:var(--text-secondary);">${bus.to.split(' ')[0]}</span>
        </div>
        <div class="bus-pricing">
          <h4>₹${bus.baseFare}</h4>
          <button class="btn-primary" style="margin-top:0.5rem;" onclick="selectBusForBooking('${bus.id}')">Book Now</button>
        </div>
      </div>
    `;
  }).join('');
}

// Seat Selector
function selectBusForBooking(busId) {
  currentSelectedBus = MSRTC_DATA.buses.find(b => b.id === busId);
  selectedSeats = [];
  discountApplied = false;
  
  document.querySelectorAll('.booking-flow-step').forEach(step => step.style.display = 'none');
  document.getElementById('booking-step-seats').style.display = 'grid';
  updateStepNodes(2);
  
  document.getElementById('sumBusName').innerText = `${currentSelectedBus.name} (${currentSelectedBus.id})`;
  document.getElementById('sumSeatsSelected').innerText = 'Selected Seats: -';
  document.getElementById('sumFare').innerText = 'Total: ₹0';

  const boardSel = document.getElementById('boardingPoint');
  const dropSel = document.getElementById('droppingPoint');
  
  boardSel.innerHTML = `<option value="${currentSelectedBus.from}">${currentSelectedBus.from} Depot</option>`;
  dropSel.innerHTML = `<option value="${currentSelectedBus.to}">${currentSelectedBus.to} Depot</option>`;
  
  renderSeatsGrid();
}

function renderSeatsGrid() {
  const container = document.getElementById('seatsGrid');
  container.innerHTML = '';
  for (let row = 1; row <= 7; row++) {
    for (let col = 1; col <= 5; col++) {
      if (col === 3) {
        const aisle = document.createElement('div');
        aisle.className = 'seat-aisle';
        container.appendChild(aisle);
        continue;
      }
      
      const seatNo = `${String.fromCharCode(64 + row)}${col > 3 ? col - 1 : col}`;
      const seatDiv = document.createElement('div');
      
      let seatClass = 'seat';
      if (row === 2) seatClass += ' ladies';
      if (row === 3 && col === 1) seatClass += ' senior';
      if (row === 4 || (row === 1 && col === 2)) seatClass += ' booked';
      
      seatDiv.className = seatClass;
      seatDiv.innerText = seatNo;
      
      if (!seatClass.includes('booked')) {
        seatDiv.onclick = () => toggleSeatSelection(seatNo, seatDiv);
      }
      container.appendChild(seatDiv);
    }
  }
}

function toggleSeatSelection(seatNo, element) {
  if (selectedSeats.includes(seatNo)) {
    selectedSeats = selectedSeats.filter(s => s !== seatNo);
    element.classList.remove('selected');
  } else {
    selectedSeats.push(seatNo);
    element.classList.add('selected');
  }
  
  const base = selectedSeats.length * currentSelectedBus.baseFare;
  document.getElementById('sumSeatsSelected').innerText = `Selected Seats: ${selectedSeats.length > 0 ? selectedSeats.join(', ') : '-'}`;
  document.getElementById('sumFare').innerText = `Total: ₹${base}`;
}

// Passenger Details & Autofill
function proceedToPassengerDetails() {
  if (selectedSeats.length === 0) {
    alert("Please select at least one seat to continue.");
    return;
  }
  
  document.querySelectorAll('.booking-flow-step').forEach(step => step.style.display = 'none');
  document.getElementById('booking-step-passenger').style.display = 'block';
  updateStepNodes(3);
  
  const container = document.getElementById('passengerFormsContainer');
  container.innerHTML = selectedSeats.map((seat, index) => `
    <div style="background:var(--bg-primary); padding: 1rem; border-radius:8px; margin-bottom:1rem; border-left: 3px solid var(--primary);">
      <h5 style="margin-bottom:0.75rem;">Passenger ${index + 1} - Seat ${seat}</h5>
      <div class="form-grid" style="grid-template-columns:1fr 1fr;">
        <div class="form-group">
          <label>Full Name</label>
          <input type="text" id="pName-${index}" required>
        </div>
        <div class="form-group">
          <label>Age</label>
          <input type="number" id="pAge-${index}" min="1" max="120" required>
        </div>
        <div class="form-group" style="margin-top:1rem;">
          <label>Gender</label>
          <select id="pGender-${index}">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>
    </div>
  `).join('');
}

function autofillSavedPassenger() {
  if (savedPassengers.length === 0) {
    alert("No profiles saved in dashboard passenger directory.");
    return;
  }
  
  selectedSeats.forEach((seat, index) => {
    if (savedPassengers[index]) {
      const nameInp = document.getElementById(`pName-${index}`);
      const ageInp = document.getElementById(`pAge-${index}`);
      const genderInp = document.getElementById(`pGender-${index}`);
      
      if (nameInp) nameInp.value = savedPassengers[index].name;
      if (ageInp) ageInp.value = savedPassengers[index].age;
      if (genderInp) genderInp.value = savedPassengers[index].gender;
    }
  });
}

// Payment calculation
function proceedToPayment(event) {
  event.preventDefault();
  
  document.querySelectorAll('.booking-flow-step').forEach(step => step.style.display = 'none');
  document.getElementById('booking-step-payment').style.display = 'block';
  updateStepNodes(4);
  
  document.getElementById('payBus').innerText = `Bus: ${currentSelectedBus.name} (ID: ${currentSelectedBus.id})`;
  document.getElementById('paySeats').innerText = `Seats: ${selectedSeats.join(', ')}`;
  
  updatePaymentFareBreakup();
}

function updatePaymentFareBreakup() {
  let basePrice = selectedSeats.length * currentSelectedBus.baseFare;
  if (discountApplied) {
    basePrice = Math.round(basePrice * 0.5);
  }
  
  const gst = Math.round(basePrice * 0.05);
  const total = basePrice + gst;
  
  document.getElementById('payBaseFare').innerText = `₹${basePrice}`;
  document.getElementById('payGst').innerText = `₹${gst}`;
  document.getElementById('payTotal').innerText = `Total Fare: ₹${total}`;
}

function applyPromoCode() {
  const code = document.getElementById('promoCodeInput').value.trim().toUpperCase();
  if (code === 'DISCO50' || code === 'MSRTC50') {
    discountApplied = true;
    showToast("Promo Code Applied! 50% discount", "success");
    updatePaymentFareBreakup();
  } else {
    showToast("Invalid Promo Code", "error");
  }
}

function togglePaymentInputs(val) {
  document.getElementById('upiInputContainer').style.display = val === 'upi' ? 'flex' : 'none';
  document.getElementById('cardInputContainer').style.display = val === 'card' ? 'block' : 'none';
}

function completeBooking(event) {
  event.preventDefault();
  const randomPnr = "PNR" + Math.floor(100000000 + Math.random() * 900000000);
  
  let basePrice = selectedSeats.length * currentSelectedBus.baseFare;
  if (discountApplied) basePrice = Math.round(basePrice * 0.5);
  const total = basePrice + Math.round(basePrice * 0.05);
  
  const newBooking = {
    pnr: randomPnr,
    from: currentSelectedBus.from,
    to: currentSelectedBus.to,
    busNo: currentSelectedBus.id,
    seats: [...selectedSeats],
    date: document.getElementById('searchDate').value,
    fare: total,
    status: "Active"
  };
  
  myBookings.unshift(newBooking);
  
  document.getElementById('ticketPnr').innerText = `PNR: ${randomPnr}`;
  document.getElementById('tFrom').innerText = currentSelectedBus.from;
  document.getElementById('tTo').innerText = currentSelectedBus.to;
  document.getElementById('tBus').innerText = `${currentSelectedBus.id} (${currentSelectedBus.name})`;
  document.getElementById('tSeats').innerText = selectedSeats.join(', ');
  document.getElementById('tDate').innerText = newBooking.date;
  document.getElementById('tFare').innerText = `₹${total}`;
  
  document.querySelectorAll('.booking-flow-step').forEach(step => step.style.display = 'none');
  document.getElementById('booking-step-success').style.display = 'block';
  document.getElementById('step-node-4').classList.add('done');
  showToast("Booking completed successfully!", "success");
}

function updateStepNodes(activeStepIndex) {
  for (let i = 1; i <= 4; i++) {
    const node = document.getElementById(`step-node-${i}`);
    if (node) {
      node.className = 'step-node';
      if (i < activeStepIndex) node.classList.add('done');
      if (i === activeStepIndex) node.classList.add('active');
    }
  }
}

function goBackToStep(stepNum) {
  document.querySelectorAll('.booking-flow-step').forEach(step => step.style.display = 'none');
  if (stepNum === 1) {
    document.getElementById('booking-step-results').style.display = 'block';
  } else if (stepNum === 2) {
    document.getElementById('booking-step-seats').style.display = 'grid';
  }
  updateStepNodes(stepNum);
}

function downloadTicketPDF() {
  showToast("Ticket PDF Download Started", "success");
}

// Authentication Tabs
function toggleAuthTab(mode) {
  const loginForm = document.getElementById('loginFormContainer');
  const signupForm = document.getElementById('signupFormContainer');
  const btnLogin = document.getElementById('tabBtnLogin');
  const btnSignup = document.getElementById('tabBtnSignup');

  if (mode === 'login') {
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
    btnLogin.classList.add('active');
    btnSignup.classList.remove('active');
  } else {
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
    btnLogin.classList.remove('active');
    btnSignup.classList.add('active');
  }
}

function toggleLoginMethod(val) {
  const isOtp = (val === 'otp');
  document.getElementById('loginMobileGroup').style.display = isOtp ? 'flex' : 'none';
  document.getElementById('loginPasswordGroup').style.display = isOtp ? 'none' : 'block';
  document.getElementById('authSubmitBtn').innerText = isOtp ? 'Send OTP' : 'Sign In';
  document.getElementById('otpInputContainer').style.display = 'none';
}

function handleAuthSubmit(event) {
  event.preventDefault();
  const loginMethod = document.getElementById('loginTypeSelect').value;
  
  if (loginMethod === 'otp') {
    const otpContainer = document.getElementById('otpInputContainer');
    const submitBtn = document.getElementById('authSubmitBtn');
    
    if (otpContainer.style.display === 'none') {
      otpContainer.style.display = 'flex';
      submitBtn.innerText = 'Verify & Login';
      showToast("OTP Verification Code Sent to Mobile", "success");
    } else {
      const otpCode = document.getElementById('authOtp').value;
      if (otpCode === '1234') {
        const mobile = document.getElementById('authMobile').value;
        const isAdmin = (mobile === '9876543210');
        
        userSession = {
          mobile,
          name: isAdmin ? "System Admin" : "Atharva K.",
          role: isAdmin ? "admin" : "user"
        };
        updateAuthUI();
        showSection(isAdmin ? 'admin' : 'dashboard');
        showToast("Login Successful", "success");
      } else {
        showToast("Invalid OTP. Try 1234", "error");
      }
    }
  } else {
    const email = document.getElementById('authEmail').value;
    const password = document.getElementById('authPassword').value;
    
    if (email && password.length >= 4) {
      userSession = {
        mobile: "9938210398",
        name: "Atharva K.",
        role: "user"
      };
      updateAuthUI();
      showSection('dashboard');
      showToast("Signed In via Email", "success");
    } else {
      showToast("Verification Error", "error");
    }
  }
}

function handleRegistrationSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('regName').value;
  const mobile = document.getElementById('regMobile').value;
  
  userSession = {
    mobile,
    name,
    role: "user"
  };
  
  showToast("Account created successfully", "success");
  updateAuthUI();
  showSection('dashboard');
}

function updateAuthUI() {
  const widget = document.getElementById('userWidget');
  if (userSession) {
    widget.innerHTML = `
      <span style="font-weight:600; color:var(--primary); font-size:0.95rem; margin-right:1rem;">Hi, ${userSession.name}</span>
      <button onclick="handleLogout()" class="btn-secondary" data-key="logout" style="padding:0.4rem 1rem; font-size:0.85rem;">Logout</button>
    `;
  } else {
    widget.innerHTML = `
      <button onclick="showSection('login')" class="btn-primary" data-key="login" style="padding:0.4rem 1rem; font-size:0.85rem;">Login / Sign Up</button>
    `;
  }
  updateLangStrings();
}

function handleLogout() {
  userSession = null;
  updateAuthUI();
  showSection('home');
  showToast("Logged Out Successfully", "success");
}

// User Dashboard Tabs & Functions
function switchDashboardTab(tabName, el) {
  document.querySelectorAll('.dash-tab-content').forEach(tab => tab.style.display = 'none');
  document.getElementById(`dash-${tabName}`).style.display = 'block';
  
  el.parentElement.querySelectorAll('.panel-menu-item').forEach(btn => btn.classList.remove('active'));
  el.classList.add('active');
}

function renderDashboard() {
  if (!userSession) {
    showSection('login');
    alert("Authentication required. Please sign in first.");
    return;
  }
  
  document.getElementById('dashboardGreeting').innerText = `Namaskar, ${userSession.name} (${userSession.mobile})`;
  
  const ticketCont = document.getElementById('dashboardTicketsList');
  ticketCont.innerHTML = myBookings.map(t => `
    <div class="bus-card">
      <div class="bus-info">
        <h3>${t.from.split(' ')[0]} ➔ ${t.to.split(' ')[0]}</h3>
        <p style="color:var(--text-secondary); font-size:0.9rem;">Journey Date: ${t.date} | Seats: ${t.seats.join(', ')}</p>
        <span class="bus-tag">${t.pnr}</span>
      </div>
      <div>
        <small style="color:var(--text-secondary);">Bus ID</small>
        <h4>${t.busNo}</h4>
      </div>
      <div>
        <small style="color:var(--text-secondary);">Total Paid</small>
        <h4>₹${t.fare}</h4>
      </div>
      <div>
        <span style="background:rgba(16,185,129,0.1); color:var(--seat-avail); padding:0.25rem 0.6rem; border-radius:6px; font-weight:bold;">${t.status}</span>
        ${t.status === 'Active' ? `<button class="btn-secondary" style="margin-top:0.5rem; display:block; width:100%; font-size:0.8rem; padding:0.3rem;" onclick="cancelTicketSim('${t.pnr}')">Cancel</button>` : ''}
      </div>
    </div>
  `).join('');

  const passCont = document.getElementById('dashboardPassesList');
  passCont.innerHTML = myPasses.map(p => `
    <div class="bus-card">
      <div class="bus-info">
        <h3>${p.type}</h3>
        <p style="color:var(--text-secondary); font-size:0.85rem;">Holder: ${p.name} | Verified Proof: ${p.proof}</p>
        <span class="bus-tag">${p.id}</span>
      </div>
      <div class="qr-placeholder" style="margin:0;">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="black">
          <rect x="0" y="0" width="30" height="30"/>
          <rect x="70" y="0" width="30" height="30"/>
          <rect x="0" y="70" width="30" height="30"/>
          <rect x="40" y="40" width="20" height="20"/>
        </svg>
      </div>
      <div style="text-align:right;">
        <span style="background:rgba(16,185,129,0.1); color:var(--seat-avail); padding:0.25rem 0.6rem; border-radius:6px; font-weight:bold;">${p.status}</span>
      </div>
    </div>
  `).join('');

  const compCont = document.getElementById('dashboardComplaintsList');
  compCont.innerHTML = myComplaints.map(c => `
    <div class="bus-card" style="border-left: 4px solid var(--primary);">
      <div class="bus-info">
        <h3>${c.category}</h3>
        <p style="color:var(--text-secondary); font-size:0.85rem;">${c.desc}</p>
        <span class="bus-tag">${c.id}</span>
      </div>
      <div>
        <small style="color:var(--text-secondary);">Target Vehicle</small>
        <p style="font-weight:bold;">${c.busNo || 'N/A'}</p>
      </div>
      <div style="text-align:right;">
        <span style="background:rgba(251,191,36,0.1); color:var(--primary); padding:0.25rem 0.6rem; border-radius:6px; font-weight:bold;">${c.status}</span>
      </div>
    </div>
  `).join('');

  const favCont = document.getElementById('dashboardFavoritesList');
  favCont.innerHTML = favoriteRoutes.map(route => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${route.from.split(' ')[0]} to ${route.to.split(' ')[0]}</strong>
        <p style="font-size:0.8rem; color:var(--text-secondary);">${route.from} ➔ ${route.to}</p>
      </div>
      <div style="text-align:right;">
        <button class="btn-primary" style="font-size:0.8rem; padding:0.4rem 0.8rem;" onclick="bookPopularRoute('${route.from}', '${route.to}')">Book</button>
      </div>
    </div>
  `).join('');

  const psgCont = document.getElementById('dashboardPassengersList');
  psgCont.innerHTML = savedPassengers.map(p => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${p.name}</strong>
        <p style="font-size:0.8rem; color:var(--text-secondary);">Age: ${p.age} | Gender: ${p.gender}</p>
      </div>
      <div style="text-align:right;">
        <button class="btn-secondary" style="font-size:0.8rem; color:var(--primary); border-color:var(--primary); padding:0.25rem 0.5rem;" onclick="deleteSavedPassenger('${p.name}')">Delete</button>
      </div>
    </div>
  `).join('');
}

function cancelTicketSim(pnr) {
  if (confirm(`Cancel ticket booking PNR: ${pnr}?`)) {
    myBookings = myBookings.map(t => t.pnr === pnr ? { ...t, status: "Cancelled" } : t);
    renderDashboard();
    showToast("Ticket Cancelled successfully", "success");
  }
}

// Pass Actions
function showPassApplicationForm() {
  document.getElementById('passAppFormContainer').style.display = 'block';
}

function submitPassApplication(event) {
  event.preventDefault();
  const name = document.getElementById('passName').value;
  const type = document.getElementById('passType').value;
  const proof = document.getElementById('passIdProof').value;
  const newPassId = "PASS-S" + Math.floor(100 + Math.random() * 900);
  
  myPasses.push({ id: newPassId, name, type, proof: `Aadhaar: ${proof}`, status: "Approved" });
  document.getElementById('passAppFormContainer').style.display = 'none';
  document.getElementById('passAppForm').reset();
  renderDashboard();
  showToast("New smart pass issued", "success");
}

// Saved Passengers Actions
function showAddPassengerForm() {
  document.getElementById('addPassengerFormContainer').style.display = 'block';
}

function saveNewPassenger(event) {
  event.preventDefault();
  const name = document.getElementById('spName').value;
  const age = parseInt(document.getElementById('spAge').value);
  const gender = document.getElementById('spGender').value;
  
  savedPassengers.push({ name, age, gender });
  document.getElementById('addPassengerFormContainer').style.display = 'none';
  document.getElementById('addPassengerForm').reset();
  renderDashboard();
  showToast("Traveler profile saved", "success");
}

function deleteSavedPassenger(name) {
  savedPassengers = savedPassengers.filter(p => p.name !== name);
  renderDashboard();
  showToast("Traveler profile removed", "success");
}

// Complaint filing Actions
function showComplaintForm() {
  document.getElementById('complaintFormContainer').style.display = 'block';
}

function submitGrievance(event) {
  event.preventDefault();
  const category = document.getElementById('compCategory').value;
  const busNo = document.getElementById('compBusNo').value;
  const desc = document.getElementById('compDesc').value;
  const compId = "COMP-" + Math.floor(100 + Math.random() * 900);
  
  myComplaints.push({ id: compId, category, busNo, desc, status: "Pending" });
  document.getElementById('complaintFormContainer').style.display = 'none';
  document.getElementById('complaintForm').reset();
  renderDashboard();
  showToast("Grievance registered in database", "success");
}

// Parcel calculator & trackers
function switchParcelTab(tabName, el) {
  document.querySelectorAll('.parcel-tab-content').forEach(tab => tab.style.display = 'none');
  document.getElementById(`parcel-${tabName}`).style.display = 'block';
  
  el.parentElement.querySelectorAll('.panel-menu-item').forEach(btn => btn.classList.remove('active'));
  el.classList.add('active');
}

function calcParcelPrice() {
  const w = parseFloat(document.getElementById('pWeight').value) || 0;
  const d = parseFloat(document.getElementById('pDistance').value) || 0;
  const total = Math.round((w * 15) + (d * 0.8));
  document.getElementById('parcelEstPrice').innerText = `₹${total}`;
}

function handleParcelBooking(event) {
  event.preventDefault();
  const sender = document.getElementById('pbSender').value;
  const receiver = document.getElementById('pbReceiver').value;
  
  const id = "MSR-P-" + Math.floor(100 + Math.random() * 900);
  allParcels.push({
    id, sender, receiver, status: "booked", details: "Parcel registered and loaded onto dispatch container."
  });
  
  alert(`Booking Confirmed! Reference Track ID: ${id}`);
  document.getElementById('parcelBookForm').reset();
  showToast("Parcel booked successfully", "success");
}

function trackParcel() {
  const trackId = document.getElementById('parcelTrackId').value.trim();
  const matchedParcel = allParcels.find(p => p.id.toLowerCase() === trackId.toLowerCase());
  
  const resultDiv = document.getElementById('parcelTrackResult');
  if (!matchedParcel) {
    resultDiv.innerHTML = `<p style="color:var(--primary);">No parcel records matching ID: ${trackId}</p>`;
    resultDiv.style.display = 'block';
    return;
  }
  
  resultDiv.style.display = 'block';
  document.getElementById('pTrackStatusHeader').innerText = `Status: ${matchedParcel.status.toUpperCase()}`;
  document.getElementById('pTrackDetails').innerText = matchedParcel.details;
  
  document.querySelectorAll('.tracker-node').forEach(node => node.classList.remove('active'));
  document.getElementById('p-node-booked').classList.add('active');
  
  if (matchedParcel.status === 'dispatched' || matchedParcel.status === 'transit' || matchedParcel.status === 'delivered') {
    document.getElementById('p-node-dispatched').classList.add('active');
  }
  if (matchedParcel.status === 'transit' || matchedParcel.status === 'delivered') {
    document.getElementById('p-node-transit').classList.add('active');
  }
  if (matchedParcel.status === 'delivered') {
    document.getElementById('p-node-delivered').classList.add('active');
  }
  showToast("Parcel details loaded", "success");
}

// Schedule board filtering
function renderSchedulesList() {
  const container = document.getElementById('scheduleList');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.buses.map(bus => `
    <div class="bus-card">
      <div class="bus-info">
        <h3>${bus.from.split(' ')[0]} ➔ ${bus.to.split(' ')[0]}</h3>
        <p style="color:var(--text-secondary); font-size:0.9rem;">Runs: ${bus.runsOn} | Details: ${bus.distance} @ ${bus.duration}</p>
        <span class="bus-tag">${MSRTC_DATA.busTypes.find(t => t.id === bus.type).name}</span>
      </div>
      <div class="bus-timing">
        <h4>${bus.dept}</h4>
        <p>Departure</p>
      </div>
      <div class="bus-timing">
        <h4>${bus.arr}</h4>
        <p>Arrival</p>
      </div>
      <div>
        <button class="btn-primary" onclick="bookFromSchedule('${bus.from}', '${bus.to}')">Book Journey</button>
      </div>
    </div>
  `).join('');
}

function filterSchedules() {
  const query = document.getElementById('scheduleSearch').value.toLowerCase();
  const typeFilter = document.getElementById('scheduleBusType').value;
  
  const filtered = MSRTC_DATA.buses.filter(bus => {
    const matchesCity = bus.from.toLowerCase().includes(query) || bus.to.toLowerCase().includes(query);
    const matchesType = (typeFilter === 'all') || (bus.type === typeFilter);
    return matchesCity && matchesType;
  });
  
  const container = document.getElementById('scheduleList');
  container.innerHTML = filtered.map(bus => `
    <div class="bus-card">
      <div class="bus-info">
        <h3>${bus.from.split(' ')[0]} ➔ ${bus.to.split(' ')[0]}</h3>
        <p style="color:var(--text-secondary); font-size:0.9rem;">Runs: ${bus.runsOn} | Details: ${bus.distance} @ ${bus.duration}</p>
        <span class="bus-tag">${MSRTC_DATA.busTypes.find(t => t.id === bus.type).name}</span>
      </div>
      <div class="bus-timing">
        <h4>${bus.dept}</h4>
        <p>Departure</p>
      </div>
      <div class="bus-timing">
        <h4>${bus.arr}</h4>
        <p>Arrival</p>
      </div>
      <div>
        <button class="btn-primary" onclick="bookFromSchedule('${bus.from}', '${bus.to}')">Book Journey</button>
      </div>
    </div>
  `).join('');
}

function bookFromSchedule(from, to) {
  document.getElementById('searchFrom').value = from;
  document.getElementById('searchTo').value = to;
  showSection('home');
}

// Admin portal controls
function switchAdminTab(tabName, el) {
  document.querySelectorAll('.admin-tab-content').forEach(tab => tab.style.display = 'none');
  document.getElementById(`admin-${tabName}`).style.display = 'block';
  
  el.parentElement.querySelectorAll('.panel-menu-item').forEach(btn => btn.classList.remove('active'));
  el.classList.add('active');
}

function renderAdminPortal() {
  if (!userSession || userSession.role !== 'admin') {
    showSection('login');
    alert("Admin privileges required. Sign in with mobile number '9876543210'.");
    return;
  }
  
  const fleetList = document.getElementById('adminBusList');
  fleetList.innerHTML = MSRTC_DATA.buses.map(bus => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${bus.id}</strong> - ${bus.name}
        <p style="font-size:0.85rem; color:var(--text-secondary);">${bus.from} to ${bus.to}</p>
      </div>
      <div><p>Dept: ${bus.dept}</p></div>
      <div><p>Fare: ₹${bus.baseFare}</p></div>
      <div style="text-align:right;">
        <button class="btn-secondary" style="font-size:0.75rem; color:var(--primary); border-color:var(--primary); padding:0.25rem 0.5rem;" onclick="removeBusFromFleet('${bus.id}')">Remove</button>
      </div>
    </div>
  `).join('');

  const routeList = document.getElementById('adminRouteList');
  routeList.innerHTML = MSRTC_DATA.routes.map(r => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${r.id}</strong> - ${r.from} to ${r.to}
        <p style="font-size:0.85rem; color:var(--text-secondary);">Via: ${r.via}</p>
      </div>
      <div><p>${r.dailyTrips}</p></div>
      <div style="text-align:right;">
        <span style="color:var(--seat-avail); font-weight:bold;">${r.status}</span>
      </div>
    </div>
  `).join('');

  const grievanceList = document.getElementById('adminComplaintsList');
  grievanceList.innerHTML = myComplaints.map(c => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${c.id}</strong> | ${c.category}
        <p style="font-size:0.85rem;">Description: ${c.desc}</p>
      </div>
      <div><small>Bus: ${c.busNo || 'N/A'}</small></div>
      <div style="text-align:right;">
        <select onchange="updateComplaintStatus('${c.id}', this.value)" style="background:var(--bg-primary); border:1px solid var(--border); color:var(--text-primary); padding:0.25rem; border-radius:4px;">
          <option value="Pending" ${c.status === 'Pending' ? 'selected' : ''}>Pending</option>
          <option value="In Progress" ${c.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
          <option value="Resolved" ${c.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
        </select>
      </div>
    </div>
  `).join('');

  const tendersList = document.getElementById('adminTenderList');
  tendersList.innerHTML = MSRTC_DATA.tenders.map(t => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${t.reference}</strong>
        <p style="font-size:0.85rem;">${t.title}</p>
      </div>
      <div><p>Deadline: ${t.submissionDate}</p></div>
      <div style="text-align:right;">
        <span style="color:var(--primary); font-weight:bold;">${t.status}</span>
      </div>
    </div>
  `).join('');
}

function showAddBusForm() {
  document.getElementById('addBusFormContainer').style.display = 'block';
}

function handleNewBus(event) {
  event.preventDefault();
  const id = document.getElementById('abId').value;
  const from = document.getElementById('abFrom').value;
  const to = document.getElementById('abTo').value;
  const dept = document.getElementById('abDept').value;
  
  MSRTC_DATA.buses.push({
    id, name: "Shivneri AC Volvo", type: "shivneri", from, to, dept, arr: "12:00", baseFare: 600, duration: "4h 00m", distance: "180 km", rating: 4.5, runsOn: "Daily"
  });
  document.getElementById('addBusFormContainer').style.display = 'none';
  document.getElementById('addBusForm').reset();
  renderAdminPortal();
  showToast("Bus added to database fleet", "success");
}

function removeBusFromFleet(busId) {
  MSRTC_DATA.buses = MSRTC_DATA.buses.filter(b => b.id !== busId);
  renderAdminPortal();
  showToast("Bus removed from fleet", "success");
}

function showAddRouteForm() {
  document.getElementById('addRouteFormContainer').style.display = 'block';
}

function handleNewRoute(event) {
  event.preventDefault();
  const id = document.getElementById('arId').value;
  const from = document.getElementById('arFrom').value;
  const to = document.getElementById('arTo').value;
  const via = document.getElementById('arVia').value;
  
  MSRTC_DATA.routes.push({ id, from, to, via, dailyTrips: "12 Trips", status: "Active" });
  document.getElementById('addRouteFormContainer').style.display = 'none';
  document.getElementById('addRouteForm').reset();
  renderAdminPortal();
  showToast("New route registered", "success");
}

function showAddTenderForm() {
  document.getElementById('addTenderFormContainer').style.display = 'block';
}

function handleNewTender(event) {
  event.preventDefault();
  const reference = document.getElementById('atRef').value;
  const title = document.getElementById('atTitle').value;
  const submissionDate = document.getElementById('atDate').value;
  
  MSRTC_DATA.tenders.push({ reference, title, submissionDate, status: "Open" });
  document.getElementById('addTenderFormContainer').style.display = 'none';
  document.getElementById('addTenderForm').reset();
  renderAdminPortal();
  renderPublicTenders();
  showToast("Tender notice published", "success");
}

function updateComplaintStatus(compId, val) {
  myComplaints = myComplaints.map(c => c.id === compId ? { ...c, status: val } : c);
  showToast(`Grievance status changed to ${val}`, "success");
  renderAdminPortal();
}

// Info Pages Renderers
function renderAboutSection() {
  document.getElementById('aboutHistory').innerText = MSRTC_DATA.aboutData.history;
  document.getElementById('aboutMission').innerText = MSRTC_DATA.aboutData.mission;
  document.getElementById('aboutVision').innerText = MSRTC_DATA.aboutData.vision;
  
  const container = document.getElementById('leadershipGrid');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.aboutData.leadership.map(l => `
    <div class="archive-card" style="text-align:center;">
      <div style="width:70px; height:70px; background:var(--bg-primary); border-radius:50%; display:flex; justify-content:center; align-items:center; margin:0 auto 1rem auto; font-size:1.8rem;">👤</div>
      <strong>${l.name}</strong>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.25rem;">${l.role}</p>
    </div>
  `).join('');
}

function renderDepotsList() {
  const container = document.getElementById('depotsContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.depots.map(d => `
    <div class="archive-card">
      <h4 style="color:var(--primary); margin-bottom:0.5rem;">${d.name}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem;">City: ${d.city} | Inquiries: ${d.contacts}</p>
      <p style="font-size:0.9rem;"><strong>Facilities Available:</strong> ${d.facilities}</p>
    </div>
  `).join('');
}

function filterDepotsList() {
  const query = document.getElementById('depotSearchInput').value.toLowerCase();
  const filtered = MSRTC_DATA.depots.filter(d => d.city.toLowerCase().includes(query) || d.name.toLowerCase().includes(query));
  
  const container = document.getElementById('depotsContainer');
  container.innerHTML = filtered.map(d => `
    <div class="archive-card">
      <h4 style="color:var(--primary); margin-bottom:0.5rem;">${d.name}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem;">City: ${d.city} | Inquiries: ${d.contacts}</p>
      <p style="font-size:0.9rem;"><strong>Facilities Available:</strong> ${d.facilities}</p>
    </div>
  `).join('');
}

function renderConcessionsList() {
  const container = document.getElementById('concessionsContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.concessions.map(c => `
    <div class="archive-card">
      <h4 style="color:var(--primary); margin-bottom:0.5rem;">${c.title}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem;">Eligibility: ${c.eligibility}</p>
      <p style="font-weight:bold; color:var(--seat-avail);">${c.benefit}</p>
    </div>
  `).join('');
}

function renderPublicTenders() {
  const container = document.getElementById('publicTendersContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.tenders.map(t => `
    <div class="archive-card">
      <small style="color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Ref: ${t.reference}</small>
      <h4 style="margin-bottom:0.5rem;">${t.title}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary);">Last Submission: ${t.submissionDate}</p>
      <span style="display:inline-block; background:rgba(255, 107, 0, 0.05); color:var(--primary); font-size:0.75rem; padding:0.15rem 0.4rem; border-radius:4px; font-weight:bold; margin-top:0.5rem;">${t.status}</span>
    </div>
  `).join('');
}

function renderPublicRecruitments() {
  const container = document.getElementById('publicRecruitmentsContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.recruitments.map(r => `
    <div class="archive-card">
      <small style="color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Code: ${r.code}</small>
      <h4 style="margin-bottom:0.5rem;">${r.position}</h4>
      <p style="font-size:0.85rem; color:var(--text-secondary);">Vacancies: <strong>${r.vacancies}</strong> | Last Date: ${r.lastDate}</p>
      <p style="font-size:0.9rem; margin-top:0.5rem;">Requirement: ${r.qualification}</p>
      <button class="btn-primary" style="font-size:0.8rem; padding:0.4rem 0.8rem; margin-top:1rem;" onclick="alert('Applications opening shortly.')">Apply Online</button>
    </div>
  `).join('');
}

function renderPublicCirculars() {
  const container = document.getElementById('circularsContainer');
  if (!container) return;
  container.innerHTML = MSRTC_DATA.circulars.map(c => `
    <div class="bus-card" style="padding:1rem;">
      <div>
        <strong>${c.title}</strong>
        <p style="font-size:0.8rem; color:var(--text-secondary);">${c.number}</p>
      </div>
      <div style="text-align:right;">
        <span style="font-size:0.8rem;">Date: ${c.date}</span>
        <button class="btn-secondary" style="font-size:0.75rem; margin-top:0.5rem; display:block;" onclick="alert('Downloading circular file...')">Download</button>
      </div>
    </div>
  `).join('');
}

// AI Chatbot Companion Engine
function toggleAIChat() {
  document.getElementById('aiChatWindow').classList.toggle('active');
}

function handleChatKey(event) {
  if (event.key === 'Enter') sendChatMessage();
}

function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  
  appendMessage(text, 'user');
  input.value = '';
  
  setTimeout(() => {
    const reply = getAIResponse(text);
    appendMessage(reply, 'bot');
    
    if (window.speechSynthesis) {
      const speech = new SpeechSynthesisUtterance(reply.replace(/<[^>]*>/g, ''));
      speech.lang = currentLang === 'mr' ? 'mr-IN' : currentLang === 'hi' ? 'hi-IN' : 'en-US';
      window.speechSynthesis.speak(speech);
    }
  }, 700);
}

function toggleVoiceInput() {
  voiceActive = !voiceActive;
  const input = document.getElementById('chatInput');
  
  if (voiceActive) {
    input.placeholder = "Listening to voice input...";
    setTimeout(() => {
      input.value = "Show buses to Pune";
      input.placeholder = "Ask MSRTC AI...";
      voiceActive = false;
      sendChatMessage();
    }, 2000);
  }
}

function triggerSuggestedPrompt(promptText) {
  appendMessage(promptText, 'user');
  setTimeout(() => {
    const reply = getAIResponse(promptText);
    appendMessage(reply, 'bot');
  }, 600);
}

function appendMessage(text, sender) {
  const container = document.getElementById('chatMessages');
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = text;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function getAIResponse(query) {
  const q = query.toLowerCase();
  
  if (q.includes('bus') || q.includes('pune') || q.includes('mumbai') || q.includes('schedule')) {
    return `To search for buses, please use the search panel on the Home page. We operate premium Shivneri coaches every 30 mins between Mumbai and Pune. <br><button onclick="showSection('home')" class="btn-primary" style="margin-top: 0.5rem; font-size: 0.8rem; padding: 0.3rem 0.6rem;">Go to Home Search</button>`;
  }
  if (q.includes('parcel') || q.includes('track')) {
    return `You can track parcels instantly! Go to the Parcel Services section and type 'MSR-P-992' to test. <br><button onclick="showSection('parcel')" class="btn-primary" style="margin-top:0.5rem; font-size:0.8rem; padding: 0.3rem 0.6rem;">Track Parcels</button>`;
  }
  if (q.includes('pass') || q.includes('student') || q.includes('concession')) {
    return `Student concessions receive a 66% discount. You can register for new smart cards on the dashboard's pass application panel.`;
  }
  if (q.includes('refund') || q.includes('cancel')) {
    return `All cancellations processed through the user dashboard are refunded automatically within 5-7 working days.`;
  }
  if (q.includes('depot') || q.includes('nearest')) {
    return `We connect 250+ depots across Maharashtra. The nearest major hubs are Mumbai Central Depot and Shivajinagar Pune Depot. You can filter the directory under the 'Bus Stops & Depots' tab in the navigation.`;
  }
  if (q.includes('complaint')) {
    return `You can register your grievance on our passenger portal. Select the category, add bus number details, describe the problem, and our team will resolve it. <br><button onclick="showComplaintDashboard()" class="btn-primary" style="margin-top:0.5rem; font-size:0.8rem; padding:0.3rem 0.6rem;">File Complaint</button>`;
  }
  if (q.includes('hello') || q.includes('hey') || q.includes('namaskar')) {
    return `Namaskar! I can guide you with bus timings, ticket refund policies, parcel deliveries, or pass forms. Ask me anything!`;
  }
  return `I'm here to assist you with MSRTC operations. If you need details on specific route timings, ticket booking steps, concessions or logistics tracking, let me know! You can call our Toll Free number 1800 22 1250 for urgent support.`;
}

// Redirect helpers
function openTrackBusPrompt() {
  showSection('parcel');
  switchParcelTab('track', document.querySelector('[onclick*="track"]'));
  alert("Enter simulated tracking code 'MSR-P-992' to see transit tracking.");
}

function showPassDashboard() {
  showSection('dashboard');
  switchDashboardTab('my-passes', document.querySelector('[onclick*="my-passes"]'));
}

function showComplaintDashboard() {
  showSection('dashboard');
  switchDashboardTab('my-complaints', document.querySelector('[onclick*="my-complaints"]'));
}

function showTicketsDashboard() {
  showSection('dashboard');
  switchDashboardTab('my-tickets', document.querySelector('[onclick*="my-tickets"]'));
}
