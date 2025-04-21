# feedback Route

## Overview
This document provides technical documentation for the Feedback API routes defined in `feedback.route.js`. The API exposes multiple endpoints that handle various operations related to course feedback, including retrieving feedback information, checking feedback status, submitting feedback, and managing global feedback settings.

## Base URL
All routes are prefixed with `/api/feedback` (assumed based on typical Express configuration)

## Endpoints

### Retrieve Feedback

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/faculty/:facultyId/:courseCode` | `getFeedback` | Retrieves feedback for a specific faculty member and course |

### Check Feedback Status

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/status/:userId/:courseCode/:facultyId` | `checkFeedbackStatus` | Checks if a user has submitted feedback for a specific course and faculty member |

### Submit Feedback

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/submit` | `submitFeedback` | Submits new feedback for a course and faculty member |

### Course Faculty Details

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/course/:courseCode/faculty` | `getCourseFacultyDetails` | Retrieves details of faculty members teaching a specific course |

### Course Details

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/course/:courseCode/details` | `getCourseDetails` | Retrieves details about a specific course |

### Get Global Feedback Status

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/admin/status` | `getGlobalstatus` | Retrieves the global feedback status (e.g., whether feedback collection is active) |

### Set Global Feedback Status

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/admin/set` | `setGlobalstatus` | Updates the global feedback status |

## Usage Examples

### Retrieve Feedback for a Faculty Member and Course
```javascript
// Example request
fetch('/api/feedback/faculty/F12345/CS101', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Check User Feedback Status
```javascript
// Example request
fetch('/api/feedback/status/U67890/CS101/F12345', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Feedback
```javascript
// Example request
fetch('/api/feedback/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    userId: 'U67890',
    courseCode: 'CS101',
    facultyId: 'F12345',
    ratings: {
      teaching: 5,
      knowledge: 4,
      communication: 5,
      availability: 4,
      overall: 4.5
    },
    comments: 'Excellent teaching style and very knowledgeable about the subject.'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Course Faculty Details
```javascript
// Example request
fetch('/api/feedback/course/CS101/faculty', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Course Details
```javascript
// Example request
fetch('/api/feedback/course/CS101/details', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Global Feedback Status
```javascript
// Example request
fetch('/api/feedback/admin/status', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Set Global Feedback Status
```javascript
// Example request
fetch('/api/feedback/admin/set', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    isActive: true,
    startDate: '2025-04-15T00:00:00Z',
    endDate: '2025-04-30T23:59:59Z'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Request processed successfully
- 201: Resource created successfully (for POST operations)
- 400: Bad request (invalid parameters or data)
- 401: Unauthorized (invalid or missing authentication)
- 403: Forbidden (user doesn't have required permissions)
- 404: Resource not found
- 409: Conflict (e.g., duplicate feedback submission)
- 500: Server error

## Security Considerations
- Authentication should be implemented for all routes
- Role-based access control should be enforced:
  - Admin routes should be restricted to administrators only
  - Faculty feedback retrieval should be limited to appropriate personnel
  - Students should only be able to check and submit their own feedback
- Input validation should be performed for all data submissions
- Consider implementing rate limiting to prevent abuse