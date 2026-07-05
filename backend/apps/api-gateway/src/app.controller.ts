import { Controller, Get, Post, Body, Query, Param, HttpException, HttpStatus } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';
import { MSRTC_DATA } from './data';

// In-memory data store for prototype
const users = new Map<string, any>();
const bookings = new Map<string, any[]>();
const passes = new Map<string, any[]>();
const complaints = new Map<string, any[]>();

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
    return [
      {
        id: "MSR-7731",
        name: "Shivneri AC Volvo",
        type: "shivneri",
        from: from || "Pune",
        to: to || "Mumbai",
        dept: "06:30 AM",
        arr: "10:00 AM",
        duration: "3h 30m",
        distance: "155 km",
        baseFare: 550,
        runsOn: "Daily"
      },
      {
        id: "MSR-4209",
        name: "Shivshahi Sleeper",
        type: "shivshahi",
        from: from || "Pune",
        to: to || "Mumbai",
        dept: "08:15 AM",
        arr: "12:15 PM",
        duration: "4h 00m",
        distance: "155 km",
        baseFare: 420,
        runsOn: "Daily"
      }
    ];
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
          role: body.mobile === '9876543210' ? 'admin' : 'user'
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
        role: 'user'
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
    return {
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
    
    return { success: true, booking };
  }
}
