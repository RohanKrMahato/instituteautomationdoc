# CourseStats

## Overview

The `CourseStats` component is a React component that displays attendance statistics for courses. It has different functionalities based on the user's role (student, faculty, or academic administrator). The component allows faculty to upload attendance data in CSV format and view statistics for individual students.

## Features

- **Role-based views**: Different interfaces for students and faculty
- **Attendance statistics**: Shows percentage, classes missed, classes attended, and required classes
- **CSV upload**: Faculty can upload attendance data in bulk via CSV
- **Student selection**: Faculty can search and select students to view their attendance
- **Calendar integration**: Displays attendance calendar view

## Component Structure

### Props
- None (uses context and params instead)

### State Variables
- `courseName`: Name of the current course
- `courseId`: ID of the current course (from URL parameters)
- `attendanceAll`, `classesMissed`, `classesAttended`, `classesRequired`, `percentage`: Attendance statistics
- `file`: Stores the CSV file for upload
- `submitted`: Tracks the upload status (false, 'loading', 'success', 'error')
- `showStats`: Controls whether to show student statistics
- `selectedStudent`: ID of the currently selected student
- `studentList`: List of students in the course
- `studentAttendanceData`: Attendance data for students
- `loadingStudents`: Indicates if student data is being loaded

## Main Functions

### `handleFileChange(event)`
Handles file input changes, storing the selected file in state.

### `showStudentStats(rollNo)`
Displays attendance statistics for a specific student:
- Sets `showStats` to true
- Updates `selectedStudent` with the provided student ID
- Calls `fetchAttendance` to get the student's attendance data

### `handleSubmit()`
Processes and uploads CSV attendance data:
1. Validates that a file is selected
2. Parses CSV content using PapaParse
3. Validates CSV structure (required columns: rollno, date, status)
4. Normalizes and validates each record
5. Separates valid and invalid records
6. Prepares data payload for API
7. Uploads data to server via POST request
8. Handles success/error responses

### `fetchAttendance(rollNo)`
Fetches attendance data for a specific student:
1. Makes a GET request to the attendance API
2. Updates state with received statistics (missed classes, attended classes, etc.)
3. Sets `showStats` to true

### `deleteCourse()`
Currently just shows an alert and navigates to home page.

## Conditional Rendering

The component renders different UI elements based on user role:

### For Students
- Calendar view
- Attendance statistics (percentage, missed classes, attended classes, required classes)

### For Faculty
- File upload interface for attendance data
- Student search dropdown
- Selected student's attendance statistics (when a student is selected)
- AddOrUpdate component for managing attendance

## Dependencies

- React (useState, useEffect, useContext, useRef)
- React Router (useParams, useNavigate)
- PapaParse for CSV parsing
- React Icons (FaFileUpload, FaCheckCircle, FaUndo)
- React Query (useQuery)
- Custom components:
  - MyCalendar
  - AddOrUpdate
  - SearchableStudentDropdown
- Custom contexts:
  - RoleContext

## API Interactions

1. GET `/student/{userId}` - Fetches student data
2. GET `/api/attendancelanding/student/{courseId}` - Fetches attendance for a student in a course
3. POST `/api/attendancelanding/add/bulk/{courseId}` - Uploads bulk attendance data

## Usage Example

The component is typically used in a course view with role-based access:

```jsx
import { CourseStats } from './path/to/CourseStats';

function CoursePage() {
  return (
    <div className="course-page">
      <h1>Course Overview</h1>
      <CourseStats />
    </div>
  );
}
```

## Code Flow

1. Component mounts and retrieves user data from localStorage
2. If the user is a student, their attendance data is fetched automatically
3. If the user is faculty, they see options to upload attendance or select a student
4. When a student is selected, their attendance data is fetched and displayed
5. Faculty can upload CSV attendance data which is validated and sent to the server

## CSV Upload Requirements

CSV files must have the following columns:
- `rollno`: Student roll number
- `date`: Date in YYYY-MM-DD format
- `status`: Attendance status ('present' or 'absent')