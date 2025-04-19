# Attendance Route

## Overview
This document provides comprehensive technical documentation for the Attendance Management API routes defined in `attendance.route.js`. These routes facilitate the tracking, recording, and approval of attendance for courses, serving different user roles including students, faculty, and administrators.

## Base URL
All routes are prefixed with `/api/attendance` (assumed based on typical Express configuration)

## Endpoints

### Student Routes
Routes accessible to students for viewing their attendance information.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/student/:courseId` | `getCourse` | Get attendance information for a specific course |
| GET | `/student/` | `getPercentages` | Get attendance percentages across all courses for the logged-in student |

### Faculty Routes
Routes for faculty members to manage attendance for their courses.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/faculty/` | `getFacultyCourses` | Retrieve all courses taught by the logged-in faculty member |
| GET | `/faculty/:id` | `getStudents` | Get all students enrolled in a specific course |
| PUT | `/update/` | `modifyAttendanceRecord` | Update an existing attendance record |
| POST | `/add/` | `createAttendanceRecord` | Create a new attendance record for a student |
| POST | `/add/bulk/:id` | `createBulkAttendanceRecords` | Create attendance records for multiple students in a course |

### Admin Routes
Routes for administrators to oversee and manage attendance records.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/admin/` | `getAllCourses` | Retrieve all courses in the system |
| GET | `/admin/approval` | `getApprovalRequests` | Get attendance records pending approval |
| PATCH | `/admin/approval` | `approveAttendance` | Approve or reject pending attendance records |
| GET | `/admin/student` | `getAllStudents` | Get attendance data for all students |

## Usage Examples

### Student: View Course Attendance
```javascript
// Example request
fetch('/api/attendance/student/CS101')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Faculty: Create Attendance Record
```javascript
// Example request
fetch('/api/attendance/add/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    courseId: 'CS101',
    date: '2025-04-19',
    studentId: '2023001',
    status: 'present'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Faculty: Create Bulk Attendance Records
```javascript
// Example request
fetch('/api/attendance/add/bulk/CS101', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    date: '2025-04-19',
    records: [
      { studentId: '2023001', status: 'present' },
      { studentId: '2023002', status: 'absent' },
      { studentId: '2023003', status: 'present' }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Admin: Approve Attendance
```javascript
// Example request
fetch('/api/attendance/admin/approval', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    recordIds: ['record123', 'record456'],
    status: 'approved',
    comment: 'Verified with class records'
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
- 403: Forbidden (accessing resources without proper role)
- 404: Resource not found
- 500: Server error

## Security Considerations
- Role-based access control should be implemented to restrict access:
  - Students should only access their own attendance records
  - Faculty should only manage attendance for courses they teach
  - Admins should have oversight across all courses
- Input validation should be performed for all date fields and status values
- Authentication should be required for all endpoints
- Consider implementing audit logs for attendance modifications