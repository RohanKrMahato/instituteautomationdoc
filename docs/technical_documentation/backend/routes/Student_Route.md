# Student Route

## Overview
This document provides technical documentation for the Student API routes defined in `student.route.js`. The API exposes multiple endpoints that handle operations related to student management, including profile management, course registration, academic requests, document applications, and fee management.

## Base URL
All routes are prefixed with `/api/student` (assumed based on typical Express configuration)

## Endpoints

### Student Profile Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id` | `getStudent` | Retrieve a student's profile information |
| PUT | `/:id/profile` | `updateStudentProfile` | Update a student's profile information |
| GET | `/:id/rollno` | `getStudentFromRollNumber` | Look up student details by roll number |

### Course Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/courses` | `getStudentCourses` | Get all courses currently registered by a student |
| GET | `/:id/completed-courses` | `getCompletedCourses` | Get all completed courses for a student |
| GET | `/:id/available-courses` | `getAvailableCourses` | Get all available courses for registration |
| GET | `/courses/:courseId` | `getCourseAnnouncements` | Get announcements for a specific course |
| GET | `/:id/performance` | `getPerformance` | Get the academic performance metrics for a student |

### Course Drop Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/:id/drop-requests` | `createCourseDropRequest` | Create a new course drop request |
| GET | `/:id/drop-requests` | `getStudentDropRequests` | Get all course drop requests for a student |
| DELETE | `/:id/drop-requests/:requestId` | `cancelDropRequest` | Cancel a pending course drop request |
| *Commented* | `/:id/courses/:courseId` | `dropCourse` | Drop a course (commented out in code) |

### Course Approval

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/:id/course-approval` | `submitCourseApprovalRequest` | Submit a new course approval request |
| GET | `/:id/pending-requests` | `getPendingRequests` | Get all pending course approval requests |

### Bonafide Certificate Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/bonafide` | `getStudentBonafideDetails` | Get student details for bonafide certificate |
| POST | `/:id/bonafide/apply` | `createBonafideApplication` | Create a new bonafide certificate application |
| GET | `/:id/bonafide/applications` | `getBonafideApplications` | Get all bonafide applications for a student |

### Passport Verification Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/passport` | `getStudentPassportDetails` | Get student details for passport verification |
| POST | `/:id/passport/apply` | `submitPassportApplication` | Submit a new passport verification application |
| GET | `/:id/passport/applications` | `getPassportApplications` | Get all passport applications for a student |

### Fee Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/fees` | `getStudentFeeDetails` | Get fee details for a student |
| POST | `/:id/fees/payment` | `recordFeePayment` | Record a fee payment |
| GET | `/:id/fees/history` | `getFeePaymentHistory` | Get fee payment history for a student |

### Announcements

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/:id/announcements` | `getAllAnnouncements` | Get all announcements relevant to a student |

## Usage Examples

### Get Student Profile
```javascript
// Example request
fetch('/api/student/S12345', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Update Student Profile
```javascript
// Example request
fetch('/api/student/S12345/profile', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    phoneNumber: '9876543210',
    address: '123 Student Housing, University Campus',
    emergencyContact: {
      name: 'Parent Name',
      relationship: 'Parent',
      phoneNumber: '1234567890'
    }
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Student Courses
```javascript
// Example request
fetch('/api/student/S12345/courses', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer <token>'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Create Course Drop Request
```javascript
// Example request
fetch('/api/student/S12345/drop-requests', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    courseId: 'CS101',
    reason: 'Schedule conflict with mandatory internship',
    supportingDocuments: ['https://example.com/documents/internship-letter.pdf']
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Apply for Bonafide Certificate
```javascript
// Example request
fetch('/api/student/S12345/bonafide/apply', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    purpose: 'Bank Loan',
    copies: 2,
    addressedTo: 'The Branch Manager, State Bank',
    deliveryMethod: 'physical',
    additionalDetails: 'Need urgently for education loan application'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Submit Passport Verification Application
```javascript
// Example request
fetch('/api/student/S12345/passport/apply', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    passportNumber: 'A1234567',
    applicantName: 'Student Full Name',
    purpose: 'International exchange program',
    verificationAddress: 'Passport Office, City Name',
    attachments: ['https://example.com/documents/passport-form.pdf']
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Record Fee Payment
```javascript
// Example request
fetch('/api/student/S12345/fees/payment', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    amount: 25000,
    paymentDate: '2025-04-15T10:30:00Z',
    paymentMethod: 'netbanking',
    transactionId: 'TXN12345678',
    bankName: 'State Bank',
    paymentFor: 'Tuition Fee - Spring 2025',
    semester: 'Spring 2025'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Expected Responses

### Student Profile
```json
{
  "success": true,
  "student": {
    "id": "S12345",
    "name": "Student Name",
    "rollNumber": "B20CS001",
    "email": "student.name@example.edu",
    "program": "B.Tech Computer Science",
    "batch": "2020-2024",
    "department": "Computer Science and Engineering",
    "currentSemester": 8,
    "dateOfBirth": "2002-05-15T00:00:00Z",
    "phoneNumber": "9876543210",
    "address": "123 Student Housing, University Campus",
    "guardian": {
      "name": "Parent Name",
      "relationship": "Parent",
      "contact": "1234567890"
    },
    "hostel": "Hostel Block A",
    "roomNumber": "A-123"
  }
}
```

### Student Courses
```json
{
  "success": true,
  "courses": [
    {
      "id": "CS101",
      "name": "Introduction to Computer Science",
      "credits": 4,
      "instructor": "Dr. Faculty Name",
      "schedule": [
        {
          "day": "Monday",
          "time": "10:00 AM - 11:30 AM",
          "location": "Lecture Hall 1"
        },
        {
          "day": "Wednesday",
          "time": "10:00 AM - 11:30 AM",
          "location": "Lecture Hall 1"
        }
      ],
      "attendance": 85.5,
      "currentGrade": "In Progress"
    },
    // Additional courses...
  ],
  "totalCredits": 16
}
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Request processed successfully
- 201: Resource created successfully (for POST operations)
- 400: Bad request (invalid parameters or data)
- 401: Unauthorized (invalid or missing authentication)
- 403: Forbidden (user doesn't have required permissions)
- 404: Resource not found (e.g., student or course not found)
- 409: Conflict (e.g., duplicate application, deadline passed)
- 500: Server error

## Security Considerations
- Authentication should be implemented for all routes
- Authorization should ensure students can only access their own data
- Input validation should be performed for all data submissions
- Security headers should be implemented to prevent common web vulnerabilities
- Rate limiting should be considered to prevent abuse
- Proper error handling should avoid exposing sensitive information