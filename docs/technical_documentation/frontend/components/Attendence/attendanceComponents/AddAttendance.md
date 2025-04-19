# AddAttendance

## Overview

The `AddAttendance` component is a React form interface designed to record student attendance for a specific course. It allows instructors or administrators to mark students as present or absent on a selected date.

## Component Props

| Prop | Type | Description |
|------|------|-------------|
| `selectedStudent` | String | The roll number of the student whose attendance is being recorded |

## State Management

The component manages the following state variables using React's `useState` hook:

- `date`: Stores the selected attendance date (defaults to current date)
- `present`: Stores the attendance status (true for present, false for absent, null for unselected)

## URL Parameters

The component uses React Router's `useParams` hook to extract the course code from the URL:

- `id`: Represents the course code from the URL parameter

## Functionality

### Date Selection

The component uses the `react-datepicker` library to provide a user-friendly date selection interface with calendar visualization.

### Attendance Status Selection

Users can select one of three attendance states from a dropdown:
- None (default)
- Present
- Absent

### Form Submission

When the form is submitted:

1. The default form submission behavior is prevented
2. Form data is prepared, including:
   - Course code (from URL)
   - Date (in ISO format)
   - Attendance status (boolean)
   - Approval status (defaulted to false)
3. A POST request is sent to `http://localhost:8000/api/attendancelanding/add`
4. The student's roll number is included in the request headers
5. Upon successful submission:
   - Form fields are reset
   - Success message is displayed
6. Error handling provides user feedback if submission fails

## Code Breakdown

### Imports

```jsx
import { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { useParams } from "react-router-dom";
```

- `useState`: React hook for component state management
- `DatePicker`: Third-party component for date selection
- `useParams`: React Router hook for accessing URL parameters

### Component Definition

```jsx
function AddAttendance({ selectedStudent }) {
    // Component implementation
}
```

The component accepts a `selectedStudent` prop which should contain the student's roll number.

### State and Parameter Setup

```jsx
const { id } = useParams(); // get courseCode from URL params
const courseCode = id;
const rollNo = selectedStudent; // get rollNo from selected student
const [date, setDate] = useState(new Date());
const [present, setPresent] = useState(null);
```

- Extracts course code from URL parameters
- References the selected student's roll number
- Initializes state for date (current date) and attendance status (null)

### Event Handlers

#### Attendance Status Change Handler

```jsx
const handlePresentChange = (event) => {
    const value = event.target.value;
    setPresent(value === "true"); // convert string to boolean
};
```

Converts the string value from the select element to a boolean and updates state.

#### Form Submission Handler

```jsx
const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = {
        courseCode: courseCode,
        date: date.toISOString(), // send full ISO date
        isPresent: present,
        isApproved: false
    };
    
    try {
        // API call and response handling
        // ...
    } catch (error) {
        // Error handling
        // ...
    }
};
```

This asynchronous function:
1. Prevents default form submission behavior
2. Prepares the data package
3. Makes an API call to record attendance
4. Handles success/error scenarios

### Render Method

The component renders a form with:
1. A DatePicker component for date selection
2. A dropdown for attendance status selection (Present/Absent)
3. A submit button to record the attendance

## API Integration

The component interacts with an attendance API endpoint:

- **Endpoint**: `http://localhost:8000/api/attendancelanding/add`
- **Method**: POST
- **Headers**:
  - Content-Type: application/json
  - rollno: [student roll number]
- **Body**:
  ```json
  {
    "courseCode": "[course code]",
    "date": "[ISO date string]",
    "isPresent": true|false,
    "isApproved": false
  }
  ```

## Usage Notes

1. This component should be used within a context where `selectedStudent` is provided
2. The component expects to be rendered on a route that includes the course code as a URL parameter
3. API endpoint may need to be updated based on environment (development, production, etc.)
4. The attendance is marked as not approved by default, suggesting an approval workflow