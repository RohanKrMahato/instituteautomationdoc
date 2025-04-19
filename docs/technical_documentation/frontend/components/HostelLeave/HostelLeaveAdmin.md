# Hostel Leave Admin Component

## Overview

The `HostelLeaveAdmin` component provides an administrative interface for managing student hostel leave requests. It displays a tabular view of all leave requests with their details and allows administrators to approve or reject pending requests. The component fetches leave data from an API, manages the display state, and handles status updates.

---

## Dependencies

- **React**: Core library for building the UI
- **@tanstack/react-query**: For data fetching, caching, and state management
- **newRequest**: Custom API request utility

---

## Component Structure

### Imported Modules

- `useQuery` from '@tanstack/react-query'
- `useState`, `useEffect` from 'react'
- `newRequest` from '../../utils/newRequest'

### State Management

- **requests**: Array of formatted leave requests
- **selectedReason**: Currently selected reason for modal display (null when modal is closed)

### Data Fetching

- Uses React Query's `useQuery` hook to fetch all hostel leave requests
- Query key: `["leaves"]`
- Endpoint: `/hostel/leaves`

---

## Functionality

### Data Processing

- Formats raw API data into a more manageable structure
- Extracts relevant fields: ID, student ID, dates, reason, and status
- Uses `useEffect` to update the local state when data changes

### Leave Request Management

- **Approve/Reject**: Updates leave request status via PUT request
- **Optimistic Updates**: Updates UI immediately before API confirmation
- **Error Handling**: Reverts UI state if API update fails

### UI Features

- **Tabular Display**: Shows all leave requests in a structured table
- **Status Highlighting**: Color-codes status fields (green for approved, red for rejected)
- **Reason Modal**: Shows full reason text when truncated reason is clicked
- **Conditional Rendering**: Only shows action buttons for pending requests

---

## UI Components

### Main Table

- **Headers**: Student ID, Start Date, End Date, Reason, Status, Action
- **Row Data**: Displays leave request information with truncated reason text
- **Action Buttons**: Approve and Reject buttons for pending requests

### Reason Modal

- **Trigger**: Clicking on truncated reason text
- **Content**: Full reason text in a modal dialog
- **Close Action**: Button to dismiss the modal

---

## API Interactions

### Data Fetching

```javascript
newRequest.get(`/hostel/leaves`).then((res) => {
    return res.data;
})
```

### Status Updates

```javascript
newRequest.put(`/hostel/leaves/${id}`, { status: newStatus })
```

---

## Styling

- Uses Tailwind CSS for styling
- **Color Scheme**:
  - Green for approved status and approve buttons
  - Red for rejected status and reject buttons
  - Gray for pending status
- **Layout**: Responsive table with overflow handling
- **Modal**: Fixed position with semi-transparent backdrop

---

## Implementation Details

- **Reason Truncation**: Shows only first two words of reason with ellipsis
- **Optimistic Updates**: Updates UI state immediately, then reverts if API fails
- **Loading & Error States**: Handled by React Query
- **Conditional Rendering**: Actions only available for pending requests

---

## Best Practices Demonstrated

- **Separation of Concerns**: UI rendering separated from data fetching
- **React Query Usage**: Efficient data fetching with automatic caching
- **Optimistic Updates**: Responsive UI updates with failure fallback
- **Conditional Rendering**: Only shows relevant UI elements based on state
- **Responsive Design**: Table supports overflow for smaller screens

---

## Usage

```jsx
// Import the component
import HostelLeaveAdmin from './path/to/HostelLeaveAdmin';

// Use within a parent component
function ParentComponent() {
  return (
    <div>
      <HostelLeaveAdmin />
    </div>
  );
}
```

> **Note**: The component requires proper setup of React Query's QueryClient provider in the application.

---

## Enhancement Possibilities

- Add pagination for handling large numbers of requests
- Implement filtering by status, date range, or student ID
- Add sorting functionality to table columns
- Include a search feature for finding specific requests
- Add detailed student information display
- Implement bulk actions for handling multiple requests