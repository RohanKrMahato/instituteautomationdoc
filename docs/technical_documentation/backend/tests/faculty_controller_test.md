# Faculty Controller Test

## Overview

The faculty controller test suite ensures that faculty members can retrieve their assigned courses, view students registered for a course, and approve student registrations. Each function is tested with both successful and error scenarios, and all database/model interactions are mocked to focus on controller logic.


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
  - `supertest` for HTTP simulation
  - `express` for setting up test routes


## getFacultyCourses

**Input**
- Route parameter: `id` (faculty user ID)

**Process**
- Checks if the `id` parameter is provided in the request.
- Uses the `Faculty` model to find a faculty member by `userId`.
- If the faculty exists, retrieves all course mappings for that faculty from the `FacultyCourse` model.
- Extracts all course codes from the mappings and fetches detailed course information from the `Course` model.
- Handles cases where the faculty is not found, or no courses are assigned, and manages any internal errors.

**Output**
- 400 Bad Request: If user ID is missing.
- 404 Not Found: If the faculty is not found or has no assigned courses.
- 200 OK: Returns `{ success: true, data: [courses] }` with an array of course objects.
- 500 Internal Server Error: On database or unexpected errors.


## getStudentsByCourse

**Input**
- Route parameter: `courseCode` (course code)

**Process**
- Uses the `CourseRegistration` model to find all registrations for the given course code and populates student details.
- Maps each registration to a student object containing name, roll number, program, and semester.
- Handles and reports any internal errors.

**Output**
- 200 OK: Returns `{ success: true, students: [...] }` with an array of student objects for the course.
- 500 Internal Server Error: On database or unexpected errors.


## approveRegistrations

**Input**
- JSON body with:
  - `courseCode`: String (required)
  - `students`: Array of roll numbers (required)

**Process**
- Checks that both `courseCode` and `students` are provided and that `students` is an array.
- For each roll number in the `students` array:
  - Uses the `CourseRegistration` model to find the registration for the student and course.
    - If the registration is not found, continues to the next student.
  - Uses the `StudentCourse` model to update or create the student-course mapping, setting fields like `courseId`, `rollNo`, `creditOrAudit`, `semester`, `status` as "Approved", and `updatedAt` to the current date.
  - Deletes the registration from the `CourseRegistration` model after approval.
- Handles and reports any errors encountered during the process.

**Output**
- 400 Bad Request: If required fields are missing or invalid.
- 200 OK: Returns `{ success: true, message: 'Students approved successfully' }` after processing all students.
- 500 Internal Server Error: On database or unexpected errors.

