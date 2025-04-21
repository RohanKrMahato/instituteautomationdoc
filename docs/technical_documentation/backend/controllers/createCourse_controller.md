# Create Course Controller

## Overview

The `createCourse.controller.js` module handles creation of new courses, faculty-course mappings, and program-course-semester configurations. This endpoint ensures that a course is registered once and then mapped across programs, departments, and semesters as required.

## Dependencies

```javascript
import { Course, FacultyCourse, ProgramCourseMapping } from "../models/course.model.js";`
```

## Controller Methods

### `createCourse`
Creates a course along with faculty and program-semester mappings.

**Input:**
-   `req.body` should include:
    -   `courseCode` (string)
    -   `courseName` (string)
    -   `maxIntake` (number)
    -   `faculty` (faculty ID string)
    -   `slot` (string)
    -   `courseDepartment` (string)
    -   `credits` (number)
    -   `year` (number)
    -   `session` (string)
    -   `configurations[]`: array of configuration objects with:
        -   `program` (string)
        -   `department` (string)
        -   `semesters[][]` (nested array of semester identifiers)
        -   `type` (e.g., "core", "elective")

**Process:**
1.  Checks if a course already exists by `courseCode`.
2.  If not, creates a new course document.
3.  Iterates over each configuration:
    -   Creates a new `FacultyCourse` entry for each.
    -   For every semester in the configuration, creates a `ProgramCourseMapping`.

    
**Key Code Snippet**
```javascript
let course = await Course.findOne({ courseCode });
if (!course) {
  course = new Course({ courseCode, department:courseDepartment, courseName, maxIntake, slot, credits });
  await course.save();
}

// faculty course mapping
const facultyCourse = new FacultyCourse({
  facultyId: faculty,
  courseCode,
  year,
  session
});
await facultyCourse.save();

//Program setter mapping
const programMapping = new ProgramCourseMapping({
  courseCode,
  program,
  department,
  year,
  semester:semester[0],
  type
});
await programMapping.save();
```

**Output:**
-   Success (200): Confirmation message indicating all data saved.
-   Error (500): Internal server error during any DB operation.

## Error Handling Strategy

-   Entire method wrapped in try-catch block.
-   Logs all internal errors to the server console.
-   Returns meaningful HTTP error message on failure.

## Functional Highlights

-   Prevents duplicate course creation.
-   Supports batch setup of:
    -   Course metadata
    -   Faculty-course associations
    -   Program-department-semester-course mappings