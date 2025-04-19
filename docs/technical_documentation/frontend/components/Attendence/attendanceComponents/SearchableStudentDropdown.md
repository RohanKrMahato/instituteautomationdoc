# SearchableStudentDropdown

## Overview

The `SearchableStudentDropdown` component is a React component that provides a searchable dropdown interface for selecting students. It fetches student data based on the user's role (faculty or academic administrator) and allows filtering students by name or roll number.

## Props

| Prop | Type | Description |
|------|------|-------------|
| `courseId` | String | The ID of the course for which to fetch student data (required for faculty role) |
| `onStudentSelect` | Function | Callback function that receives the selected student's roll number |

## Features

- Dynamic data fetching based on user role
- Search functionality for filtering students by name or roll number
- Loading and error states
- Integration with RoleContext for role-based data fetching

## Component Workflow

1. The component fetches student data when mounted or when role/courseId changes
2. Different API endpoints are used depending on the user's role:
   - Faculty: `/api/attendancelanding/faculty/${courseId}`
   - Academic Admin: `/api/attendancelanding/admin/student`
3. Users can search for students using the search input field
4. When a student is selected from the dropdown, the `onStudentSelect` callback is triggered with the selected roll number

## Code Explanation

### State Management

The component uses several state variables:
- `selectedStudent`: Stores the currently selected student's roll number
- `searchTerm`: Stores the current search query
- `students`: Stores the list of students retrieved from the API
- `loading`: Tracks whether data is currently being fetched
- `error`: Stores any errors that occur during data fetching

### Data Fetching

Data is fetched in a `useEffect` hook that runs when the component mounts or when `role` or `courseId` changes:

```javascript
useEffect(() => {
    const fetchStudents = async () => {
        // Different API calls based on user role
        if (role === "faculty") {
            // Faculty-specific API call
        }
        if (role === 'acadAdmin') {
            // Admin-specific API call
        }
    };

    fetchStudents();
}, [role, courseId]);
```

### Student Filtering

Students are filtered based on the search term, matching either name or roll number:

```javascript
const filteredStudents = students.filter(student => 
    student.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    student.rollNumber.toLowerCase().includes(searchTerm.toLowerCase())
);
```

### Event Handlers

- `handleInputChange`: Updates the search term when the user types in the search input
- `handleStudentChange`: Updates the selected student and calls the `onStudentSelect` callback when a student is selected from the dropdown

### Rendering

The component renders:
1. A search input field for filtering students
2. A dropdown select element showing filtered students
3. Appropriate feedback for loading and error states

## Usage Example

```jsx
import SearchableStudentDropdown from './SearchableStudentDropdown';

function AttendancePage() {
  const handleStudentSelect = (rollNumber) => {
    console.log(`Selected student: ${rollNumber}`);
    // Fetch attendance or perform other actions with the selected student
  };

  return (
    <div>
      <h1>Student Attendance</h1>
      <SearchableStudentDropdown 
        courseId="CS101" 
        onStudentSelect={handleStudentSelect} 
      />
    </div>
  );
}
```

## Dependencies

- React (useState, useEffect, useContext)
- RoleContext from "../../../context/Rolecontext"

## Note

The component assumes that the backend API returns student data in a specific format:
- For faculty role: `data.rollNumbers` containing an array of roll numbers
- For academic admin role: `data.data` containing an array of roll numbers

If the API response format changes, the component's data processing logic will need to be updated accordingly.