# assignment route

## Overview
This document provides comprehensive technical documentation for the Assignment Management API routes defined in `assignment.route.js`. These routes facilitate the management of course assignments, submissions, and related operations for both faculty and students.

## Base URL
All routes are prefixed with `/api/assignments` (assumed based on typical Express configuration)

## Endpoints

### User Information

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:userId` | `getUser` | Get user information (works for both faculty and students) |
| GET | `/student/:userId` | `getStudent` | Get specific student information |

### Course Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/faculty/:userId/courses` | `getFacultyCourses` | Retrieve all courses taught by a specific faculty member |
| GET | `/student/:userId/courses` | `getStudentCourses` | Retrieve all courses enrolled by a specific student |
| GET | `/course/:courseCode` | `getCourse` | Get details of a specific course |

### Assignment Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/course/:courseId/assignments` | `getCourseAssignments` | Retrieve all assignments for a specific course |
| POST | `/course/:courseId/assignments` | `createAssignment` | Create a new assignment for a course |
| GET | `/:courseId/:assignmentId` | `getAssignmentDetails` | Get detailed information about a specific assignment |
| DELETE | `/:courseId/:assignmentId` | `deleteAssignmentDetails` | Delete a specific assignment |
| PUT | `/:courseId/:assignmentId` | `editAssignmentDetails` | Update the details of a specific assignment |

### Assignment Submission

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/:courseCode/:assignmentId/submit` | `submitAssignment` | Submit an assignment |
| DELETE | `/:courseCode/:assignmentId/undo/:rollNo` | `undoSubmission` | Remove a student's assignment submission |

## Usage Examples

### Get Faculty Courses
```javascript
// Example request
fetch('/api/assignments/faculty/123456/courses')
  .then(response => response.json())
  .then(courses => console.log(courses));
```

### Create Assignment
```javascript
// Example request
fetch('/api/assignments/course/CS101/assignments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Midterm Project',
    description: 'Design and implement a data structure for efficient searching',
    dueDate: '2025-05-15T23:59:59',
    totalMarks: 25,
    attachments: [
      {
        filename: 'project_guidelines.pdf',
        url: 'https://storage.example.com/files/project_guidelines.pdf'
      }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Assignment
```javascript
// Example request - using FormData for file uploads
const formData = new FormData();
formData.append('comment', 'Completed assignment as per requirements');
formData.append('submissionFile', fileObject);

fetch('/api/assignments/CS101/assign123/submit', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Delete Assignment
```javascript
// Example request
fetch('/api/assignments/CS101/assign123', {
  method: 'DELETE'
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
- 403: Forbidden (e.g., student trying to delete an assignment)
- 404: Resource not found
- 500: Server error

## Security Considerations
- Assignment creation and deletion should be restricted to faculty members
- Students should only be able to submit assignments for courses they are enrolled in
- Faculty should only be able to manage assignments for courses they teach
- Implement proper authentication and authorization middleware
- Validate all input parameters, especially file uploads
- Consider implementing file type and size restrictions for assignment submissions