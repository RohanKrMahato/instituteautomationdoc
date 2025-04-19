# AcadAdmin Route

## Overview
This document provides comprehensive technical documentation for the Academic Administration API routes defined in `acadAdmin.route.js`. These routes manage document applications, course drop requests, fee structures, and student document access controls.

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

### Add a Fee Structure
```javascript
// Example request
fetch('/api/acadAdmin/feeControl/addFee', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Tuition Fee 2025',
    amount: 50000,
    category: 'Tuition',
    program: 'Bachelor of Science',
    academicYear: '2025-2026',
    items: [
      { name: 'Base Fee', amount: 40000 },
      { name: 'Lab Fee', amount: 10000 }
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
- Access to these endpoints should be restricted to authorized academic administrators
- Implement proper authentication and authorization middleware
- Validate all input parameters to prevent injection attacks
- Implement rate limiting to prevent abuse