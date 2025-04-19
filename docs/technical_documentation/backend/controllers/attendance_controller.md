# Attendance Controller

## Overview

The `attendance.controller.js` module manages attendance operations for students, faculty, and administrators. It supports creation, modification, and retrieval of attendance records, as well as analytics such as attendance percentage calculations, bulk uploads, and pending approval management.

## Dependencies

```javascript

import { Course } from '../models/course.model.js';
import { Attendance } from '../models/attendance.model.js';
import { FacultyCourse } from '../models/course.model.js';
import { StudentCourse } from '../models/course.model.js';
import { Student } from '../models/student.model.js';`
```
## Controller Methods

### Student Side

#### `getPercentages`
Calculates per-course attendance percentage for a student.

**Input:**
-   Header: `rollno`

**Process:**
1.  Aggregates total and present approved attendance per course.
2.  Fetches course names for mapping.
3.  Computes percentages for each course.

**Output:**
-   Success (200): Attendance percentage per course.
-   Error (400/500): Missing roll number or internal server error.

#### `getCourse`
Fetches full attendance data and statistics for a specific course.

**Input:**
-   `req.params`: `courseId`
-   Header: `rollno`

**Process:**
1.  Fetches course and student attendance records.
2.  Computes attendance statistics and events list.
3.  Builds response with summary and calendar view format.

**Output:**
-   Success (200): Full course attendance details.
-   Error (400/404/500): Missing or invalid data.

#### `createAttendanceRecord`
Creates an individual attendance record for a student.

**Input:**
-   Header: `rollno`
-   Body: `courseCode`, `date`, `isPresent`, `isApproved`

**Process:**
1.  Validates existence of course and student.
2.  Ensures record for the same date does not already exist.
3.  Creates a new attendance document.

**Output:**
-   Success (201): Created record.
-   Error (400/500): Validation or server error.

#### `createBulkAttendanceRecords`
Uploads multiple attendance records in bulk.

**Input:**
-   `req.body`: `attendanceRecords[]` (each with `rollNo`, `date`, `status`)
-   `req.params`: `id` (courseCode)

**Process:**
1.  Iterates over each record.
2.  Converts and validates dates.
3.  Internally calls `createAttendanceRecord` for each.

**Output:**
-   Success (200): Summary of successes and failures.
-   Error (400/500): Input validation or internal error.

### Faculty Side

#### `getFacultyCourses`
Fetches faculty-assigned courses along with attendance analytics.

**Input:**
-   Header: `userid` (faculty ID)

**Process:**
1.  Retrieves courses assigned to the faculty.
2.  Aggregates attendance data.
3.  Computes student count and average attendance.

**Output:**
-   Success (200): Courses with attendance stats.
-   Error (400/404/500): Faculty not found or internal error.

#### `addFacultyCourse`
Assigns a course to a faculty member.

**Input:**
-   Body: `facultyId`, `courseCode`, `year`, `session`, `status` (optional)

**Process:**
1.  Validates input and year range.
2.  Prevents duplicate assignments for session+year.
3.  Creates and saves course mapping.

**Output:**
-   Success (201): Mapping created.
-   Error (400/409/500): Validation or internal error.

#### `getStudents`
Returns roll numbers of students enrolled in a course.

**Input:**
-   `req.params`: `id` (course ID)

**Process:**
1.  Queries `StudentCourse` collection for approved entries.
2.  Extracts roll numbers.

**Output:**
-   Success (200): List of student roll numbers.
-   Error (400/500): Missing course ID or internal error.

#### `modifyAttendanceRecord`
Updates attendance for a specific student, date, and course.

**Input:**
-   Header: `rollno`
-   Body: `courseCode`, `date`, `isPresent`, `isApproved`

**Process:**
1.  Locates the attendance record for the date.
2.  Updates `isPresent`, `isApproved`, and timestamp.

**Output:**
-   Success (200): Updated record.
-   Error (400/404/500): Validation failure or not found.

### Admin Side

#### `getAllCourses`
Fetches minimal course data for UI dropdowns or listings.

**Input:**
-   None

**Process:**
1.  Fetches all courses selecting `courseCode` and `courseName`.

**Output:**
-   Success (200): Course data.
-   Error (500): Internal server error.

#### `getApprovalRequests`
Fetches all attendance entries pending approval.

**Input:**
-   None

**Process:**
1.  Queries for attendance with `isApproved = false`.
2.  Formats response with `courseId`, `studentId`, `date`, etc.

**Output:**
-   Success (200): List of unapproved entries.
-   Error (500): Server error.

#### `approveCourse`
Approves a specific attendance record.

**Input:**
-   Body: `courseCode`, `rollNo`, `date`

**Process:**
1.  Converts date into `startOfDay` and `endOfDay`.
2.  Updates the matching record to `isApproved = true`.

**Output:**
-   Success (200): Updated record.
-   Error (400/404/500): Validation or internal error.

#### `getAllStudents`
Returns all registered student roll numbers.

**Input:**
-   None

**Process:**
1.  Queries the `Student` collection and selects `rollNo`.

**Output:**
-   Success (200): List of roll numbers.
-   Error (500): Internal server error.

## Error Handling Strategy

-   Consistent status codes for all endpoints (`400`, `404`, `500`).
-   Validation for required parameters and formats.
-   Descriptive error messages for frontend consumption.
-   Try-catch blocks around all async database calls.

## Functional Highlights

-   Student: View attendance stats and course records.
-   Faculty: Manage course attendance and analytics.
-   Admin: Review and approve attendance logs.
-   Bulk upload: Efficient multi-student record processing.