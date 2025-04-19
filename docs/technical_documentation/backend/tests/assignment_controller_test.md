# Assignment Controller Test 

***This document describes the testing implementation for the assignment controller functions, using Jest and mock HTTP requests.***


## Overview
This test suite validates multiple controller functions from the assignment controller module, including course retrieval, assignment creation, submission, deletion, and user/student data access.

## Dependencies

***Controllers Mocked***
- getFacultyCourses
- getStudentCourses
- createAssignment
- getCourseAssignments
- getAssignmentDetails
- submitAssignment
- undoSubmission
- deleteAssignmentDetails
- editAssignmentDetails
- getStudent
- getUser

***Model Mocks***
- Faculty
- Student
- User
- Course
- FacultyCourse
- StudentCourse
- Assignment

***Libraries Used***
- `node-mocks-http` for mocking HTTP requests and responses


## getFacultyCourses

 ***Input***
- Path parameter: `userId`

***Process***
- Mocks a faculty's list of courses
- Calls `getFacultyCourses` with mock request and response

***Output***
- 200 OK with JSON: `{ courses: [...] }`


## getStudentCourses

***Input***
- Path parameter: `userId`

***Process***
- Mocks a student's list of courses
- Calls `getStudentCourses` with mock request and response

***Output***
- 200 OK with JSON: `{ courses: [...] }`


## createAssignment

***Input***
- Path parameter: `courseId`
- Body: `title`, `description`, `dueDate`

***Process***
- Validates required fields
- Returns 201 if all data is present
- Returns 400 for missing fields

***Output***
- 201 Created with assignment info
- 400 Bad Request if fields are missing


## submitAssignment

***Input***
- Path parameters: `courseCode`, `assignmentId`
- Body: `studentRollNo`, `studentName`, `content`

***Process***
- Accepts submission if not previously submitted
- Rejects duplicate submissions

***Output***
- 200 OK for successful submission
- 409 Conflict for duplicates


## deleteAssignmentDetails

***Input***
- Path parameters: `courseId`, `assignmentId`

***Process***
- Deletes assignment for valid IDs
- Returns 404 if IDs are invalid

***Output***
- 200 OK if deleted
- 404 Not Found if invalid


## getStudent

***Input***
- Path parameter: `userId`

***Process***
- Fetches mocked student details using `getStudent`

***Output***
- 200 OK with student info


## getUser

***Input***
- Path parameter: `userId`

***Process***
- Fetches mocked user details using `getUser`

***Output***
- 200 OK with user info


