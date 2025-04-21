# createCourse Route

## Overview
This document provides technical documentation for the Course Creation API route defined in `createCourse.route.js`. This simple API exposes a single endpoint that handles the creation of new courses in the system.

## Base URL
All routes are prefixed with `/api/courses` (assumed based on typical Express configuration)

## Endpoints

### Course Creation

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/create-course` | `createCourse` | Create a new course in the system |

## Usage Example

### Create a New Course
```javascript
// Example request
fetch('/api/courses/create-course', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    courseCode: 'CS101',
    courseName: 'Introduction to Computer Science',
    description: 'A foundational course covering basic concepts in computer science.',
    credits: 3,
    department: 'Computer Science',
    semester: 'Fall 2025',
    instructor: '607f1f77bcf86cd799439011', // Instructor's ID
    maxCapacity: 60,
    schedule: [
      {
        day: 'Monday',
        startTime: '10:00',
        endTime: '11:30',
        location: 'Room 305, CS Building'
      },
      {
        day: 'Wednesday',
        startTime: '10:00',
        endTime: '11:30',
        location: 'Room 305, CS Building'
      }
    ],
    prerequisites: ['MATH101'],
    syllabus: 'https://storage.example.com/syllabi/cs101-fall2025.pdf'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Error Handling
The API returns appropriate HTTP status codes:
- 201: Course created successfully
- 400: Bad request (invalid course data)
- 401: Unauthorized (if authentication is required)
- 409: Conflict (e.g., course with the same code already exists)
- 500: Server error

## Security Considerations
- This endpoint should be restricted to authorized personnel only (administrators or department heads)
- Consider implementing authentication middleware to protect this route
- Input validation should be performed for all course details
- Consider implementing a review/approval workflow for new courses