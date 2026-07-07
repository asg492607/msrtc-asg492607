import { Controller, Get, Post, Put, Delete, Body, Query, Param, HttpException, HttpStatus } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';
import { MSRTC_DATA } from './data';

// In-memory data store for prototype
const users = new Map<string, any>();
const bookings = new Map<string, any[]>();
const passes = new Map<string, any[]>();
const complaints = new Map<string, any[]>();
const parcels = new Map<string, any>();

@Controller('api/v1')
export class AppController {
  
  // ----------------------------------------------------
  // DATA
  // ----------------------------------------------------
  @Get('data/all')
  getAllData() {
    return MSRTC_DATA;
  }

  // ----------------------------------------------------
  // BUSES
  // ----------------------------------------------------
  @Get('buses')
  getBuses(@Query('from') from: string, @Query('to') to: string, @Query('date') date: string) {
    // Dynamic logic for generating buses based on input
    const origin = from || 'Pune';
    const destination = to || 'Mumbai';
    
    // Generate some deterministic but dynamic-looking results based on the route
    const isLongRoute = origin.length + destination.length > 12;
    
    const results = [
      {
        id: `MSR-${Math.floor(1000 + Math.random() * 8000)}`,
        name: "Shivneri AC Volvo",
        type: "shivneri",
        from: origin,
        to: destination,
        dept: "06:30 AM",
        arr: isLongRoute ? "02:30 PM" : "10:00 AM",
        duration: isLongRoute ? "8h 00m" : "3h 30m",
        distance: isLongRoute ? "450 km" : "155 km",
        baseFare: isLongRoute ? 1200 : 550,
        runsOn: "Daily"
      },
      {
        id: `MSR-${Math.floor(1000 + Math.random() * 8000)}`,
        name: "Shivshahi Sleeper",
        type: "shivshahi",
        from: origin,
        to: destination,
        dept: "08:15 AM",
        arr: isLongRoute ? "05:15 PM" : "12:15 PM",
        duration: isLongRoute ? "9h 00m" : "4h 00m",
        distance: isLongRoute ? "450 km" : "155 km",
        baseFare: isLongRoute ? 950 : 420,
        runsOn: "Daily"
      },
      {
        id: `MSR-${Math.floor(1000 + Math.random() * 8000)}`,
        name: "Lal Pari (Ordinary)",
        type: "ordinary",
        from: origin,
        to: destination,
        dept: "10:00 AM",
        arr: isLongRoute ? "08:00 PM" : "02:30 PM",
        duration: isLongRoute ? "10h 00m" : "4h 30m",
        distance: isLongRoute ? "450 km" : "155 km",
        baseFare: isLongRoute ? 400 : 180,
        runsOn: "Daily"
      }
    ];
    
    return results;
  }

  // ----------------------------------------------------
  // AUTHENTICATION
  // ----------------------------------------------------
  @Post('auth/register')
  register(@Body() body: { name: string, mobile: string }) {
    if (!body.name || !body.mobile) {
      throw new HttpException('Name and mobile required', HttpStatus.BAD_REQUEST);
    }
    if (users.has(body.mobile)) {
      throw new HttpException('User already exists', HttpStatus.CONFLICT);
    }
    
    const user = {
      id: uuidv4(),
      name: body.name,
      mobile: body.mobile,
      role: 'user'
    };
    
    users.set(body.mobile, user);
    bookings.set(body.mobile, []); // Initialize empty lists
    passes.set(body.mobile, []);
    complaints.set(body.mobile, []);
    
    return { success: true, user };
  }

