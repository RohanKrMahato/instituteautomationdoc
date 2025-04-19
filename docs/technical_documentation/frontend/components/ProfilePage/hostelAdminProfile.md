
# Hostel Admin Profile Component Documentation

## Overview
A simple React component that displays a profile dashboard for a hostel administrator. It provides a welcome message and context for managing hostel-related tasks.

## File Location
**File Name**: `HostelAdminProfile.js`

## Component Structure
- **Container**  
  `<div className="min-h-screen flex items-center justify-center bg-green-100">`  
  Centers content with a full-screen light green background.

- **Card**  
  `<div className="bg-white p-8 rounded shadow-lg w-full max-w-md">`  
  White card with padding, rounded corners, and shadow.

- **Title**  
  `<h1 className="text-2xl font-bold mb-4 text-center text-green-700">`  
  Displays "Hostel Admin Profile" in bold green text.

- **Description**  
  `<p className="text-gray-700 text-center">`  
  A brief welcome message for the hostel admin.

## Usage Example
```jsx
import HostelAdminProfile from './HostelAdminProfile';

function Dashboard() {
  return <HostelAdminProfile />;
}
```
