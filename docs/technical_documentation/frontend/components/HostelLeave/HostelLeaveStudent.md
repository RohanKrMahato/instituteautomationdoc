# Hostel Leave Student Component

## Overview

The `HostelLeaveStudent` component provides an interface for students to view their hostel leave requests and submit new ones. Students can see the status of their previous leave applications, view full details of the reason for leave, and submit new leave requests. The component handles form validation, data submission, and displays existing requests.

---

## Dependencies

- **React**: Core library for building the UI
- **@tanstack/react-query**: For data fetching, caching, and state management
- **newRequest**: Custom API request utility

---

## Component Structure

### Imported Modules

- `useState` from 'react'
- `useQuery` from '@tanstack/react-query'
- `newRequest` from '../../utils/newRequest'

### State Management

- **requests**: Array of leave requests
- **showForm**: Boolean to toggle the leave application form
- **formData**: Object containing form input values (startDate, endDate, reason)
- **selectedReason**: Selected reason for modal display (null when modal is closed)

### Data Fetching

- Uses React Query's `useQuery` hook to fetch student's hostel leave requests
- Query key: `["leaves"]`
- Endpoint: `/hostel/${userId}/leaves`

---

## Functionality

### User Authentication

- Retrieves user data (email, userId) from localStorage
- Uses this data for API requests and form submissions

### Form Management

- **Open/Close Form**: Toggle form visibility with buttons
- **Form Reset**: Clear form data when discarding
- **Form Validation**: Validates that end date is after start date
- **Form Submission**: Handles form submission and API requests

### Leave Request Management

- **Submit Request**: Creates new leave request via POST request
- **View Requests**: Displays all existing leave requests
- **View Full Reason**: Shows complete reason text in a modal

---

## UI Components

### Requests Display

- **Request Cards**: Shows leave request details including ID, dates, status, and truncated reason
- **Empty State**: Shows message when no requests exist

### Leave Application Form

- **Date Inputs**: Start and end date selection with validation
- **Reason Input**: Textarea for entering reason for leave
- **Action Buttons**: Submit and Discard buttons for form actions

### Reason Modal

- **Trigger**: Clicking on a request card
- **Content**: Full reason text in a modal dialog
- **Close Action**: Button to dismiss the modal

---

## API Interactions

### Data Fetching

```javascript
newRequest.get(`/hostel/${userId}/leaves`).then((res) => {
    return res.data;
})
```

### Leave Submission

```javascript
newRequest.post('/hostel/leave', newReq)
```

---

## Styling

- Uses Tailwind CSS for styling
- **Color Scheme**:
  - Blue for primary actions (submit, apply)
  - Gray for secondary actions (discard)
  - White background with gray cards for requests
- **Layout**: Responsive card-based layout
- **Modal**: Fixed position with semi-transparent backdrop

---

## Implementation Details

- **Date Formatting**: Truncates date strings to display only relevant portions
- **Reason Truncation**: Shows only first few words of reason with ellipsis
- **Loading & Error States**: Handled by React Query
- **Form Validation**: Prevents submission when end date is before or equal to start date
- **Conditional Rendering**: Shows appropriate UI based on data and user actions

---

## Best Practices Demonstrated

- **Form Validation**: Client-side validation with visual feedback
- **React Query Usage**: Efficient data fetching with automatic caching
- **Conditional Rendering**: Only shows relevant UI elements based on state
- **User Feedback**: Shows loading states and validation errors
- **Modal Pattern**: Uses modals for displaying additional information

---

## Usage

```jsx
// Import the component
import HostelLeaveStudent from './path/to/HostelLeaveStudent';

// Use within a parent component
function ParentComponent() {
  return (
    <div>
      <HostelLeaveStudent />
    </div>
  );
}
```

> **Note**: The component requires proper setup of React Query's QueryClient provider in the application and expects user data to be stored in localStorage.

---