  @Post('auth/login')
  login(@Body() body: { method: string, mobile?: string, email?: string, password?: string, otp?: string }) {
    if (body.method === 'otp') {
      if (body.otp !== '1234') {
        throw new HttpException('Invalid OTP', HttpStatus.UNAUTHORIZED);
      }
      
      let user = users.get(body.mobile);
      if (!user) {
        // Auto-register on OTP login if not exists for prototype convenience
        user = {
          id: uuidv4(),
          name: body.mobile === '9876543210' ? 'System Admin' : 'Guest User',
          mobile: body.mobile,
          role: body.mobile === '9876543210' ? 'admin' : 'user',
          walletBalance: 1500
        };
        users.set(body.mobile, user);
        bookings.set(body.mobile, []);
        passes.set(body.mobile, []);
        complaints.set(body.mobile, []);
      }
      return { success: true, user };
    } else {
      // Email login mock
      if (!body.email || !body.password) {
        throw new HttpException('Invalid credentials', HttpStatus.UNAUTHORIZED);
      }
      // Mock existing user for email login
      const user = {
        id: uuidv4(),
        name: 'Email User',
        mobile: '9938210398',
        role: 'user',
        walletBalance: 1500
      };
      if (!users.has('9938210398')) {
        users.set('9938210398', user);
        bookings.set('9938210398', []);
      }
      return { success: true, user };
    }
  }

  // ----------------------------------------------------
  // DASHBOARD
  // ----------------------------------------------------
  @Get('users/:mobile/dashboard')
  getDashboard(@Param('mobile') mobile: string) {
    if (!users.has(mobile)) {
      throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    }
    const user = users.get(mobile);
    return {
      user: {
        id: user.id,
        name: user.name,
        mobile: user.mobile,
        walletBalance: user.walletBalance || 0
      },
      bookings: bookings.get(mobile) || [],
      passes: passes.get(mobile) || [],
      complaints: complaints.get(mobile) || []
    };
  }

  // ----------------------------------------------------
  // BOOKINGS
  // ----------------------------------------------------
  @Post('bookings')
  createBooking(@Body() body: { mobile: string, from: string, to: string, busNo: string, seats: string[], date: string, fare: number }) {
    if (!users.has(body.mobile)) {
      throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    }
    
    const pnr = "PNR" + Math.floor(100000000 + Math.random() * 900000000);
    const booking = {
      pnr,
      from: body.from,
      to: body.to,
      busNo: body.busNo,
      seats: body.seats,
      date: body.date,
      fare: body.fare,
      status: "Active",
      createdAt: new Date().toISOString()
    };
    
    const userBookings = bookings.get(body.mobile) || [];
    userBookings.unshift(booking);
    bookings.set(body.mobile, userBookings);
    
    const user = users.get(body.mobile);
    if (body.paymentMethod === 'wallet') {
      if (user.walletBalance < body.fare) {
        throw new HttpException('Insufficient wallet balance', HttpStatus.BAD_REQUEST);
      }
      user.walletBalance -= body.fare;
      users.set(body.mobile, user);
    }
    
    return { success: true, booking, newWalletBalance: user.walletBalance };
  }

  // ----------------------------------------------------
  // PASSES
  // ----------------------------------------------------
  @Post('passes')
  applyPass(@Body() body: { mobile: string, passType: string, duration: string, startFrom: string }) {
    if (!users.has(body.mobile)) {
      throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    }
    
    const pass = {
      id: "PASS" + Math.floor(100000 + Math.random() * 900000),
      type: body.passType,
      duration: body.duration,
      startFrom: body.startFrom,
      status: "Processing",
      createdAt: new Date().toISOString()
    };
    
    const userPasses = passes.get(body.mobile) || [];
    userPasses.unshift(pass);
    passes.set(body.mobile, userPasses);
    
    return { success: true, pass };
  }

  // ----------------------------------------------------
  // COMPLAINTS
  // ----------------------------------------------------
  @Post('complaints')
  fileComplaint(@Body() body: { mobile: string, category: string, description: string, pnr?: string }) {
    if (!users.has(body.mobile)) {
      throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    }
    
    const complaint = {
      id: "GRV" + Math.floor(10000 + Math.random() * 90000),
      category: body.category,
      description: body.description,
      pnr: body.pnr,
      status: "Open",
      createdAt: new Date().toISOString()
    };
    
    const userComplaints = complaints.get(body.mobile) || [];
    userComplaints.unshift(complaint);
    complaints.set(body.mobile, userComplaints);
    
    return { success: true, complaint };
  }

