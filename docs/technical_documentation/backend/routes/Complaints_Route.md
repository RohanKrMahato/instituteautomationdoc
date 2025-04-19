# Complaints Route

## Overview
This document provides comprehensive technical documentation for the Complaints Management API routes defined in `complaints.route.js`. These routes facilitate the creation, tracking, and resolution of user complaints, as well as the management of support staff.

## Base URL
All routes are prefixed with `/api/complaints` (assumed based on typical Express configuration)

## Authentication
All endpoints in this API require authentication. The `validateAccessToken` middleware is applied to every route to ensure that only authenticated users can access these endpoints.

## Endpoints

### User Complaint Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/` | `getUserComplaints` | Retrieve all complaints submitted by the authenticated user |
| POST | `/create` | `createComplaint` | Submit a new complaint |
| DELETE | `/delete` | `deleteComplaint` | Delete a user's own complaint |

### Admin Complaint Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/admin` | `getAllComplaints` | Retrieve all complaints in the system (admin only) |
| PATCH | `/admin/updateStatus` | `updateStatus` | Update the status of a complaint (e.g., pending, in progress, resolved) |
| PATCH | `/admin/assign` | `assignComplaint` | Assign a complaint to a support staff member |

### Support Staff Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/admin/supportStaff` | `createSupportStaff` | Add a new support staff member to the system |
| DELETE | `/admin/supportStaff` | `deleteSupportStaff` | Remove a support staff member from the system |
| GET | `/admin/supportStaff` | `getAllSupportStaff` | Retrieve all support staff members |
| GET | `/admin/filteredSupportStaff` | `getFilteredSupportStaff` | Get support staff filtered by specific criteria |
| PATCH | `/admin/supportStaff/availability` | `updateSupportStaffAvailability` | Update the availability status of a support staff member |

## Usage Examples

### Get User Complaints
```javascript
// Example request
fetch('/api/complaints/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Create New Complaint
```javascript
// Example request
fetch('/api/complaints/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    subject: 'Network Connectivity Issue',
    description: 'Unable to connect to campus WiFi in Building C',
    category: 'IT',
    priority: 'medium'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Admin: Update Complaint Status
```javascript
// Example request
fetch('/api/complaints/admin/updateStatus', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    complaintId: '12345',
    status: 'resolved',
    remarks: 'Issue fixed - router was reset and is now functioning properly'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Admin: Assign Complaint
```javascript
// Example request
fetch('/api/complaints/admin/assign', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    complaintId: '12345',
    staffId: '789',
    notes: 'Please check within 24 hours'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Admin: Create Support Staff
```javascript
// Example request
fetch('/api/complaints/admin/supportStaff', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    name: 'John Smith',
    email: 'jsmith@example.com',
    department: 'IT',
    specializations: ['networking', 'hardware'],
    contactNumber: '555-123-4567'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 201: Resource created successfully
- 400: Bad request (invalid parameters)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Resource not found
- 500: Server error

## Security Considerations
- All endpoints are protected by authentication middleware
- Role-based access control should be implemented:
  - Regular users should only access their own complaints
  - Admin users should have access to all complaints and staff management functions
- Input validation should be performed for all request parameters
- Consider implementing rate limiting for complaint creation