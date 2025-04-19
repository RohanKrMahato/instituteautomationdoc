# FacultyCourse Controller Test

## Overview

The FacultyCourse controller test suite validates the endpoints for retrieving faculty-assigned courses, listing students registered in a course, and approving student registrations. All models and controller functions are mocked, and HTTP requests are simulated using Supertest and Express. Each controller function is described in detail, including its internal operations and error handling.


## Dependencies

- **Controllers Tested**
  - `getFacultyCourses`
  - `getStudentsByCourse`
  - `approveRegistrations`

- **Models Mocked**
  - `Faculty`
  - `FacultyCourse`
  - `Course`
  - `CourseRegistration`
  - `StudentCourse`

- **Libraries and Tools**
  - `jest` for mocking and assertions
  - `supertest` for HTTP request simulation
  - `express` and `body-parser` for setting up test routes


## getFacultyCourses

**Input**
- Route parameter: `id` (faculty user ID)

**Process**
- Validates if the `id` parameter is provided in the request.
- Uses the `Faculty` model to find a faculty member by `userId`.
- If the faculty is found, uses the `FacultyCourse` model to find all course mappings for that faculty.
- Extracts course codes from the mappings.
- Uses the `Course` model to fetch detailed information for each course code.
- Handles the following error cases:
  - If no `id` is provided, responds with 400.
  - If the faculty is not found, responds with 404.
  - If no courses are assigned to the faculty, responds with 404.
  - Any internal server error results in a 500 response.

**Output**
- 400 Bad Request: If user ID is missing.
- 404 Not Found: If faculty is not found or has no assigned courses.
- 200 OK: Returns `{ success: true, data: [courses] }`, an array of course objects.
- 500 Internal Server Error: On unexpected errors.


## getStudentsByCourse

**Input**
- Route parameter: `courseCode` (course code)

**Process**
- Uses the `CourseRegistration` model to find all registrations for the given course code.
- Calls `.populate()` to include student details in each registration.
- Maps each registration to a student object containing:
  - `name` (from `rollNo.userId.name`)
  - `rollNo` (from `rollNo.rollNo`)
  - `program` (from `rollNo.program`)
  - `semester` (from `rollNo.semester`)
- Handles errors during database operations.

**Output**
- 200 OK: Returns `{ success: true, students: [...] }`, an array of student objects for the course.
- 500 Internal Server Error: On database or unexpected errors.


## approveRegistrations

**Input**
- JSON body with:
  - `courseCode`: String (required)
  - `students`: Array of roll numbers (required)

**Process**
- Validates that both `courseCode` and `students` are provided and that `students` is an array.
  - If not, responds with 400 and an error message.
- For each roll number in the `students` array:
  - Uses the `CourseRegistration` model to find the registration for the student and course.
    - If the registration is not found, skips to the next student.
  - Uses the `StudentCourse` model to update or create the student-course mapping, setting:
    - `courseId`, `rollNo`, `creditOrAudit`, `semester`, `status` as "Approved", and `updatedAt` to the current date.
  - Deletes the registration from the `CourseRegistration` model after approval.
- Handles errors during any part of the process and responds with a 500 error if encountered.

**Output**
- 400 Bad Request: If required fields are missing or invalid.
- 200 OK: Returns `{ success: true, message: 'Students approved successfully' }` after processing all students.
- 500 Internal Server Error: On database or unexpected errors.
