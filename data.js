// Expanded MSRTC Database, Information pages, and Translations
const MSRTC_DATA = {
  locations: [
    "Mumbai (Mumbai Central)",
    "Pune (Shivajinagar)",
    "Pune (Swargate)",
    "Nashik (Thakkar Bazaar)",
    "Nagpur (Ganeshpeth)",
    "Kolhapur (CBS)",
    "Aurangabad (Chhatrapati Sambhajinagar)",
    "Solapur",
    "Thane",
    "Ratnagiri",
    "Nanded",
    "Jalgaon",
    "Ahmednagar",
    "Satara"
  ],

  depots: [
    { name: "Mumbai Central Depot", city: "Mumbai", facilities: "Waiting Lounge, AC Cloak Room, Food Plaza, Book Stalls, Drinking Water", contacts: "022-23071850" },
    { name: "Shivajinagar Depot", city: "Pune", facilities: "AC Restrooms, Charging Kiosks, Digital Inquiry Screen, Pharmacy", contacts: "020-25536631" },
    { name: "Swargate Depot", city: "Pune", facilities: "Dormitories, Escalators, Food Court, ATM, Tourist Info Desk", contacts: "020-24440017" },
    { name: "Thakkar Bazaar Depot", city: "Nashik", facilities: "Waiting Hall, Parcel Counter, Canteen, Wheelchair Assistance", contacts: "0253-2317688" },
    { name: "Ganeshpeth Depot", city: "Nagpur", facilities: "Cloak Room, Parking facility, Drinking water, Police booth", contacts: "0712-2726221" }
  ],

  busTypes: [
    { id: "shivneri", name: "Shivneri (Volvo AC)", fareMultiplier: 2.2, amenities: ["AC", "Water Bottle", "Charging Point", "WiFi", "Reclining Seats"] },
    { id: "shivshahi", name: "Shivshahi (AC Seater)", fareMultiplier: 1.5, amenities: ["AC", "Charging Point", "Reclining Seats"] },
    { id: "laldabba", name: "Parivartan (Ordinary/Lal Dabba)", fareMultiplier: 0.9, amenities: ["Standard Seats", "Window Shutters"] },
    { id: "sheetal", name: "Sheetal (Semi-Luxury)", fareMultiplier: 1.2, amenities: ["Charging Point", "Push-back Seats"] }
  ],

  buses: [
    { id: "MSR-101", name: "Shivneri AC Volvo", type: "shivneri", from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", dept: "06:00", arr: "09:30", baseFare: 550, duration: "3h 30m", distance: "150 km", rating: 4.8, runsOn: "Daily" },
    { id: "MSR-102", name: "Shivneri AC Volvo", type: "shivneri", from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", dept: "08:00", arr: "11:30", baseFare: 550, duration: "3h 30m", distance: "150 km", rating: 4.7, runsOn: "Daily" },
    { id: "MSR-103", name: "Shivshahi AC", type: "shivshahi", from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", dept: "09:15", arr: "13:00", baseFare: 380, duration: "3h 45m", distance: "150 km", rating: 4.2, runsOn: "Daily" },
    { id: "MSR-104", name: "Parivartan Ordinary", type: "laldabba", from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", dept: "10:30", arr: "14:45", baseFare: 220, duration: "4h 15m", distance: "150 km", rating: 3.9, runsOn: "Daily" },
    { id: "MSR-201", name: "Shivneri AC Volvo", type: "shivneri", from: "Pune (Shivajinagar)", to: "Mumbai (Mumbai Central)", dept: "07:00", arr: "10:30", baseFare: 550, duration: "3h 30m", distance: "150 km", rating: 4.9, runsOn: "Daily" },
    { id: "MSR-202", name: "Shivshahi AC", type: "shivshahi", from: "Pune (Shivajinagar)", to: "Mumbai (Mumbai Central)", dept: "12:00", arr: "15:45", baseFare: 380, duration: "3h 45m", distance: "150 km", rating: 4.1, runsOn: "Daily" },
    { id: "MSR-301", name: "Shivneri AC Volvo", type: "shivneri", from: "Mumbai (Mumbai Central)", to: "Nashik (Thakkar Bazaar)", dept: "06:30", arr: "10:30", baseFare: 620, duration: "4h 00m", distance: "170 km", rating: 4.6, runsOn: "Daily" },
    { id: "MSR-401", name: "Shivshahi AC", type: "shivshahi", from: "Pune (Swargate)", to: "Kolhapur (CBS)", dept: "06:15", arr: "11:30", baseFare: 480, duration: "5h 15m", distance: "230 km", rating: 4.4, runsOn: "Daily" }
  ],

  routes: [
    { id: "R-50", from: "Mumbai", to: "Pune", via: "Lonavala, Pimpri", dailyTrips: "48 Trips", status: "Active" },
    { id: "R-52", from: "Mumbai", to: "Nashik", via: "Thane, Kasara, Igatpuri", dailyTrips: "24 Trips", status: "Active" },
    { id: "R-60", from: "Pune", to: "Aurangabad", via: "Shirur, Ahmednagar", dailyTrips: "18 Trips", status: "Active" },
    { id: "R-72", from: "Pune", to: "Kolhapur", via: "Satara, Karad", dailyTrips: "32 Trips", status: "Active" }
  ],

  tenders: [
    { reference: "MSRTC/MECH/2026/09", title: "Procurement of 500 Lithium-Ion Battery Packs for E-Buses", submissionDate: "August 15, 2026", status: "Open" },
    { reference: "MSRTC/CIVIL/2026/04", title: "Modernization of Swargate Bus Station (Phase II)", submissionDate: "July 30, 2026", status: "Open" },
    { reference: "MSRTC/IT/2026/12", title: "Design, Development and Hosting of Cloud Unified Mobile Application", submissionDate: "August 05, 2026", status: "Open" }
  ],

  recruitments: [
    { code: "REC/2026/01", position: "Assistant Depot Manager (Operations)", vacancies: 45, qualification: "MBA / Degree in Transport Studies", lastDate: "July 25, 2026" },
    { code: "REC/2026/02", position: "Junior Engineer (Mechanical/Automobile)", vacancies: 120, qualification: "B.E/B.Tech in Automobile/Mechanical Engineering", lastDate: "August 02, 2026" },
    { code: "REC/2026/03", position: "Direct Driver-cum-Conductor Cadre 2026", vacancies: 8500, qualification: "10th Standard Pass + Valid Heavy Motor Vehicle License", lastDate: "September 10, 2026" }
  ],

  circulars: [
    { number: "CIR-2026/41", title: "Revision of luggage carriage rules & limits for Shivshahi AC buses", date: "July 01, 2026" },
    { number: "CIR-2026/38", title: "Introduction of UPI payments at physical booking counters in rural depots", date: "June 15, 2026" },
    { number: "CIR-2026/32", title: "Rules governing concession pass verification for senior citizens above 75", date: "May 29, 2026" }
  ],

  concessions: [
    { title: "Amrut Jyeshtha Nagarik", benefit: "100% Free travel in Ordinary, Semi-Luxury, & AC Shivshahi", eligibility: "Maharashtra Resident age 75+" },
    { title: "Student Pass (School/College)", benefit: "66% Concession on daily tickets between home and school", eligibility: "Students up to post-graduation" },
    { title: "Divyang Concession Scheme", benefit: "75% Concession for disabled person + 50% Concession for companion", eligibility: "Valid Medical Disability certificate holder" }
  ],

  popularRoutes: [
    { from: "Mumbai (Mumbai Central)", to: "Pune (Shivajinagar)", fare: "₹550", time: "3.5 hrs" },
    { from: "Pune (Shivajinagar)", to: "Aurangabad (Chhatrapati Sambhajinagar)", fare: "₹490", time: "5.25 hrs" },
    { from: "Mumbai (Mumbai Central)", to: "Nashik (Thakkar Bazaar)", fare: "₹420", time: "4.25 hrs" },
    { from: "Pune (Swargate)", to: "Kolhapur (CBS)", fare: "₹480", time: "5.25 hrs" }
  ],

  announcements: [
    { title: "Ashadhi Ekadashi Special Buses", desc: "MSRTC is launching 5,000 additional special buses to Pandharpur starting July 10th.", date: "July 04, 2026" },
    { title: "Route Diversion near Mumbai-Pune Expressway", desc: "Due to maintenance work near Khandala Ghat, Shivneri buses might be delayed by 20-30 mins.", date: "July 03, 2026" }
  ],

  news: [
    { title: "MSRTC updates environmental standard to BS-VI", desc: "100 new eco-friendly electric buses added to Mumbai-Pune sector." },
    { title: "Direct Shivneri Cargo Services Launched", desc: "Same-day parcel delivery launched between Nagpur, Aurangabad, and Mumbai." }
  ],

  faqs: [
    { q: "How do I claim a refund for a cancelled transaction?", a: "Refunds are processed automatically to the original source of payment within 5-7 working days. You can track status on the Payments tab." },
    { q: "Are senior citizens eligible for any ticket concession?", a: "Yes, Maharashtra residents aged 65 and above are eligible for a 50% fare concession, and citizens above 75 can travel for free on ordinary and semi-luxury buses with a valid Aadhaar/Smart Card pass." }
  ],

  aboutData: {
    history: "Formed in 1948 under the Road Transport Corporation Act, the Maharashtra State Road Transport Corporation (MSRTC) serves as the primary public transport network connecting every village, town, and city across Maharashtra with over 15,000 buses.",
    mission: "To provide safe, reliable, comfortable, affordable, and accessible transport solutions to the passengers of Maharashtra, acting as a true lifeline for the state.",
    vision: "To transform rural and urban connectivity with environmental sustainability, modern AI fleet management, and clean user experience.",
    leadership: [
      { name: "Hon. Shri. Eknath Shinde", role: "Chief Minister & President, MSRTC" },
      { name: "Shri. Madhav Kusekar, IAS", role: "Vice Chairman & Managing Director" }
    ]
  },

  translations: {
    en: {
      appName: "MSRTC Smart Digital Transport Platform",
      tagline: "Lifeline of Maharashtra - Digitized for your Comfort",
      searchBus: "Search Buses",
      bookTickets: "Book Tickets",
      trackBus: "Track Bus",
      busSchedule: "Bus Schedule",
      parcelServices: "Parcel Services",
      latestUpdates: "Latest Updates",
      aboutUs: "About Us",
      faq: "FAQs",
      contactUs: "Contact Us",
      login: "Login / Sign Up",
      logout: "Logout",
      dashboard: "Dashboard",
      applyPass: "Bus Passes",
      complaintPortal: "Complaints",
      adminPortal: "Admin Portal",
      from: "From",
      to: "To",
      date: "Journey Date",
      searchBtn: "Search Buses",
      popularRoutes: "Popular Routes",
      emergencyAnnouncements: "Emergency Announcements & Diversions",
      latestNews: "Latest Updates & Press Releases",
      viewAll: "View All",
      bookNow: "Book Now",
      seatsLeft: "seats left",
      busDetails: "Bus Details & Route Information",
      selectSeats: "Select Seats",
      passengerDetails: "Passenger Details",
      payment: "Payment Portal",
      success: "Booking Successful",
      pnr: "PNR No",
      busNo: "Bus No",
      seatNo: "Seat No(s)",
      totalFare: "Total Fare",
      downloadPdf: "Download PDF Ticket",
      voiceChatHint: "Ask me 'Buses to Pune' or 'Track parcel MSR-P-992'",
      chatPlaceholder: "Ask MSRTC AI...",
      submit: "Submit",
      apply: "Apply",
      track: "Track",
      home: "Home",
      parcelRates: "Parcel Rate Calculator",
      adminTitle: "MSRTC Admin Panel",
      statistics: "Live Operational Statistics",
      busStopsDepots: "Bus Stops & Depots",
      tendersList: "Active Tenders",
      recruitmentList: "Recruitment Opportunities",
      actsRules: "Acts & Rules",
      circularsList: "Department Circulars",
      citizenCharter: "Citizen Charter",
      achievements: "Key Achievements"
    },
    mr: {
      appName: "एस.टी. महामंडळ डिजिटल प्लॅटफॉर्म",
      tagline: "महाराष्ट्राची जीवनवाहिनी - आता अधिक सुलभ आणि डिजिटल",
      searchBus: "बस शोधा",
      bookTickets: "तिकीट बुकिंग",
      trackBus: "बस ट्रॅकिंग",
      busSchedule: "बस वेळापत्रक",
      parcelServices: "पार्सल सेवा",
      latestUpdates: "नवीन घडामोडी",
      aboutUs: "आमच्याबद्दल",
      faq: "वारंवार विचारले जाणारे प्रश्न",
      contactUs: "संपर्क साधा",
      login: "लॉगिन / नोंदणी",
      logout: "बाहेर पडा",
      dashboard: "डॅशबोर्ड",
      applyPass: "बस पासेस",
      complaintPortal: "तक्रार निवारण",
      adminPortal: "प्रशासक पोर्टल",
      from: "कुठून",
      to: "कुठे",
      date: "प्रवासाची तारीख",
      searchBtn: "बस शोधा",
      popularRoutes: "लोकप्रिय मार्ग",
      emergencyAnnouncements: "तातडीच्या घोषणा आणि मार्ग बदल",
      latestNews: "नवीनतम बातम्या आणि प्रसिद्धीपत्रके",
      viewAll: "सर्व पहा",
      bookNow: "आरक्षण करा",
      seatsLeft: "जागा शिल्लक",
      busDetails: "बस तपशील आणि मार्ग माहिती",
      selectSeats: "जागा निवडा",
      passengerDetails: "प्रवासी तपशील",
      payment: "पेमेंट पोर्टल",
      success: "बुकिंग यशस्वी झाले",
      pnr: "पी.एन.आर क्रमांक",
      busNo: "बस क्रमांक",
      seatNo: "सीट क्रमांक",
      totalFare: "एकूण भाडे",
      downloadPdf: "पीडीएफ तिकीट डाउनलोड करा",
      voiceChatHint: "मला विचार 'पुण्यासाठी बसेस' किंवा 'पार्सल ट्रॅक करा MSR-P-992'",
      chatPlaceholder: "एस.टी. मदतनीसला विचारा...",
      submit: "सबमिट करा",
      apply: "अर्ज करा",
      track: "ट्रॅक करा",
      home: "मुख्यपृष्ठ",
      parcelRates: "पार्सल दर कॅल्क्युलेटर",
      adminTitle: "एस.टी. महामंडळ प्रशासक नियंत्रण",
      statistics: "थेट ऑपरेशन्स आकडेवारी",
      busStopsDepots: "बस थांबे आणि डेपो",
      tendersList: "सक्रिय निविदा",
      recruitmentList: "भरती प्रक्रिया",
      actsRules: "कायदे आणि नियम",
      circularsList: "विभागीय परिपत्रके",
      citizenCharter: "नागरिक सनद",
      achievements: "प्रमुख यश"
    },
    hi: {
      appName: "एमएसआरटीसी स्मार्ट डिजिटल ट्रांसपोर्ट",
      tagline: "महाराष्ट्र की जीवनरेखा - आपकी सुविधा के लिए डिजिटल",
      searchBus: "बस खोजें",
      bookTickets: "टिकट बुकिंग",
      trackBus: "बस ट्रैकिंग",
      busSchedule: "बस समय सारणी",
      parcelServices: "पार्सल सेवाएं",
      latestUpdates: "नवीनतम अपडेट",
      aboutUs: "हमारे बारे में",
      faq: "अक्सर पूछे जाने वाले प्रश्न",
      contactUs: "संपर्क करें",
      login: "लॉगिन / साइन अप",
      logout: "लॉगआउट",
      dashboard: "डैशबोर्ड",
      applyPass: "बस पास",
      complaintPortal: "शिकायत पोर्टल",
      adminPortal: "एडमिन पोर्टल",
      from: "कहाँ से",
      to: "कहाँ तक",
      date: "यात्रा की तिथि",
      searchBtn: "बस खोजें",
      popularRoutes: "लोकप्रिय मार्ग",
      emergencyAnnouncements: "आपातकालीन घोषणाएं और मार्ग परिवर्तन",
      latestNews: "नवीनतम समाचार और सूचनाएं",
      viewAll: "सभी देखें",
      bookNow: "बुकिंग करें",
      seatsLeft: "सीटें खाली हैं",
      busDetails: "बस विवरण और मार्ग की जानकारी",
      selectSeats: "सीटें चुनें",
      passengerDetails: "यात्री विवरण",
      payment: "भुगतान पोर्टल",
      success: "बुकिंग सफल रही",
      pnr: "पीएनआर नंबर",
      busNo: "बस नंबर",
      seatNo: "सीट नंबर",
      totalFare: "कुल किराया",
      downloadPdf: "पीडीएफ टिकट डाउनलोड करें",
      voiceChatHint: "मुझसे पूछें 'पुणे के लिए बसें' या 'पार्सल ट्रैक MSR-P-992'",
      chatPlaceholder: "एमएसआरटीसी एआई से पूछें...",
      submit: "जमा करें",
      apply: "आवेदन करें",
      track: "ट्रैक करें",
      home: "मुख्यपृष्ठ",
      parcelRates: "पार्सल दर कैलकुलेटर",
      adminTitle: "एमएसआरटीसी एडमिन पैनल",
      statistics: "लाइव परिचालन आंकड़े",
      busStopsDepots: "बस स्टॉप और डिपो",
      tendersList: "सक्रिय निविदाएं",
      recruitmentList: "भर्ती के अवसर",
      actsRules: "अधिनियम और नियम",
      circularsList: "विभागीय परिपत्र",
      citizenCharter: "नागरिक चार्टर",
      achievements: "प्रमुख उपलब्धियां"
    }
  }
};
