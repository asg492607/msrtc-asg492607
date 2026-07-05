# MSRTC Conductor App

A React Native (Expo) application for MSRTC conductors providing:

- 🔐 Secure OTP + biometric login
- 📋 Duty roster & shift management
- 📷 QR ticket & pass validation
- 👥 Live passenger manifest
- 📍 Background GPS tracking
- 🔌 Offline-first architecture

## Getting Started

```bash
cd frontend/apps/conductor-app
npm install
npx expo start
```

Scan the QR code with **Expo Go** (Android/iOS) or press `a` for Android emulator.

## Test Credentials
- Employee ID: `EMP-1234`
- Phone: `9876543210`
- OTP: `1234`

## Architecture
- **State:** Zustand (auth) + React Query (server state)
- **API:** Typed mock client → v1 backend contracts
- **Offline:** expo-sqlite cache + background sync queue
- **GPS:** expo-location background task → Fleet Service
