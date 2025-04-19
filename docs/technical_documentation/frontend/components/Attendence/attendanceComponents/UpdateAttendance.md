# UpdateAttendance

## Overview

The `UpdateAttendance` component is a React component designed to provide an interface for updating student attendance records. It allows users to select a date and mark a student as present or absent for a specific course.

## Props

| Prop | Type | Description |
|------|------|-------------|
| `selectedStudent` | String | The roll number of the student whose attendance is being updated |

## Features

- Date selection using the React DatePicker component
- Present/Absent attendance status selection
- Form validation to ensure attendance status is selected
- API integration for updating attendance records
- Success and error handling with user feedback

## Component Workflow

1. The component retrieves the course code from URL parameters
2. Users select a date using the DatePicker
3. Users select attendance status (Present/Absent)
4. On form submission, the data is sent to the API endpoint
5. Users receive feedback about the success or failure of the update

## Code Explanation

### Dependencies

The component uses several React-related libraries and hooks:
- `useState` for state management
- `DatePicker` from react-datepicker for date selection
- `useParams` from react-router-dom to access URL parameters

### State Management

The component maintains two main state variables:
- `date`: Stores the selected date (defaults to current date)
- `present`: Boolean that indicates whether the student is present (true), absent (false), or not yet specified (null)

```javascript
const [date, setDate] = useState(new Date());
const [present, setPresent] = useState(null);
```

### Event Handlers

#### `handlePresentChange`

Manages the present/absent selection value:

```javascript
const handlePresentChange = (event) => {
    const value = event.target.value;
    setPresent(value === "true" ? true : value === "false" ? false : null);
};
```

#### `handleSubmit`

Processes the form submission:
1. Prevents default form submission behavior
2. Validates that attendance status is selected
3. Prepares data for API submission
4. Sends a PUT request to the API
5. Handles the response and provides user feedback
6. Resets form state on success

```javascript
const handleSubmit = async (event) => {
    event.preventDefault();

    if (present === null) {
        alert("Please select Present or Absent.");
        return;
    }

    // Prepare and send data to API
    // ...
};
```

### API Integration

The component makes a PUT request to update attendance:

```javascript
const response = await fetch('http://localhost:8000/api/attendancelanding/update', {
    method: 'PUT', 
    headers: {
        'Content-Type': 'application/json',
        'rollno': rollNo
    },
    body: JSON.stringify(formData)
});
```

The request includes:
- Course code
- Date (formatted as ISO string)
- Attendance status (isPresent)
- Approval status (defaulted to false)

### UI Structure

The component renders a form with:
1. A DatePicker for selecting the date
2. A dropdown for selecting attendance status (Present/Absent)
3. A submit button for updating the attendance

## Usage Example

```jsx
import UpdateAttendance from './UpdateAttendance';

function AttendanceManagementPage() {
  return (
    <div>
      <h1>Update Student Attendance</h1>
      <UpdateAttendance selectedStudent="ABC123" />
    </div>
  );
}
```

## Notes

- The component expects the rollNo to be passed as a prop named `selectedStudent`
- The courseCode is extracted from the URL parameters
- The API response is expected to include an error property in case of failure
- Success/failure feedback is provided through browser alerts