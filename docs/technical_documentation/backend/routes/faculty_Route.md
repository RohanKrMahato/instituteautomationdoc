# faculty Route


## Overview
This document provides comprehensive technical documentation for the Faculty API routes defined in `faculty.route.js`. These routes facilitate faculty interactions with the system, including course management, announcements, student information, and request approvals.

## Base URL
All routes are prefixed with `/api/faculty` (assumed based on typical Express configuration)

## Endpoints

### Faculty Information

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id` | `getFaculty` | Retrieve information about a specific faculty member |

### Course Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/courses` | `getFacultyCourses` | Get all courses taught by a specific faculty member |
| GET | `/:id/dashboard-courses` | `getFacultyDashboardCourses` | Get courses formatted for the faculty dashboard |
| GET | `/courses/:courseId/students` | `getCourseStudents` | Get all students enrolled in a specific course |

### Announcements Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/announcements` | `getFacultyAnnouncements` | Get all announcements made by a faculty member |
| GET | `/courses/:courseId/announcements` | `getCourseAnnouncements` | Get all announcements for a specific course |
| POST | `/courses/:courseId/announcements/add` | `addCourseAnnouncement` | Create a new announcement for a course |
| PUT | `/courses/:courseId/announcements/:announcementId/update` | `updateCourseAnnouncement` | Update an existing course announcement |
| DELETE | `/courses/:courseId/announcements/:announcementId/delete` | `deleteCourseAnnouncement` | Delete a course announcement |

### Request Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/pending-requests-approval` | `getPendingRequestsFaculty` | Get all pending requests that require faculty approval |
| PUT | `/approval-requests/:requestId` | `handleRequestApprovalFaculty` | Approve or reject a pending request |

## Usage Examples

### Get Faculty Information
```javascript
// Example request
fetch('/api/faculty/faculty123')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Faculty Courses
```javascript
// Example request
fetch('/api/faculty/faculty123/courses')
  .then(response => response.json())
  .then(courses => console.log(courses));
```

### Add Course Announcement
```javascript
// Example request
fetch('/api/faculty/courses/CS101/announcements/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Midterm Date Change',
    content: 'The midterm exam has been rescheduled to next Friday, April 26th.',
    priority: 'high',
    attachments: [
      {
        name: 'updated_syllabus.pdf',
        url: 'https://storage.example.com/files/updated_syllabus.pdf'
      }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Course Students
```javascript
// Example request
fetch('/api/faculty/courses/CS101/students')
  .then(response => response.json())
  .then(students => console.log(students));
```

### Handle Request Approval
```javascript
// Example request
fetch('/api/faculty/approval-requests/req123', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    status: 'approved',
    comments: 'Student has valid reasons for extension.'
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
- 403: Forbidden (attempting to access/modify resources of another faculty)
- 404: Resource not found
- 500: Server error

## Security Considerations
- All endpoints should verify that the authenticated user has faculty privileges
- Ensure faculty members can only access/modify data related to courses they teach
- Faculty members should only be able to approve/reject requests directed to them
- Consider implementing middleware to validate faculty permissions before processing requests
- Validate all input data, especially for announcement creation and updates