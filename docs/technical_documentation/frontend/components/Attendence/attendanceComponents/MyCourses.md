# MyCourses

## Overview

The `MyCourses` component is a React component that displays course information and attendance statistics based on user roles (student, faculty, or academic administrator). The component fetches user-specific course data from an API and renders different interfaces depending on the user's role.

## Features

- **Role-based interfaces** for students, faculty, and academic administrators
- **Course listing** with attendance statistics 
- **Student search functionality** for administrators
- **Attendance alerts** for students with attendance below 75%
- **Dynamic data fetching** based on user role and selected students

## Component Structure

### Imports

```jsx
import Course from "./Course";
import { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "../../../context/Rolecontext";
import SearchableStudentDropdown from "./SearchableStudentDropdown";
import AttendanceApprovalDashboard from "./AttendanceApprovalDashboard";
import SiteAlert from "./siteAlert";
import { useQuery } from "@tanstack/react-query";
import newRequest from "../../../utils/newRequest";
```

### State Variables

- `courses`: Array of course objects with attendance data
- `loading`: Boolean to track loading state
- `overall`: Boolean indicating if attendance is satisfactory (true) or needs attention (false)
- `selectedStudent`: ID of the selected student (for faculty and admin views)
- `showStats`: Boolean to control visibility of student statistics

## Core Functions

### `showStudentStats(rollNo)`

Selects a student and fetches their course data:

```jsx
const showStudentStats = (rollNo) => {
    setSelectedStudent(rollNo);
    fetchStudentCourses(rollNo);
    setShowStats(true);
};
```

### `fetchStudentCourses(rollNo)`

Fetches course data for a specific student:

```jsx
const fetchStudentCourses = async (rollNo) => {
    try {
        const response = await fetch("http://localhost:8000/api/attendancelanding/student", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "rollno": rollNo
            }
        });

        // Process response and format courses
        // ...
    } catch (error) {
        console.error("Error fetching student courses:", error);
        throw error;
    }
};
```

### `useEffect` - Data Initialization

Fetches course data when the component mounts:

```jsx
useEffect(() => {
    const fetchCourses = async () => {
        try {
            setLoading(true);

            if (role === "student") {
                // Fetch student-specific courses
                // ...
            } else if (role === "faculty") {
                // Fetch faculty-specific courses
                // ...
            }
        } catch (error) {
            console.error("Error fetching courses:", error);
        } finally {
            setLoading(false);
        }
    };

    fetchCourses();
}, [role]);
```

### `handleStudentChange(e)`

Updates selected student and fetches their courses (used by dropdown):

```jsx
const handleStudentChange = async (e) => {
    const rollNumber = e.target.value;
    setSelectedStudent(rollNumber);

    if (rollNumber) {
        // Fetch and process course data for the selected student
        // ...
    } else {
        setShowStats(false);
    }
};
```

## Role-Based Behavior

### Student Role

- Shows "My Courses" heading
- Displays a warning alert if attendance falls below 75% in any course
- Shows list of courses with attendance percentages

### Faculty Role

- Shows "My Courses" heading
- Displays courses taught by the faculty with average attendance and total student count

### Academic Administrator Role

- Shows an attendance approval dashboard
- Provides a student search dropdown
- Displays selected student's courses and attendance

## API Endpoints

1. `/student/${userId}` - Fetches student data
2. `/api/attendancelanding/student` - Fetches student's course attendance data
3. `/api/attendancelanding/faculty` - Fetches faculty's course data
4. `/api/attendancelanding/${rollNumber}` - Fetches course data for a specific student

## Rendered UI Components

- `Course`: Renders the list of courses
- `SiteAlert`: Warning component for students with low attendance
- `AttendanceApprovalDashboard`: Dashboard for academic administrators
- `SearchableStudentDropdown`: Component for searching and selecting students

## Usage Example

```jsx
import MyCourses from './path/to/MyCourses';

function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Student Dashboard</h1>
      <MyCourses />
    </div>
  );
}
```

## Data Flow

1. Component mounts and retrieves user data from localStorage
2. Based on the user's role, it fetches appropriate course data
3. For students, it checks attendance percentages and shows alerts if needed
4. For faculty, it shows courses they teach with attendance statistics
5. For administrators, it allows searching and viewing any student's attendance

## Dependencies

- React (useState, useEffect, useContext)
- React Router (useNavigate)
- React Query (useQuery)
- Custom context (RoleContext)
- Custom components (Course, SearchableStudentDropdown, AttendanceApprovalDashboard, SiteAlert)
- Custom utility (newRequest)