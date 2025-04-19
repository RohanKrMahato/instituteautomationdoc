# Admin Drop Requests Component

## Overview

The `AdminDropRequests` component provides an administrative interface for reviewing and processing student course drop requests. This component allows academic administrators to view all drop requests in a tabular format and take appropriate actions (approve or reject).

## Component Structure

The component presents a simple, structured view with:
- A header section with title
- Loading and error states
- A table displaying all drop requests
- Action buttons for pending requests

## Dependencies

```jsx
import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import newRequest from '../../utils/newRequest';
import { FaCheck, FaTimes, FaClock } from 'react-icons/fa';
```

## Data Fetching

The component uses React Query to fetch drop request data:

```jsx
const { isLoading, error, data: dropRequests = [] } = useQuery({
  queryKey: ['adminDropRequests'],
  queryFn: () =>
    newRequest.get('/acadadmin/drop-requests').then((res) => res.data),
});
```

## State Management

The component relies on React Query for state management, with:
- `isLoading`: Tracks loading state
- `error`: Captures any errors during data fetching
- `dropRequests`: Stores the request data

## Mutations

The component includes a mutation for updating drop request status:

```jsx
const updateRequestStatus = useMutation({
  mutationFn: ({ requestId, status, remarks }) =>
    newRequest.patch(`/acadadmin/drop-requests/${requestId}`, { status, remarks }),
  onSuccess: () => {
    queryClient.invalidateQueries(['adminDropRequests']);
  },
});
```

## Utility Functions

### handleStatusUpdate

Handles the status change workflow, prompting for admin remarks:

```jsx
const handleStatusUpdate = (requestId, newStatus) => {
  const remarks = prompt("Enter remarks for this decision:");
  if (remarks !== null) {
    updateRequestStatus.mutate({ requestId, status: newStatus, remarks });
  }
};
```

### getStatusColor

Returns appropriate CSS class based on request status:

```jsx
const getStatusColor = (status) => {
  switch (status) {
    case 'Pending': return 'text-yellow-500';
    case 'Approved': return 'text-green-500';
    case 'Rejected': return 'text-red-500';
    default: return 'text-gray-500';
  }
};
```

## UI Components

### Loading State

Displays a spinner while data is being fetched:

```jsx
{isLoading ? (
  <div className="text-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
    <p className="mt-4">Loading requests...</p>
  </div>
) : null}
```

### Error State

Displays error message if data fetching fails:

```jsx
{error ? (
  <div className="text-red-500 text-center">
    Error loading requests: {error.message}
  </div>
) : null}
```

### Drop Requests Table

Displays all drop requests in a tabular format:

```jsx
<table className="min-w-full bg-white">
  <thead className="bg-gray-100">
    <tr>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Roll Number</th>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Course</th>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Request Date</th>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
    </tr>
  </thead>
  <tbody className="divide-y divide-gray-200">
    {/* Row mapping logic */}
  </tbody>
</table>
```

### Status Indicator

Shows the current status with appropriate icon and color:

```jsx
<span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(request.status)}`}>
  {request.status === 'Pending' ? <FaClock className="mr-1" /> : 
   request.status === 'Approved' ? <FaCheck className="mr-1" /> : 
   <FaTimes className="mr-1" />}
  {request.status}
</span>
```

### Action Buttons

Provides appropriate action buttons for pending requests:

```jsx
{request.status === 'Pending' ? (
  <>
    <button
      onClick={() => handleStatusUpdate(request._id, 'Approved')}
      className="text-green-600 hover:text-green-900 mr-4"
    >
      Approve
    </button>
    <button
      onClick={() => handleStatusUpdate(request._id, 'Rejected')}
      className="text-red-600 hover:text-red-900"
    >
      Reject
    </button>
  </>
) : (
  <span className="text-gray-500">No actions available</span>
)}
```

## Expected Data Structure

The component expects drop request data in the following format:

```javascript
[
  {
    _id: "requestId123",
    studentName: "John Doe",
    rollNo: "B20CS001",
    courseId: "CS101",
    courseName: "Introduction to Computer Science",
    requestDate: "2025-04-10T14:30:00.000Z",
    status: "Pending" | "Approved" | "Rejected",
    // Other request properties
  },
  // More requests...
]
```

## API Endpoints

The component interacts with two API endpoints:

1. `GET /acadadmin/drop-requests` - Fetches all drop requests
2. `PATCH /acadadmin/drop-requests/:requestId` - Updates a drop request status

## Workflow

1. The component loads and displays all drop requests from the system
2. For pending requests, admin can choose to approve or reject
3. When an action is taken, admin is prompted to enter remarks
4. The status is updated and the list is refreshed automatically
5. Processed requests (approved/rejected) show their status but no longer have action buttons

## Error Handling

The component implements basic error handling:
- Displays error messages if API requests fail
- Uses default empty array for drop requests if data is undefined
- Checks for null response when prompting for remarks

## Styling

The component uses Tailwind CSS for styling:
- Color-coded status indicators (yellow for pending, green for approved, red for rejected)
- Responsive table with appropriate spacing
- Clear action buttons
- Loading spinner for better UX during data fetching

## Accessibility

The component includes:
- Semantic HTML structure with proper table markup
- Visual indicators with text labels
- Informative button text

