# Hostel Route

## Overview
This document provides technical documentation for the Hostel API routes defined in `hostel.route.js`. The API exposes multiple endpoints that handle operations related to hostel management, including student leaves, hostel transfers, and mess/meal subscription services.

## Base URL
All routes are prefixed with `/api/hostel` (assumed based on typical Express configuration)

## Endpoints

### Leave Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/leave` | `studentLeave` | Submit a new leave request |
| GET | `/:id/leaves` | `getStudentLeave` | Get all leave requests for a specific student |
| GET | `/leaves` | `getAllLeaves` | Get all leave requests (admin access) |
| PUT | `/leaves/:id` | `updateAnyLeave` | Update status of a leave request |

### Hostel Transfer

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/transfer` | `hostelTransfer` | Submit a new hostel transfer request |
| GET | `/:id/transfer-requests` | `getStudentTransfer` | Get all transfer requests for a specific student |
| GET | `/transfer-requests` | `getAllTransferRequests` | Get all transfer requests (admin access) |
| PUT | `/transfer-requests/:id` | `updateTransferRequest` | Update status of a transfer request |

### Mess/Meal Management

| Method | Endpoint | Controller Function | Middleware | Description |
|--------|----------|---------------------|------------|-------------|
| GET | `/mess/subscription` | `getStudentSubscriptionInfo` | validateMealAccess, isStudent | Get student's current meal subscription details |
| POST | `/mess/subscribe` | `createMealPlanRequest` | validateMealAccess, isStudent | Submit a new meal plan subscription request |
| GET | `/mess/requests/history` | `getStudentMealRequestHistory` | validateMealAccess, isStudent | Get history of meal plan requests for a student |
| GET | `/mess/admin/requests` | `getSubscriptionRequestsForAdmin` | validateMealAccess, isMealAdmin | Get all meal subscription requests (admin access) |
| PUT | `/mess/admin/requests/:requestId` | `processSubscriptionRequest` | validateMealAccess, isMealAdmin | Process (approve/reject) a meal subscription request |

## Usage Examples

### Submit a Leave Request
```javascript
// Example request
fetch('/api/hostel/leave', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    studentId: 'S12345',
    startDate: '2025-05-01T00:00:00Z',
    endDate: '2025-05-05T00:00:00Z',
    reason: 'Family event',
    destination: 'Home town',
    contactNumber: '1234567890'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Student's Leave Requests
```javascript
// Example request
fetch('/api/hostel/S12345/leaves', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get All Leave Requests (Admin)
```javascript
// Example request
fetch('/api/hostel/leaves', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Update Leave Request Status
```javascript
// Example request
fetch('/api/hostel/leaves/L67890', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    status: 'approved',
    comments: 'Approved as requested'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Hostel Transfer Request
```javascript
// Example request
fetch('/api/hostel/transfer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    studentId: 'S12345',
    currentHostel: 'Hostel A',
    requestedHostel: 'Hostel B',
    reason: 'Medical reasons requiring ground floor accommodation',
    supportingDocuments: ['https://example.com/documents/medical-certificate.pdf']
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Student's Meal Subscription Information
```javascript
// Example request
fetch('/api/hostel/mess/subscription', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Meal Plan Request
```javascript
// Example request
fetch('/api/hostel/mess/subscribe', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    planType: 'vegetarian',
    duration: 'semester',
    startDate: '2025-09-01T00:00:00Z',
    dietaryRestrictions: ['lactose-free'],
    comments: 'Prefer South Indian cuisine when available'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Process Meal Subscription Request (Admin)
```javascript
// Example request
fetch('/api/hostel/mess/admin/requests/M54321', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    status: 'approved',
    comments: 'Approved as requested',
    validFrom: '2025-09-01T00:00:00Z',
    validUntil: '2025-12-31T23:59:59Z'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Expected Responses

### Leave Request Submission
```json
{
  "success": true,
  "message": "Leave request submitted successfully",
  "leaveId": "L67890",
  "status": "pending"
}
```

### Student Leave Requests
```json
{
  "success": true,
  "leaves": [
    {
      "id": "L67890",
      "startDate": "2025-05-01T00:00:00Z",
      "endDate": "2025-05-05T00:00:00Z",
      "reason": "Family event",
      "status": "approved",
      "appliedOn": "2025-04-15T14:30:00Z",
      "approvedOn": "2025-04-16T10:15:00Z",
      "approvedBy": "Admin User"
    },
    {
      "id": "L67891",
      "startDate": "2025-03-10T00:00:00Z",
      "endDate": "2025-03-12T00:00:00Z",
      "reason": "Medical appointment",
      "status": "completed",
      "appliedOn": "2025-03-01T09:45:00Z",
      "approvedOn": "2025-03-02T11:30:00Z",
      "approvedBy": "Admin User"
    }
  ],
  "total": 2
}
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Request processed successfully
- 201: Resource created successfully (for POST operations)
- 400: Bad request (invalid parameters or data)
- 401: Unauthorized (invalid or missing authentication)
- 403: Forbidden (user doesn't have required permissions)
- 404: Resource not found
- 409: Conflict (e.g., overlapping leave or transfer requests)
- 500: Server error

## Security Considerations
- Authentication should be implemented for all routes
- Role-based access control is enforced via middleware:
  - `validateMealAccess`: Validates general access permissions for meal-related endpoints
  - `isStudent`: Ensures the user is a student
  - `isMealAdmin`: Ensures the user is a mess/meal administrator
- Admin endpoints should be protected with appropriate permissions
- Input validation should be performed for all data submissions
- Consider implementing audit logging for administrative actions