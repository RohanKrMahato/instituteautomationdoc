# Hostel Controller

## Overview

The `HostelController` manages student-related hostel operations including leave requests and hostel transfers. It provides endpoints for students to submit requests and for admins to retrieve and update them accordingly.

## Dependencies

```javascript

import axios from "axios";
import { HostelLeave, HostelTransfer } from "../models/hostel.model.js";
import { Student } from '../models/student.model.js';`
```

## Controller Methods

### Hostel Leave Management

`studentLeave`
Submits a hostel leave request for a student.

**Input:**
-   `req.body`: Includes `studentId`, `startDate`, `endDate`, `applicationId` (optional), `email`, `reason`

**Process:**
1.  Validates presence of required fields
2.  Checks logical correctness of `startDate` and `endDate`
3.  Finds student using `email`
4.  Verifies `studentId` matches the student's record
5.  Creates a leave request with status `Pending`
6.  Saves to the `HostelLeave` collection

**Key Code Snippet**
```javascript
const leaveRequest = {
    rollNo: student.rollNo,
    startDate,
    endDate,
    reason,
    status: 'Pending'
};
await HostelLeave.create(leaveRequest);
```

**Output:**
-   Success (200): Confirmation message
-   Error (400/404/500): Appropriate error response


#### `getStudentLeave`
Fetches leave requests for a specific student.

**Input:**
-   `req.params.id`: Student's `userId`

**Process:**
1.  Finds student by `userId`
2.  Queries `HostelLeave` by `rollNo`
3.  Returns list of leave records

**Key Code Snippet**
```javascript
const leaves = await HostelLeave.find({ rollNo: student.rollNo });
```

**Output:**
-   Success (200): Array of leave requests
-   Error (404/500): Error message

#### `getAllLeaves`
Retrieves all hostel leave records in the system.

**Input:**
-   None

**Process:**
1.  Fetches all documents from `HostelLeave` collection

**Output:**
-   Success (200): All leave entries
-   Error (404/500): Error message


#### `updateAnyLeave`
Updates the status of a specific leave request.

**Input:**
-   `req.params.id`: Leave request ID
-   `req.body.status`: New status value

**Process:**
1.  Updates the `status` field of the leave record
2.  Returns updated record

**Key Code Snippet**
```javascript
const leave = await HostelLeave.findByIdAndUpdate(leaveId, { status }, { new: true });
```

**Output:**
-   Success (200): Confirmation and updated leave data
-   Error (404/500): Appropriate error response


### Hostel Transfer Management

#### `hostelTransfer`
Submits a hostel transfer request for a student.

**Input:**
-   `req.body`: Includes `status`, `studentId`, `currentHostel`, `requestedHostel`, `reason`

**Process:**
1.  Validates required fields
2.  Finds student by `rollNo`
3.  Constructs a `HostelTransfer` document
4.  Saves the request to the database

**Key Code Snippet**
```javascript
const transferRequest = {
    rollNo: student.rollNo,
    currentHostel,
    requestedHostel,
    reason,
    status
};
await HostelTransfer.create(transferRequest);
```

**Output:**
-   Success (200): Confirmation message
-   Error (400/404/500): Appropriate error message

#### `getStudentTransfer`
Fetches hostel transfer requests for a specific student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Finds student using `userId`
2.  Retrieves all `HostelTransfer` records for the student's `rollNo`

**Output:**
-   Success (200): Array of transfer requests
-   Error (404/500): Error response

#### `getAllTransferRequests`
Retrieves all hostel transfer requests in the system.

**Input:**
-   None

**Process:**
1.  Fetches all records from `HostelTransfer` collection

**Output:**
-   Success (200): Array of transfer requests
-   Error (500): Error message

#### `updateTransferRequest`
Approves or rejects a specific hostel transfer request and updates the student's profile accordingly.

**Input:**
-   `req.params.id`: Transfer request ID
-   `req.body`: Includes `status`, `reason`, `newHostel`, `rollNo`

**Process:**
1.  Validates the status field (`Approved` or `Rejected`)
2.  Calls external API to fetch `userId` using `rollNo`
3.  If approved, makes a PUT request to update the student's hostel info
4.  Updates the transfer request document with new status and reason

**Key Code Snippet**
```javascript
// External API call to get userId
const response = await axios.get(`http://localhost:8000/api/student/${rollNo}/rollno`);

// Update student hostel if approved
await axios.put(`http://localhost:8000/api/student/${userId}/profile`, {
    hostel: newHostel
});

// Update transfer status
const request = await HostelTransfer.findByIdAndUpdate(
    requestId,
    { status, reason },
    { new: true }
);
```

**Output:**
-   Success (200): Confirmation and updated transfer request
-   Error (400/404/500): Returns appropriate error message

**External Dependencies:**
-   Calls local student API to fetch and update user information using `axios`


## Error Handling Strategy
The controller ensures robust error handling:
-   Validates all inputs before processing
-   Logs detailed error messages to the console
-   Sends clear HTTP status codes and error descriptions

## Security Considerations
1.  **Authorization:**
    -   Assumes upstream middleware handles user authentication and roles
2.  **Input Validation:**
    -   All critical fields are checked for presence and logical validity
3.  **External Requests:**
    -   Proper try/catch blocks are implemented for all external API calls