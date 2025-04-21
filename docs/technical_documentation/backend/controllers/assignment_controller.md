# Assignment Controller

## Overview

The `assignment.controller` module handles operations related to course assignments for both faculty and students. It includes functionalities for managing courses, creating and updating assignments, student submissions, and fetching user-specific academic data.

## Dependencies

```javascript

import mongoose from "mongoose";
import { Faculty } from "../models/faculty.model.js";
import { Course, FacultyCourse } from "../models/course.model.js";
import { Assignment } from "../models/assignment.model.js";
import { Student } from "../models/student.model.js";
import { StudentCourse } from "../models/course.model.js";
import { User } from "../models/user.model.js";`
```

## Controller Methods

### Course Management

#### `getFacultyCourses`
Fetches all ongoing courses assigned to a faculty.

**Input:**
-   `req.params`: `userId` (faculty's user ID)

**Process:**
1.  Retrieves the faculty using `userId`.
2.  Finds all ongoing course mappings from `FacultyCourse`.
3.  Fetches course details from `Course`.

**Key Code Snippet**
```javascript
const facultyCourses = await FacultyCourse.find({ facultyId: userId, status: "Ongoing" });
const courseCodes = facultyCourses.map(fc => fc.courseCode);
const courses = await Course.find({ courseCode: { $in: courseCodes } });

```


**Output:**
-   Success (200): List of courses.
-   Error (404/500): Returns error message.

#### `getStudentCourses`
Fetches all approved courses a student is enrolled in.

**Input:**
-   `req.params`: `userId` (student's user ID)

**Process:**
1.  Finds student record by `userId`.
2.  Retrieves approved course enrollments from `StudentCourse`.
3.  Fetches course details from `Course`.

**Key Code Snippet**
```javascript
const studentCourses = await StudentCourse.find({ rollNo: student.rollNo, status: 'Approved' });
const courseCodes = studentCourses.map(sc => sc.courseId);
const courses = await Course.find({ courseCode: { $in: courseCodes } });
```

**Output:**
-   Success (200): List of enrolled courses.
-   Error (404/500): Returns error message.

#### `getCourse`
Retrieves details of a course using `courseCode`.

**Input:**
-   `req.params`: `courseCode`

**Process:**
1.  Fetches course using course code.

**Key Code Snippet**
```javascript
const course = await Course.findOne({ courseCode });
```

**Output:**
-   Success (200): Course data.
-   Error (400/404/500): Returns error message.

### Assignment Management

#### `createAssignment`
Creates a new assignment for a course.

**Input:**
-   `req.params`: `courseId`
-   `req.body`: `title`, `description`, `dueDate`

**Process:**
1.  Validates input fields.
2.  Counts current assignments to assign a sequential number.
3.  Creates and saves new assignment.


**Key Code Snippet**
```javascript
const assignmentCount = await Assignment.countDocuments({ courseCode: courseId });
const newAssignment = new Assignment({
  assignmentNumber: assignmentCount + 1,
  courseCode: courseId,
  title,
  description,
  dueDate: new Date(dueDate),
});
await newAssignment.save();

```

**Output:**
-   Success (201): Assignment object.
-   Error (400/500): Returns error message.

#### `getCourseAssignments`
Fetches all assignments of a course.

**Input:**
-   `req.params`: `courseId`

**Process:**
1.  Validates course ID.
2.  Finds assignments using course code.

**Key Code Snippet**
```javascript
const assignments = await Assignment.find({ courseCode: courseId });
```

**Output:**
-   Success (200): List of assignments.
-   Error (400/500): Returns error message.

#### `getAssignmentDetails`
Fetches details of a specific assignment.

**Input:**
-   `req.params`: `courseId`, `assignmentId`

**Process:**
1.  Finds assignment by course and assignment number.

**Key Code Snippet**
```javascript
const assignment = await Assignment.findOne({
  assignmentNumber: assignmentId,
  courseCode: courseId,
});

```


**Output:**
-   Success (200): Assignment object.
-   Error (404/500): Returns error message.

#### `editAssignmentDetails`
Updates title, description, or due date of an assignment.

**Input:**
-   `req.params`: `courseId`, `assignmentId`
-   `req.body`: `title`, `description`, `dueDate`

**Process:**
1.  Validates required fields.
2.  Finds and updates assignment.

**Key Code Snippet**
```javascript
const updatedAssignment = await Assignment.findOneAndUpdate(
  { assignmentNumber: assignmentId, courseCode: courseId },
  { title, description, dueDate },
  { new: true }
);
```

**Output:**
-   Success (200): Updated assignment.
-   Error (400/404/500): Returns error message.

#### `deleteAssignmentDetails`
Deletes a specific assignment.

**Input:**
-   `req.params`: `courseId`, `assignmentId`

**Process:**
1.  Validates input.
2.  Deletes assignment using course and assignment number.

**Key Code Snippet**
```javascript
const deletedAssignment = await Assignment.findOneAndDelete({
  assignmentNumber: assignmentId,
  courseCode: courseId,
});
```

**Output:**
-   Success (200): Deleted assignment object.
-   Error (400/404/500): Returns error message.

### Submission Management

#### `submitAssignment`
Allows a student to submit an assignment.

**Input:**
-   `req.params`: `courseCode`, `assignmentId`
-   `req.body`: `studentRollNo`, `studentName`, `content`

**Process:**
1.  Finds assignment by course and ID.
2.  Checks if the student has already submitted.
3.  Pushes submission with current timestamp.

**Key Code Snippet**
```javascript
const alreadySubmitted = assignment.submissions.some(
  (sub) => sub.studentRollNo === studentRollNo
);

assignment.submissions.push({
  studentRollNo,
  studentName,
  content,
  submittedAt: new Date(),
});
await assignment.save();

```

**Output:**
-   Success (200): Confirmation message.
-   Error (404/409/500): Returns error message.

#### `undoSubmission`
Allows a student to undo a submission.

**Input:**
-   `req.params`: `courseCode`, `assignmentId`, `rollNo`

**Process:**
1.  Finds the assignment.
2.  Removes the student's submission from the list.
3.  Saves the assignment.

**Key Code Snippet**
```javascript
assignment.submissions = assignment.submissions.filter(
  (sub) => sub.studentRollNo !== rollNo
);
await assignment.save();
```

**Output:**
-   Success (200): Confirmation message.
-   Error (404/500): Returns error message.

### User and Student Info

#### `getStudent`
Fetches student details by user ID.

**Input:**
-   `req.params`: `userId`

**Process:**
1.  Finds student record using `userId`.

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId });
```

**Output:**
-   Success (200): Student object.
-   Error (404/500): Returns error message.

#### `getUser`
Fetches user details from the User collection.

**Input:**
-   `req.params`: `userId`

**Process:**
1.  Finds user document by ID.

**Key Code Snippet**
```javascript
const user = await User.findById(userId);
```

**Output:**
-   Success (200): User object.
-   Error (404/500): Returns error message.

## Error Handling Strategy

-   Validations for required fields before DB operations.
-   All async operations wrapped in try-catch.
-   Returns specific messages and status codes (`400`, `404`, `500`).
-   Console logs for debugging and traceability.

## Business Rules

-   Students cannot resubmit once an assignment is submitted (unless undone).
-   Assignment numbers are auto-incremented per course.
-   Course-based filtering ensures scoped data access.