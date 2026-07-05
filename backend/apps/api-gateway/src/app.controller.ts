import { Controller, Get, Query } from '@nestjs/common';

@Controller('api/v1')
export class AppController {
  @Get('buses')
  getBuses(@Query('from') from: string, @Query('to') to: string, @Query('date') date: string) {
    // Return mock data for testing the integration
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
}
