# Student Controller

## Overview

The `StudentController` handles student-related functionalities including profile data, course enrollments, document applications, announcements, and course drop operations. It facilitates both student self-service and admin operations through a well-structured set of endpoints.

## Dependencies

```javascript

import { Student } from '../models/student.model.js';
import { Course, StudentCourse, FacultyCourse } from '../models/course.model.js';
import { ApplicationDocument, Bonafide, Passport } from '../models/documents.models.js';
import { Faculty } from '../models/faculty.model.js';
import { CourseDropRequest } from '../models/courseDropRequest.model.js';
import { User } from '../models/user.model.js';`
```

## Controller Methods

### Student Data

#### `getStudent`
Fetches the profile of a specific student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Finds student by `userId`
2.  Populates the associated `User` document

**Output:**
-   Success (200): Returns student document
-   Error (404/500): Appropriate error message

#### `updateStudentProfile`
Updates profile information for a student.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Profile update data

**Process:**
1.  Updates user fields (`name`, `email`, `contactNo`) if present
2.  Updates student model (`hostel`, `roomNo`, `department`, etc.)

**Output:**
-   Success (200): Updated student document
-   Error (404/500): Error message

#### `getStudentFromRollNumber`
Finds the student's userId using their roll number.

**Input:**
-   `req.params.id`: Student's `rollNo`

**Process:**
1.  Searches `Student` model using `rollNo`

**Output:**
-   Success (200): Returns `userId`
-   Error (404/500): Error message

### Academic Courses

#### `getCompletedCourses`
Fetches completed courses for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `StudentCourse` entries with `isCompleted: true`
2.  Fetches course metadata using `courseCode`
3.  Merges course and performance data

**Output:**
-   Success (200): Array of completed courses
-   Error (404/500): Error message

#### `getStudentCourses`
Retrieves current approved courses for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Determines session based on current date
2.  Fetches approved `StudentCourse` records
3.  Merges with course data and faculty assignments

**Output:**
-   Success (200): Array of current course objects
-   Error (404/500): Appropriate message

#### `dropCourse`
Removes a course from the student's profile.

**Input:**
-   `req.params.studentId`: Student ID
-   `req.params.courseId`: Course ID

**Process:**
1.  Validates student enrollment
2.  Removes course from student and course models

**Output:**
-   Success (200): Confirmation message
-   Error (404): Course or student not found

#### `createCourseDropRequest`
Submits a drop request for an enrolled course.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body.courseId`: Course code

**Process:**
1.  Checks enrollment and pending drop requests
2.  Constructs a `CourseDropRequest` with `Pending` status

**Output:**
-   Success (201): Confirmation and request ID
-   Error (400/404/500): Proper error handling

#### `getStudentDropRequests`
Fetches all course drop requests for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `CourseDropRequest` by `rollNo`
2.  Sorts by most recent

**Output:**
-   Success (200): Array of drop requests
-   Error (404/500): Error message

#### `cancelDropRequest`
Cancels a pending course drop request.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.params.requestId`: Drop request ID

**Process:**
1.  Verifies ownership and pending status
2.  Deletes the request

**Output:**
-   Success (200): Confirmation
-   Error (400/403/404/500): Validated errors

### Course Announcements

#### `getCourseAnnouncements`
Fetches course announcements along with faculty details.

**Input:**
-   `req.params.courseId`: Course code

**Process:**
1.  Retrieves course and announcement list
2.  Enriches each announcement with faculty metadata
3.  Sorts by latest

**Output:**
-   Success (200): Course document with enhanced announcements
-   Error (404/500): Error message

#### `getFacultyByIds`
Retrieves a list of faculty by their IDs.

**Input:**
-   `req.query.ids`: Comma-separated faculty IDs

**Process:**
1.  Queries `Faculty` model using `$in` filter

**Output:**
-   Success (200): Array of faculty documents
-   Error (404/500): Error message

### Bonafide Certificate

#### `getStudentBonafideDetails`
Returns student profile data for bonafide application.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Populates basic user details
2.  Maps required student fields

**Output:**
-   Success (200): Returns data for bonafide application
-   Error (404/500): Error message
`createBonafideApplication`
Submits a new bonafide application.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Includes `currentSemester`, `certificateFor`, `otherReason`

**Process:**
1.  Creates `ApplicationDocument` and `Bonafide` records
2.  Handles conditional reason fields

**Output:**
-   Success (201): Application ID
-   Error (404/500): Error message

#### `getBonafideApplications`
Returns all bonafide applications submitted by a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Queries documents of type `Bonafide`
2.  Enriches with bonafide-specific data

**Output:**
-   Success (200): Array of applications
-   Error (404/500): Error message

### Passport Certificate

#### `getStudentPassportDetails`
Fetches student information for passport application.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Fetches student and user profile fields

**Output:**
-   Success (200): Populated profile object
-   Error (404/500): Error message

#### `submitPassportApplication`
Creates a passport application entry.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Includes `applicationType`, `placeOfBirth`, `semester`, etc.

**Process:**
1.  Creates `ApplicationDocument`
2.  Creates associated `Passport` document

**Output:**
-   Success (201): Application ID
-   Error (404/500): Error message


#### `getPassportApplications`
Lists all passport applications for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `ApplicationDocument` of type `Passport`
2.  Fetches and maps associated `Passport` data

**Output:**
-   Success (200): Array of passport applications
-   Error (404/500): Error message

## Error Handling Strategy
-   All endpoints validate required fields and return specific error messages
-   Logs detailed errors to the console
-   Differentiates between `404`, `400`, and `500` errors for clarity

## Security Considerations
1.  **Authentication & Authorization:**
    -   Assumes upstream middleware handles session validation
2.  **Validation:**
    -   Every endpoint validates inputs before accessing the database
3.  **Sensitive Data:**
    -   Only public student info is exposed; passwords and secure fields are omitted