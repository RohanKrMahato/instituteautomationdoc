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

**Output:**
-   Success (200): Confirmation and updated transfer request
-   Error (400/404/500): Returns appropriate error message

**External Dependencies:**
-   Calls local student API to fetch and update user information using `axios`

### Meal Plan Management

#### `getStudentSubscriptionInfo`
Fetches the current meal subscription and any pending requests for a student.

**Input:**
- `req.student`: Student information from middleware

**Process:**
1. Checks if student record exists
2. Retrieves the current subscription from `MealSubscription`
3. Checks for any pending requests in `MealPlanRequest`
4. Returns both subscription and pending request data

**Output:**
- Success (200): Current subscription and pending request (if any)
- Error (404/500): Appropriate error response

#### `createMealPlanRequest`
Submits a request to change a student's meal plan.

**Input:**
- `req.student`: Student information from middleware
- `req.body.newPlan`: Requested meal plan type

**Process:**
1. Validates the requested meal plan
2. Checks if student already has the same plan
3. Verifies no pending requests exist
4. Creates a new meal plan request with 'Pending' status

**Output:**
- Success (201): Confirmation and request details
- Error (400/404/500): Appropriate error message

#### `getStudentMealRequestHistory`
Retrieves the history of meal plan requests for a student.

**Input:**
- `req.student`: Student information from middleware

**Process:**
1. Finds all meal plan requests for the student
2. Sorts them by creation date (newest first)

**Output:**
- Success (200): Array of meal plan requests
- Error (404/500): Error message

#### `getSubscriptionRequestsForAdmin`
Fetches all meal plan subscription requests for admin review.

**Input:**
- `req.user`: Admin user information
- `req.query.status`: Optional filter by status

**Process:**
1. Verifies admin role
2. Applies status filter if provided
3. Retrieves requests with student and admin information
4. Enhances data with student names

**Output:**
- Success (200): Array of enhanced meal plan requests
- Error (403/500): Access denied or error message

#### `processSubscriptionRequest`
Approves or rejects a meal plan subscription request.

**Input:**
- `req.params.requestId`: Request ID
- `req.body`: Includes `status`, `rejectionReason`
- `req.user`: Admin information

**Process:**
1. Validates admin role
2. Runs transaction to ensure data consistency
3. If approved, creates/updates the student's meal subscription
4. Updates request status with processing information

**Output:**
- Success (200): Confirmation and updated request details
- Error (400/403/404/500): Appropriate error response



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