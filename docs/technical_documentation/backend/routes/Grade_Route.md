# Grade Route

## Overview
This document provides technical documentation for the Grade API routes defined in `grade.route.js`. The API exposes multiple endpoints that handle operations related to course grades, including retrieving student lists, retrieving faculty courses, and submitting grades.

## Base URL
All routes are prefixed with `/api/grades` (assumed based on typical Express configuration)

## Endpoints

### Get Students in a Course

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:courseId/getStudents` | `getStudentsinCourse` | Retrieves all students enrolled in a specific course |

### Get Faculty Courses

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/faculty/:userId/courses` | `getFacultyCourses` | Retrieves all courses taught by a specific faculty member |

### Submit Grades

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/:courseId/submitGrades` | `submitGrades` | Submits grades for students in a specific course |

## Usage Examples

### Get Students in a Course
```javascript
// Example request
fetch('/api/grades/CS101-SPRING2025/getStudents', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Faculty Courses
```javascript
// Example request
fetch('/api/grades/faculty/F12345/courses', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Grades
```javascript
// Example request
fetch('/api/grades/CS101-SPRING2025/submitGrades', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    grades: [
      {
        studentId: 'S12345',
        grade: 'A',
        marks: 92,
        comments: 'Excellent work throughout the semester'
      },
      {
        studentId: 'S12346',
        grade: 'B+',
        marks: 87,
        comments: 'Good performance, needs improvement in final projects'
      },
      // Additional student grades...
    ],
    submittedBy: 'F12345',
    submissionDate: '2025-05-15T10:30:00Z'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Expected Responses

### Get Students in a Course
```json
{
  "success": true,
  "students": [
    {
      "id": "S12345",
      "name": "John Doe",
      "email": "john.doe@example.edu",
      "enrollmentDate": "2025-01-15T00:00:00Z",
      "status": "active"
    },
    {
      "id": "S12346",
      "name": "Jane Smith",
      "email": "jane.smith@example.edu",
      "enrollmentDate": "2025-01-16T00:00:00Z",
      "status": "active"
    }
    // Additional students...
  ],
  "total": 25
}
```

### Get Faculty Courses
```json
{
  "success": true,
  "courses": [
    {
      "id": "CS101-SPRING2025",
      "name": "Introduction to Computer Science",
      "term": "Spring 2025",
      "studentsCount": 30,
      "gradesSubmitted": false
    },
    {
      "id": "CS202-SPRING2025",
      "name": "Data Structures",
      "term": "Spring 2025",
      "studentsCount": 25,
      "gradesSubmitted": true,
      "submissionDate": "2025-05-10T09:15:00Z"
    }
    // Additional courses...
  ]
}
```

### Submit Grades
```json
{
  "success": true,
  "message": "Grades successfully submitted for CS101-SPRING2025",
  "submissionId": "G12345678",
  "timestamp": "2025-05-15T10:30:00Z",
  "summary": {
    "totalStudents": 30,
    "gradesSubmitted": 30,
    "gradeDistribution": {
      "A": 8,
      "A-": 5,
      "B+": 6,
      "B": 4,
      "B-": 3,
      "C+": 2,
      "C": 1,
      "C-": 1,
      "D": 0,
      "F": 0
    }
  }
}
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Request processed successfully
- 201: Resource created successfully (for POST operations)
- 400: Bad request (invalid parameters or data)
- 401: Unauthorized (invalid or missing authentication)
- 403: Forbidden (user doesn't have required permissions)
- 404: Resource not found (e.g., course or faculty not found)
- 409: Conflict (e.g., grades already submitted)
- 500: Server error

## Security Considerations
- Authentication should be implemented for all routes
- Role-based access control should be enforced:
  - Only faculty members should be able to submit grades
  - Faculty should only be able to view courses they teach
  - Faculty should only be able to submit grades for their own courses
- Input validation should be performed for all grade submissions
- Consider implementing a review/approval workflow for grade submissions
- Implement audit logging for all grade submission activities