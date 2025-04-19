# Attendance Controller Test 

## Overview

This document outlines the Jest-based testing implementation for the attendance controller functions, including attendance calculations, record creation, modification, faculty and student course management, and approval workflows

## Dependencies

***Controllers Mocked***
- getPercentages
- getCourse
- createAttendanceRecord
- createBulkAttendanceRecords
- getFacultyCourses
- addFacultyCourse
- getStudents
- modifyAttendanceRecord
- getAllCourses
- getApprovalRequests
- approveCourse
- getAllStudents

***Model Mocks***
- Course
- Attendance
- FacultyCourse
- StudentCourse
- Student

***Libraries Used***
- `jest` for mocking and assertions
- `node-mocks-http` (implied standard for HTTP mocks in Node.js tests)


## getPercentages
**Input**
- Header: `rollno`
- 
**Process**
- Validates presence of `rollno` header
- Aggregates attendance data per course for the given roll number
- Calculates attendance percentage for each course
- Handles errors gracefully

**Output**
- 400 Bad Request if roll number is missing
- 200 OK with JSON: `{ rollNo, attendance: [{ courseCode, courseName, percentage }] }`
- 500 Internal Server Error on exceptions


## getCourse

**Input**
- Path parameter: `courseId`
- Header: `rollno`

**Process**
- Validates presence of `rollno` header
- Looks up course by `courseId`
- Fetches all attendance records for the student in that course
- Computes stats: percentage, classes attended/missed, required classes

**Output**
- 400 Bad Request if roll number is missing
- 404 Not Found if course is not found
- 200 OK with JSON: `{ student, courseId, courseName, stats: { percentage, classesMissed, classesAttended, reqClasses } }`


## createAttendanceRecord

**Input**
- Header: `rollno`
- Body: `courseCode`, `date`, `isPresent` (optional)

**Process**
- Validates required fields
- Checks if a record already exists for the student, course, and date
- Creates a new attendance record if not present

**Output**
- 400 Bad Request if required fields are missing or record exists
- 201 Created with JSON: `{ success: true, message: 'Attendance record created successfully' }`


## createBulkAttendanceRecords

**Input**
- Path parameter: `id` (course code)
- Body: `attendanceRecords` (array of `{ rollNo, date, status }`)

**Process**
- Iterates over attendance records
- For each record, invokes `createAttendanceRecord`
- Aggregates results and errors

**Output**
- 200 OK with JSON: `{ success: true, message, results: [...], errors: [...] }`


## getFacultyCourses

**Input**
- Header: `userid` (faculty ID)

**Process**
- Validates presence of faculty ID
- Finds courses assigned to faculty
- Calculates attendance statistics for each course

**Output**
- 400 Bad Request if faculty ID is missing
- 404 Not Found if no courses found
- 200 OK with JSON: `{ success: true, data: [{ facultyId, courseCode, attendancePercentage, totalStudents }], count }`


## addFacultyCourse

**Input**
- Body: `facultyId`, `courseCode`, `year`, `session`

**Process**
- Validates required fields
- Checks if faculty-course mapping already exists
- Creates new faculty-course assignment

**Output**
- 400 Bad Request if required fields are missing
- 409 Conflict if mapping exists
- 201 Created with JSON: `{ success: true, message: 'Faculty course added successfully' }`


## getStudents

**Input**
- Path parameter: `id` (course code)

**Process**
- Fetches all student enrollments for the course

**Output**
- 200 OK with JSON: `{ rollNumbers: [...] }`


## modifyAttendanceRecord

**Input**
- Header: `rollno`
- Body: `courseCode`, `date`, `isPresent`, `isApproved` (optional)

**Process**
- Validates required fields
- Locates attendance record by student, course, and date
- Updates attendance status and approval as needed

**Output**
- 400 Bad Request if required fields are missing
- 404 Not Found if record is not found
- 200 OK on successful update


## getAllCourses

**Input**
- None

**Process**
- Fetches all courses from the database

**Output**
- 200 OK with JSON: `{ success: true, data: [...] }`


## getApprovalRequests

**Input**
- None

**Process**
- Finds all attendance records pending approval

**Output**
- 200 OK with JSON: `[{ studentId, courseId, date, present, pendingApproval }]`


## approveCourse

**Input**
- Body: `courseCode`, `rollNo`, `date`

**Process**
- Validates required fields
- Updates the attendance record to set `isApproved: true`

**Output**
- 400 Bad Request if required fields are missing
- 404 Not Found if record is not found
- 200 OK with JSON: `{ success: true, message: 'Attendance record approved successfully' }`


## getAllStudents

**Input**
- None

**Process**
- Fetches all student roll numbers from the database

**Output**
- 200 OK with JSON: `{ success: true, count, data: [rollNo1, rollNo2, ...] }`
