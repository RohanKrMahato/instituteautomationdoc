# Faculty Controller

## Overview

The `FacultyController` handles API endpoints related to faculty data management in the academic system. This includes fetching faculty details, courses, and enrolled students, all while maintaining necessary associations across multiple data models like `Course`, `Student`, and `User`.

## Dependencies
```javascript

import { Course } from '../models/course.model.js';
import { Faculty } from '../models/faculty.model.js';
import { Student } from '../models/student.model.js';
import { StudentCourse } from '../models/course.model.js';
import { User } from '../models/user.model.js';`
```

## Controller Methods

### Faculty Data Management

#### `getFaculty`
Fetches basic details of a faculty member.

**Input:**
-   `req.params.id`: Faculty `userId` to be searched

**Process:**
1.  Queries the `Faculty` collection using `userId`
2.  Populates user information from the `User` model
3.  Returns the faculty document

**Key Code Snippet**
```javascript
const user = await Faculty.findOne({ userId: facultyId }).populate('userId');
```

**Output:**
-   Success (200): Returns faculty object
-   Error (404/500): Returns error message


#### `getFacultyByIds`
Retrieves multiple faculty members using an array of faculty IDs.

**Input:**
-   `req.query.ids`: Comma-separated list of faculty IDs

**Process:**
1.  Parses the comma-separated list of IDs
2.  Queries the `Faculty` collection with `$in` filter
3.  Returns the matched faculty documents

**Key Code Snippet**
```javascript
const facultyIds = req.query.ids.split(',');
const facultyMembers = await Faculty.find({ facultyId: { $in: facultyIds } });
```

**Output:**
-   Success (200): Returns array of faculty documents
-   Error (404/500): Returns error message


#### `getFacultyCourses`

Retrieves the list of ongoing courses taught by a faculty member and compiles course-related data.

**Input:**
-   `req.params.id`: Faculty `userId`
**Process:**

1.  Fetches the faculty document using `userId`
2.  Filters for `Ongoing` courses
3.  For each course:
    -   Fetches course details from the `Course` collection
    -   Calculates number of students
    -   Generates random data for assignments and attendance
4.  Sets feedback availability based on current month

**Key Code Snippet**
```javascript
// Filter ongoing courses
const activeCourses = facultyCourses.filter(course => course.status === 'Ongoing');

// Get course details with metrics
const coursesWithDetails = await Promise.all(activeCourses.map(async (course) => {
  const courseDetails = await Course.findOne({ courseCode: course.courseCode });
  const studentCount = courseDetails.students ? courseDetails.students.length : 0;
  return {
    id: courseDetails.courseCode,
    name: courseDetails.courseName,
    students: studentCount,
    // ...other metrics
  };
}));
```

**Output:**
-   Success (200): Returns array of course objects with metrics and feedback status
-   Error (404/500): Returns error message

**Business Logic:**
-   Feedback is open only during April--June
-   Only `Ongoing` courses are considered active


#### `getCourseStudents`
Fetches detailed information of all students enrolled in a particular course.

**Input:**
-   `req.params.courseId`: Course code for lookup

**Process:**
1.  Retrieves course details from `Course` collection
2.  Extracts `students` array from course document
3.  Fetches student-specific info from `Student` model
4.  Fetches user info (name, email, profile) from `User` model
5.  Combines all data including randomized attendance

**Key Code Snippet**
```javascript
// Get course and students
const course = await Course.findOne({ courseCode: courseId });
const students = course.students || [];

// Get student and user details
const studentDetails = await Student.find({ userId: { $in: students } });
const userInfo = await User.find({ _id: { $in: students } }, 'name email profilePicture');

// Combine data
const studentsWithDetails = students.map(registration => {
  return {
    rollNo: studentInfo.rollNo,
    name: user.name,
    // ...other details
  };
});
```

**Output:**
-   Success (200): Returns detailed student list with course info
-   Error (404/500): Returns error message


**Output Structure:**
-   Course: `courseCode`, `courseName`, `department`, `credits`
-   Students: List including `rollNo`, `name`, `email`, `profilePicture`, `department`, `semester`, `batch`, `program`, `status`, `hostel`, `roomNo`, `grade`, `attendance`, etc.


## Error Handling Strategy

Each method implements standard error handling:
-   Checks for missing or invalid parameters
-   Logs descriptive errors for server debugging
-   Returns proper status codes for client interpretation

## Data Aggregation Techniques

-   **Mapping and Lookup**: Student and user information are resolved using `userId` and mapped into response payloads.
-   **Filtering**: Courses are filtered based on `status` (`Ongoing`)
-   **Fallback Values**: Randomized data for assignments, grades, and attendance are used where real-time data is unavailable

## Security Considerations

1.  **Authorization:**
    -   This controller assumes middleware handles user authentication and access control prior to execution
2.  **Validation:**
    -   IDs and parameters are validated or checked for existence before database operations
3.  **Data Exposure:**
    -   Sensitive user data like passwords is never exposed; only public profile info is included