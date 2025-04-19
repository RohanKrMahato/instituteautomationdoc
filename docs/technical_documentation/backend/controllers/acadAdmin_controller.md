# Academic Admin Controller

## Overview

The `acadAdmin.controller` module handles academic administrative tasks related to document applications, fee structures, course drop requests, and student document access. It allows academic admins to manage and process student-related data efficiently within the Institute Automation System.

## Dependencies

```javascript

import mongoose from "mongoose";
import { ApplicationDocument, Bonafide, Passport } from '../models/documents.models.js';
import { Student } from '../models/student.model.js';
import { User } from '../models/user.model.js';
import { CourseDropRequest } from '../models/courseDropRequest.model.js';
import { Course, StudentCourse } from '../models/course.model.js';
import { FeeBreakdown } from "../models/fees.model.js";`
```

## Controller Methods

### Application Management
#### `getAllApplications`
Fetches all application documents with pagination.

**Input:**
-   `req.query`: May contain `page` and `limit`.

**Process:**
1.  Retrieves paginated applications.
2.  Populates student and user data.
3.  Appends student name to each application.

**Output:**
-   Success (200): Returns enriched applications and pagination metadata.
-   Error (500): Returns error message.

#### `filterApplications`
Filters applications based on optional query parameters.

**Input:**
-   `req.query`: Can include `rollNo`, `type`, `status`.

**Process:**
1.  Dynamically builds query based on filters.
2.  Looks up document-specific details (Bonafide/Passport).
3.  Enriches each application with student and document info.

**Output:**
-   Success (200): Filtered application list.
-   Error (500): Returns error message.

#### `getApplicationById`
Fetches a specific application with full details.

**Input:**
-   `req.params`: Contains `id` (application ID).

**Process:**
1.  Retrieves application and student/user info.
2.  Fetches extra document info based on type.
3.  Builds enriched response with detailed student data.

**Output:**
-   Success (200): Returns enriched application.
-   Error (404/500): Returns error message.

#### `updateApplicationStatus`
Updates status and optionally appends remarks.

**Input:**
-   `req.params`: `id` of the application.
-   `req.body`: Contains `status`, `remarks`.

**Process:**
1.  Validates inputs.
2.  Updates status and remarks.
3.  Populates student info and returns enriched response.

**Output:**
-   Success (200): Returns updated application.
-   Error (400/404/500): Returns error message.

#### `addComment`
Adds a comment to the application approval remarks.

**Input:**
-   `req.params`: `id` of the application.
-   `req.body`: Contains `comment`.

**Process:**
1.  Pushes new comment to remarks array.
2.  Updates `updatedAt` timestamp.

**Output:**
-   Success (200): Updated application.
-   Error (404/500): Returns error message.

### Course Drop Request Management

#### `getDropRequests`
Retrieves all course drop requests with student info.

**Input:**
-   None

**Process:**
1.  Fetches drop requests from DB.
2.  Populates student and user data.
3.  Maps each request with required metadata.

**Output:**
-   Success (200): Returns list of formatted requests.
-   Error (500): Returns error message.

#### `updateDropRequestStatus`
Updates the status and remarks of a drop request.

**Input:**
-   `req.params`: `requestId`
-   `req.body`: `status`, `remarks`

**Process:**
1.  Updates drop request fields.
2.  If status is `Approved`, unenrolls student from the course.

**Output:**
-   Success (200): Confirmation message.
-   Error (404/500): Returns error message.

**Business Rules:**
-   Course un-enrollment only occurs if the request is approved.

### Fee Structure Management

#### `addFeeStructure`
Adds a new academic fee structure.

**Input:**
-   `req.body`: Must include year, program, semesterParity, and fee component values.

**Process:**
1.  Validates required and numeric fields.
2.  Validates academic program.
3.  Creates and saves `FeeBreakdown` entry.

**Output:**
-   Success (201): New fee structure saved.
-   Error (400/500): Returns validation or server error.

**Validation:**
-   Fields must be present and numeric.
-   Program must be from: `BTech`, `MTech`, `PhD`, `BDes`, `MDes`.

#### `getFeeBreakdown`
Fetches academic fee structure based on filters.

**Input:**
-   `req.query`: Optional filters `year`, `program`, `semesterParity`

**Process:**
1.  Builds dynamic query.
2.  Retrieves matching entries.

**Output:**
-   Success (200): Fee structures.
-   Error (404/500): Returns error message.

### Document Access Management

#### `getStudentsWithDocumentAccess`
Lists students and their document access rights.

**Input:**
-   `req.query`: Filters like `branch`, `program`, `semester`, `search`, and pagination.

**Process:**
1.  Filters students based on parameters.
2.  Populates user details.
3.  Adds access flags (transcript, ID card, fee receipt).

**Output:**
-   Success (200): Students with access data.
-   Error (500): Returns error message.

#### `updateStudentDocumentAccess`
Updates document access flags for one student.

**Input:**
-   `req.params`: Student `id`
-   `req.body`: `access` object with flags

**Process:**
1.  Validates input.
2.  Updates specific access fields.

**Output:**
-   Success (200): Updated student object.
-   Error (400/404/500): Returns error message.

#### `bulkUpdateDocumentAccess`
Performs bulk access updates for multiple students.

**Input:**
-   `req.body`: `studentIds` array, `access` object

**Process:**
1.  Validates array and access object.
2.  Constructs bulk update and executes.

**Output:**
-   Success (200): Modified and matched counts.
-   Error (400/500): Returns error message.

## Error Handling Strategy

-   Input validation for all endpoints.
-   Try-catch around async DB operations.
-   Returns meaningful messages and status codes.
-   Fallbacks for optional population steps.
-   Logs errors for debugging purposes.

## Performance Considerations

-   Uses `.lean()` for performance.
-   Pagination in listing endpoints.
-   `Promise.all` used for parallel DB reads.
-   Query filtering and selective projection for efficiency.

## Security Considerations

1.  **Input Validation:**
    -   Ensures required fields are present and valid before DB ops.
2.  **Data Protection:**
    -   Uses selective field population for privacy.
3.  **Safe Bulk Updates:**
    -   Document access flags are updated using `updateMany` with checks.