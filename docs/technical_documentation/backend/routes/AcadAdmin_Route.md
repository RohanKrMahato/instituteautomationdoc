# AcadAdmin Route

## Overview
This document provides comprehensive technical documentation for the Academic Administration API routes defined in `acadAdmin.route.js`. These routes manage document applications, course drop requests, fee structures, student document access controls, student/faculty management, announcements, and department information.

## Base URL
All routes are prefixed with `/api/acadAdmin` (assumed based on typical Express configuration)

## Endpoints

### Document Management
Routes for handling document applications such as transcripts, certificates, etc.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/documents/applications` | `getAllApplications` | Retrieve all document applications |
| GET | `/documents/applications/filter` | `filterApplications` | Filter applications by specified criteria |
| GET | `/documents/applications/:id` | `getApplicationById` | Get a specific application by ID |
| PATCH | `/documents/applications/:id/status` | `updateApplicationStatus` | Update the status of an application |
| POST | `/documents/applications/:id/comment` | `addComment` | Add a comment to a specific application |

### Course Drop Request Management
Routes for handling student course drop requests.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/drop-requests` | `getDropRequests` | Retrieve all course drop requests |
| GET | `/drop-requests/:requestId` | `updateDropRequestStatus` | Get a specific drop request |
| PATCH | `/drop-requests/:requestId` | `updateDropRequestStatus` | Update status/remarks of a drop request |

### Fee Management
Routes for managing fee structures and breakdowns.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/feeControl/addFee` | `addFeeStructure` | Create a new fee structure |
| GET | `/feeControl/getFeeBreakdown` | `getFeeBreakdown` | Retrieve fee breakdown information |
| PATCH | `/feeControl/toggleStatus/:id` | `toggleFeeBreakdownStatus` | Toggle the active status of a fee breakdown |
| PUT | `/feeControl/updateFee/:id` | `updateFeeBreakdown` | Update an existing fee breakdown |

### Document Access Control
Routes for managing student access to academic documents.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/students/document-access` | `getStudentsWithDocumentAccess` | Get all students with their document access settings |
| PATCH | `/students/:id/document-access` | `updateStudentDocumentAccess` | Update document access for a specific student |
| POST | `/students/bulk-document-access` | `bulkUpdateDocumentAccess` | Update document access for multiple students at once |

### Student Management
Routes for managing student records.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/students/add-students` | `addStudents` | Add new students to the system |

### Faculty Management
Routes for managing faculty records.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/faculty/add-faculty` | `addFaculty` | Add new faculty members to the system |

### Announcement Management
Routes for creating and managing administrative announcements.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/announcements` | `getAdminAnnouncements` | Get all announcements created by admin |
| POST | `/announcements/add` | `addAnnouncement` | Create a new announcement |
| PUT | `/announcements/:announcementId/update` | `updateAnnouncement` | Update an existing announcement |
| DELETE | `/announcements/:announcementId/delete` | `deleteAnnouncement` | Delete an announcement |

### Department Information
Routes for accessing department data.

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| GET | `/departments` | `getAllDepartments` | Get all departments in the institution |

## Usage Examples

### Get All Applications
```javascript
// Example request
fetch('/api/acadAdmin/documents/applications')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Update Application Status
```javascript
// Example request
fetch('/api/acadAdmin/documents/applications/123456/status', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    status: 'approved',
    remarks: 'Application approved by registrar'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Add Students
```javascript
// Example request
fetch('/api/acadAdmin/students/add-students', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    students: [
      {
        name: 'John Doe',
        email: 'john.doe@example.com',
        rollNo: 'R2025001',
        department: 'Computer Science',
        program: 'Bachelor of Science',
        semester: 1,
        contactNo: '1234567890'
      },
      {
        name: 'Jane Smith',
        email: 'jane.smith@example.com',
        rollNo: 'R2025002',
        department: 'Electrical Engineering',
        program: 'Bachelor of Engineering',
        semester: 1,
        contactNo: '0987654321'
      }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Add Announcement
```javascript
// Example request
fetch('/api/acadAdmin/announcements/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Spring Semester Registration',
    content: 'Registration for Spring 2025 semester will begin on May 1, 2025.',
    priority: 'high',
    audience: ['all'],
    validUntil: '2025-05-15T23:59:59'
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
- Access to these endpoints should be restricted to authorized academic administrators
- Implement proper authentication and authorization middleware
- Validate all input parameters to prevent injection attacks
- Implement rate limiting to prevent abuse
- Ensure proper data validation for bulk operations