  // ----------------------------------------------------
  // PARCELS
  // ----------------------------------------------------
  @Get('parcels/:id')
  trackParcel(@Param('id') id: string) {
    if (parcels.has(id)) {
      return parcels.get(id);
    }
    
    // Mock response for any parcel ID
    const mockParcel = {
      id: id,
      status: 'In Transit',
      origin: 'Mumbai Central',
      destination: 'Pune Swargate',
      currentLocation: 'Lonavala Hub',
      estimatedDelivery: 'Tomorrow, 10:00 AM',
      timeline: [
        { status: 'Booked', time: 'Yesterday, 04:00 PM', location: 'Mumbai Central' },
        { status: 'Dispatched', time: 'Yesterday, 08:30 PM', location: 'Mumbai Central' },
        { status: 'In Transit', time: 'Today, 02:15 AM', location: 'Lonavala Hub' }
      ]
    };
    
    parcels.set(id, mockParcel);
    return mockParcel;
  }
  // ----------------------------------------------------
  // BOOKING CANCELLATION
  // ----------------------------------------------------
  @Delete('bookings/:pnr')
  cancelBooking(@Param('pnr') pnr: string) {
    let cancelled = false;
    let refundedAmount = 0;
    let targetMobile = null;
    
    // Iterate over all users' bookings
    for (const [mobile, userBookings] of bookings.entries()) {
      const booking = userBookings.find(b => b.pnr === pnr);
      if (booking && booking.status === 'Active') {
        booking.status = 'Cancelled';
        cancelled = true;
        refundedAmount = booking.fare;
        targetMobile = mobile;
        break;
      }
    }
    
    if (cancelled && targetMobile) {
      const user = users.get(targetMobile);
      if (user) {
        user.walletBalance = (user.walletBalance || 0) + refundedAmount;
        users.set(targetMobile, user);
      }
    }
    
    if (!cancelled) {
      throw new HttpException('Booking not found', HttpStatus.NOT_FOUND);
    }
    return { success: true, message: 'Booking cancelled successfully' };
  }

  // ----------------------------------------------------
  // ADMIN PORTAL ENDPOINTS
  // ----------------------------------------------------
  @Get('admin/bookings')
  getAllBookings() {
    const all = [];
    for (const [mobile, userBookings] of bookings.entries()) {
      all.push(...userBookings.map(b => ({ ...b, userMobile: mobile })));
    }
    return all.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }

  @Get('admin/complaints')
  getAllComplaints() {
    const all = [];
    for (const [mobile, userComplaints] of complaints.entries()) {
      all.push(...userComplaints.map(c => ({ ...c, userMobile: mobile })));
    }
    return all.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }

  @Get('admin/passes')
  getAllPasses() {
    const all = [];
    for (const [mobile, userPasses] of passes.entries()) {
      all.push(...userPasses.map(p => ({ ...p, userMobile: mobile })));
    }
    return all.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }

  @Put('admin/passes/:id/status')
  updatePassStatus(@Param('id') id: string, @Body('status') status: string) {
    let updated = false;
    for (const [mobile, userPasses] of passes.entries()) {
      const pass = userPasses.find(p => p.id === id);
      if (pass) {
        pass.status = status;
        updated = true;
        break;
      }
    }
    if (!updated) {
      throw new HttpException('Pass not found', HttpStatus.NOT_FOUND);
    }
    return { success: true };
  }

  @Put('admin/complaints/:id/status')
  updateComplaintStatus(@Param('id') id: string, @Body('status') status: string) {
    let updated = false;
    for (const [mobile, userComplaints] of complaints.entries()) {
      const complaint = userComplaints.find(c => c.id === id);
      if (complaint) {
        complaint.status = status;
        updated = true;
        break;
      }
    }
    if (!updated) {
      throw new HttpException('Complaint not found', HttpStatus.NOT_FOUND);
    }
    return { success: true };
  }

  @Put('admin/passes/:id/status')
  updatePassStatus(@Param('id') id: string, @Body('status') status: string) {
    let updated = false;
    for (const [mobile, userPasses] of passes.entries()) {
      const pass = userPasses.find(p => p.id === id);
      if (pass) {
        pass.status = status;
        updated = true;
        break;
      }
    }
    if (!updated) throw new HttpException('Pass not found', HttpStatus.NOT_FOUND);
    return { success: true };
  }
}
