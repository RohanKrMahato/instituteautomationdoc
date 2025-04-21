# facultyCourse Route

## Overview
This document provides technical documentation for the Faculty Course Management API routes defined in `facultyCourse.route.js`. These routes enable faculty members to manage course registrations and approve student enrollment in their courses.

## Base URL
All routes are prefixed with `/api/faculty-course` (assumed based on typical Express configuration)

## Endpoints

### Course Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/courses/:id` | `getFacultyCourses` | Retrieve all courses associated with a specific faculty member |
| GET | `/course-registrations/:courseCode` | `getStudentsByCourse` | Get all students who have registered for a specific course |
| POST | `/approve-registrations` | `approveRegistrations` | Approve or reject student course registration requests |

## Usage Examples

### Get Faculty Courses
```javascript
// Example request
fetch('/api/faculty-course/courses/faculty123')
  .then(response => response.json())
  .then(courses => console.log(courses));
```

### Get Course Registrations
```javascript
// Example request
fetch('/api/faculty-course/course-registrations/CS101')
  .then(response => response.json())
  .then(registrations => console.log(registrations));
```

### Approve Student Registrations
```javascript
// Example request
fetch('/api/faculty-course/approve-registrations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    courseCode: 'CS101',
    registrations: [
      { studentId: 'student123', status: 'approved' },
      { studentId: 'student456', status: 'rejected', reason: 'Prerequisites not met' }
    ]
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
- 401: Unauthorized
- 403: Forbidden (attempting to approve registrations for courses not taught by the faculty)
- 404: Resource not found (course or faculty not found)
- 500: Server error

## Security Considerations
- Ensure faculty members can only view and manage registrations for courses they teach
- Implement authentication and authorization to restrict access to appropriate faculty members
- Validate course codes and faculty IDs to prevent unauthorized access
- Consider implementing an audit log for registration approvals/rejections