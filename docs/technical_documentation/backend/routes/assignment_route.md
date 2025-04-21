# Assignment Route

## Overview
This document provides comprehensive technical documentation for the Assignment Management API routes defined in `assignment.route.js`. These routes manage faculty courses, student courses, assignments, submissions, and grading.

## Base URL
All routes are prefixed with `/api/assignments` (assumed based on typical Express configuration)

## Endpoints

### User Information
Routes for retrieving user information.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:userId` | `getUser` | Get user information (faculty or general user) |
| GET | `/student/:userId` | `getStudent` | Get specific student information |

### Course Management
Routes for retrieving course information for faculty and students.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/faculty/:userId/courses` | `getFacultyCourses` | Get courses taught by a specific faculty member |
| GET | `/student/:userId/courses` | `getStudentCourses` | Get courses enrolled by a specific student |
| GET | `/course/:courseCode` | `getCourse` | Get details of a specific course by course code |

### Assignment Management
Routes for creating, retrieving, updating, and deleting assignments.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/course/:courseId/assignments` | `getCourseAssignments` | Get all assignments for a specific course |
| POST | `/course/:courseId/assignments` | `createAssignment` | Create a new assignment for a course |
| GET | `/:courseId/:assignmentId` | `getAssignmentDetails` | Get details of a specific assignment |
| PUT | `/:courseId/:assignmentId` | `editAssignmentDetails` | Update details of a specific assignment |
| DELETE | `/:courseId/:assignmentId` | `deleteAssignmentDetails` | Delete a specific assignment |

### Submission and Grading
Routes for managing assignment submissions and grades.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/:courseCode/:assignmentId/submit` | `submitAssignment` | Submit an assignment (includes file upload) |
| POST | `/:courseId/:assignmentId` | `submitGrades` | Submit grades for an assignment |
| DELETE | `/:courseCode/:assignmentId/undo/:rollNo` | `undoSubmission` | Undo/remove a student's assignment submission |

## File Upload
The API uses a middleware for file uploads:
- The `upload.middleware.js` handles file uploads for assignment submissions
- Files are processed using the `single('file')` method, indicating one file per submission

## Usage Examples

### Get Faculty Courses
```javascript
// Example request to get courses taught by a faculty member
fetch('/api/assignments/faculty/F12345/courses')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Create Assignment
```javascript
// Example request to create a new assignment
fetch('/api/assignments/course/CS101/assignments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Midterm Project',
    description: 'Create a web application using Express and MongoDB',
    dueDate: '2025-05-15T23:59:59',
    totalMarks: 100,
    weightage: 20
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Assignment
```javascript
// Example request to submit an assignment with a file
const formData = new FormData();
formData.append('file', fileObject); // fileObject is the file to be uploaded

fetch('/api/assignments/CS101/A12345/submit', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Grades
```javascript
// Example request to submit grades for an assignment
fetch('/api/assignments/CS101/A12345', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    grades: [
      { studentId: 'S12345', marks: 85, feedback: 'Good work on the project' },
      { studentId: 'S12346', marks: 92, feedback: 'Excellent implementation' }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 400: Bad request (invalid parameters)
- 401: Unauthorized
- 403: Forbidden
- 404: Resource not found
- 500: Server error

## Security Considerations
- Access to these endpoints should be restricted based on user roles (faculty vs student)
- Implement proper authentication and authorization middleware
- Validate all input parameters to prevent injection attacks
- Enforce file size and type restrictions on uploads
- Implement rate limiting to prevent abuse