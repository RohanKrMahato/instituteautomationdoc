# Faculty Course Students Component

## Overview

The `FacultyCourseStudents` component provides a comprehensive interface for faculty members to view, search, filter, and manage students enrolled in a specific course. This component displays student information in a tabular format with advanced filtering, sorting, and export capabilities.

## Component Structure

The component fetches student data for a specific course and renders the following sections:
- Statistics cards showing enrollment data
- Search and filter controls
- Sortable student data table
- Export functionality

## Dependencies

```jsx
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import newRequest from "../../utils/newRequest";
import { useQuery } from "@tanstack/react-query";
import {
  FaSearch, FaFilter, FaFileDownload, FaArrowLeft, FaEnvelope,
  FaSortAlphaDown, FaSortAlphaUp, FaUserGraduate, FaCalendarCheck
} from "react-icons/fa";
```

## Props

This component doesn't accept any props. It retrieves the `courseId` from the URL parameters using React Router's `useParams` hook.

## State Management

The component maintains several state variables:

| State         | Type      | Description                                                |
|---------------|-----------|------------------------------------------------------------|
| `searchTerm`  | String    | Stores the current search input                            |
| `filter`      | Object    | Contains filter criteria for program, semester, and status |
| `sort`        | Object    | Contains sorting field and direction                       |

## API Integration

The component uses React Query to fetch student data:

```jsx
const { isLoading, error, data } = useQuery({
  queryKey: ["course-students", courseId],
  queryFn: () =>
    newRequest.get(`/faculty/courses/${courseId}/students`).then((res) => {
      console.log("Course students data received:", res.data);
      return res.data;
    }),       
});
```

## Key Functions

### `getFilteredStudents()`

Applies search, filter, and sort operations to the student data:

```jsx
const getFilteredStudents = () => {
  if (!data || !data.students) return [];
  
  return data.students
    .filter(student => {
      // Apply search and filters
      // ...
    })
    .sort((a, b) => {
      // Apply sorting
      // ...
    });
};
```

### `toggleSort(field)`

Handles column sorting:

```jsx
const toggleSort = (field) => {
  if (sort.field === field) {
    setSort({
      ...sort,
      direction: sort.direction === "asc" ? "desc" : "asc"
    });
  } else {
    setSort({
      field,
      direction: "asc"
    });
  }
};
```

### `exportStudentList()`

Exports filtered student data to CSV:

```jsx
const exportStudentList = () => {
  if (!data || !data.students) return;
  
  const headers = ["Roll No", "Name", "Email", "Program", "Semester", "Status", "Grade"];
  const csvContent = [
    headers.join(","),
    ...getFilteredStudents().map(student => [
      student.rollNo,
      student.name,
      student.email,
      student.program,
      student.semester,
      student.registrationStatus,
      student.grade || "Not Assigned"
    ].join(","))
  ].join("\n");
  
  // Create and download CSV file
  // ...
};
```

### `getStatistics()`

Calculates class statistics for the dashboard cards:

```jsx
const getStatistics = () => {
  if (!data || !data.students || !data.students.length) {
    return { totalStudents: 0, programCounts: {}, averageAttendance: 0 };
  }
  
  // Calculate statistics
  // ...
  
  return {
    totalStudents: data.students.length,
    programCounts,
    averageAttendance
  };
};
```

## UI Components

### Statistics Cards

Displays summary information about the course enrollment:
- Total number of students
- Program distribution
- Average attendance percentage

### Search and Filter Bar

Allows filtering students by:
- Text search (name, roll number, email)
- Program (BTech, MTech, PhD, etc.)
- Semester (1-8)
- Registration status (Credit/Audit)

Also includes:
- Reset filters button
- Export to CSV button

### Students Table

Displays student information with the following columns:
- Roll Number
- Name
- Email
- Program
- Semester
- Registration Status
- Attendance (with visual progress bar)
- Grade
- Action buttons (email)

All columns (except Email and Action) are sortable.

## Loading and Error States

The component handles different UI states:
- Loading state with spinner
- Error state with message
- Empty state when no students are enrolled

## Usage Example

This component is typically used in a route like:

```jsx
<Route path="/faculty/courses/:courseId/students" element={<FacultyCourseStudents />} />
```

## Expected Data Structure

The component expects the API to return data in the following format:

```javascript
{
  course: {
    courseName: "Example Course Name",
    // other course properties...
  },
  students: [
    {
      rollNo: "B20CS001",
      name: "Student Name",
      email: "student@example.com",
      program: "BTech",
      semester: 5,
      registrationStatus: "Credit",
      attendance: 85,
      grade: "A"
    },
    // more students...
  ]
}
```

## Styling

The component uses Tailwind CSS classes for styling with a responsive design that adapts to different screen sizes.

## Accessibility Features

- Proper semantic HTML structure
- Color contrast for status indicators
- Keyboard-navigable interface
- Visual feedback for interactive elements

