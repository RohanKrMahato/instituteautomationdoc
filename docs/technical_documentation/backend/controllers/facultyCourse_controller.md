# FacultyCourse Controller

## Overview

The `FacultyCourseController` manages operations related to courses assigned to faculty members and their student registrations. It enables faculties to fetch their assigned courses, retrieve enrolled students, and approve course registrations.

## Dependencies

```javascript

import { Faculty } from '../models/faculty.model.js';
import { FacultyCourse } from '../models/course.model.js';
import { Course } from '../models/course.model.js';
import { CourseRegistration } from '../models/course.model.js';
import { Student } from '../models/student.model.js';
import { StudentCourse } from '../models/course.model.js';`
```

## Controller Methods

### `getFacultyCourses`
Fetches all the courses assigned to a specific faculty member.

**Input:**
-   `req.params.id`: `userId` of the faculty

**Process:**
1.  Verifies the `userId` is provided
2.  Retrieves the `Faculty` document by `userId`
3.  Fetches all `FacultyCourse` entries linked to the faculty
4.  Maps the course codes and fetches corresponding `Course` details

**Key Code Snippet**
```javascript
const faculty = await Faculty.findOne({ userId });
const facultyCourses = await FacultyCourse.find({ facultyId: faculty.userId });
const courses = await Course.find({ courseCode: { $in: courseCodes } });
```

**Output:**
-   Success (200): Returns a list of course objects
-   Error (400/404/500): Returns appropriate error message


### `getStudentsByCourse`
Retrieves all students registered for a given course.

**Input:**
-   `req.params.courseCode`: Course code

**Process:**
1.  Queries `CourseRegistration` for all registrations matching the course
2.  Populates `rollNo` to fetch student details
3.  Extracts key fields like `name`, `rollNo`, `program`, `semester` for each student

**Key Code Snippet**
```javascript
const registrations = await CourseRegistration.find({ courseCode }).populate({
  path: 'rollNo',
  model: Student
});
const students = registrations.map((reg) => ({
  name: reg.rollNo?.userId?.name || "N/A",
  rollNo: reg.rollNo?.rollNo,
  // ...other student details
}));
```

**Output:**
-   Success (200): Returns array of student information
-   Error (500): Returns server error message

### `approveRegistrations`
Approves selected student course registrations for a given course.

**Input:**
-   `req.body.courseCode`: Course code for which registrations need approval
-   `req.body.students`: Array of student roll numbers

**Process:**
1.  Validates input structure
2.  Iterates over each student:
    -   Fetches their pending registration from `CourseRegistration`
    -   Creates or updates an entry in `StudentCourse` with status "Approved"
    -   Deletes the approved registration from `CourseRegistration`

**Key Code Snippet**
```javascript
await StudentCourse.findOneAndUpdate(
  { courseId: courseCode, rollNo },
  {
    $set: {
      status: 'Approved',
      // ...other fields
    }
  },
  { upsert: true }
);
await CourseRegistration.deleteOne({ courseCode, rollNo });
```

**Output:**
-   Success (200): Returns success message
-   Error (400/500): Returns appropriate error message

**Business Logic:**
-   Ensures each student is approved only if a corresponding registration exists
-   Uses `upsert` to ensure `StudentCourse` document is created if it doesn't already exist


## Error Handling Strategy
The controller applies consistent error handling:
-   Validates request parameters and body before proceeding
-   Logs server-side errors with descriptive messages
-   Uses HTTP status codes to differentiate between client and server issues

## Security Considerations
-----------------------
1.  **Authorization:**
    -   Assumes upstream middleware manages faculty authentication and authorization
2.  **Input Validation:**
    -   Strict validation of `userId`, `courseCode`, and student arrays
    -   Prevents invalid or malformed operations
3.  **Atomic Updates:**
    -   Ensures data consistency by using atomic updates (`findOneAndUpdate`, `deleteOne`)