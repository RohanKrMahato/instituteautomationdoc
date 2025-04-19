# Drop Course Component 

## Overview

The `DropCourse` component provides a user interface for students to request course drops, view pending drop requests, and check their drop request history. The component handles data fetching, user confirmation, and request submission through a clean and responsive interface.

## Component Structure

The component is organized into several logical sections:
- Currently Enrolled Courses
- Pending Drop Requests
- Drop Request History
- Information Section

## Dependencies

```jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { 
  FaRegClock, FaBookOpen, FaExclamationTriangle, 
  FaCheck, FaTimes, FaHistory 
} from "react-icons/fa";
import newRequest from '../../utils/newRequest';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
```

## Helper Components

### StatusIcon

A utility component that renders appropriate icons based on request status:

```jsx
const StatusIcon = ({ status }) => {
  switch (status) {
    case 'Approved':
      return <FaCheck className="text-green-500 mr-2" />;
    case 'Rejected':
      return <FaTimes className="text-red-500 mr-2" />;
    case 'Pending':
      return <FaRegClock className="text-yellow-500 mr-2" />;
    default:
      return null;
  }
};
```

## Authentication

The component retrieves the user ID from local storage:

```jsx
const {data:userData} = JSON.parse(localStorage.getItem("currentUser"));
const {userId} = userData.user;
```

## Data Fetching

### Enrolled Courses

Fetches the student's currently enrolled courses:

```jsx
const { 
  isLoading: coursesLoading, 
  error: coursesError, 
  data: enrolledCourses = [] 
} = useQuery({
  queryKey: ["studentCourses"],
  queryFn: () =>
    newRequest.get(`/student/${userId}/courses`).then((res) => {
      return res.data.courses || [];
    }),
});
```

### Drop Requests

Fetches all drop requests (both pending and historical):

```jsx
const { 
  isLoading: requestsLoading, 
  error: requestsError, 
  data: dropRequests = [] 
} = useQuery({
  queryKey: ["dropRequests"],
  queryFn: () =>
    newRequest.get(`/student/${userId}/drop-requests`).then((res) => {
      return res.data || [];
    }),
});
```

## State Management

The component uses React Query for state management and data fetching. Local state is derived from the fetched data:

```jsx
// Create a map of pending course drop requests for filtering
const pendingDropRequestsMap = new Map();
dropRequests.forEach(request => {
  if (request.status === 'Pending') {
    pendingDropRequestsMap.set(request.courseId, request);
  }
});

// Filter out courses that already have pending drop requests
const availableForDrop = enrolledCourses.filter(course => 
  !pendingDropRequestsMap.has(course.id)
);

// Get pending drop requests
const pendingRequests = dropRequests.filter(request => request.status === 'Pending');

// Get non-pending (history) drop requests
const historyRequests = dropRequests.filter(request => request.status !== 'Pending');
```

## Mutations

### Create Drop Request

Creates a new course drop request:

```jsx
const createDropRequest = useMutation({
  mutationFn: (courseId) => {
    return newRequest.post(`/student/${userId}/drop-requests`, { courseId });
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["dropRequests"] });
    queryClient.invalidateQueries({ queryKey: ["studentCourses"] });
  },
});
```

### Cancel Drop Request

Cancels a pending drop request:

```jsx
const cancelDropRequest = useMutation({
  mutationFn: (requestId) => {
    return newRequest.delete(`/student/${userId}/drop-requests/${requestId}`);
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["dropRequests"] });
    queryClient.invalidateQueries({ queryKey: ["studentCourses"] });
  },
});
```

## Handler Functions

### Request Drop Course

Handles the confirmation and submission of drop requests:

```jsx
const handleRequestDropCourse = (courseId, courseName) => {
  if (window.confirm(`Are you sure you want to request dropping ${courseName}?`)) {
    createDropRequest.mutate(courseId, {
      onSuccess: () => {
        alert("Drop request submitted successfully. You will be notified when it's processed.");
      },
      onError: (error) => {
        alert(error.response?.data?.message || "Failed to submit drop request. Please try again.");
      }
    });
  }
};
```

### Cancel Drop Request

Handles the confirmation and cancellation of pending drop requests:

```jsx
const handleCancelDropRequest = (requestId, courseName) => {
  if (window.confirm(`Are you sure you want to cancel your request to drop ${courseName}?`)) {
    cancelDropRequest.mutate(requestId, {
      onSuccess: () => {
        alert("Drop request cancelled successfully.");
      },
      onError: (error) => {
        alert(error.response?.data?.message || "Failed to cancel drop request. Please try again.");
      }
    });
  }
};
```

## UI Components

### Loading State

Displays a loading spinner when data is being fetched:

```jsx
{isLoading ? (
  <div className="bg-gray-100 p-8 rounded-lg text-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto mb-4"></div>
    <p className="text-gray-700">Loading your courses...</p>
  </div>
) : /* ... */}
```

### Error State

Displays an error message if data fetching fails:

```jsx
{error ? (
  <div className="bg-red-100 p-8 rounded-lg text-center">
    <p className="text-red-700 text-lg mb-4">{error.message || "Failed to fetch courses"}</p>
    <Link
      to="/courses"
      className="bg-pink-500 text-white py-2 px-6 rounded-md font-medium hover:bg-pink-600 transition duration-300"
    >
      Back to My Courses
    </Link>
  </div>
) : /* ... */}
```

### Enrolled Courses Section

Displays courses that are available for dropping:

```jsx
{availableForDrop.length === 0 ? (
  <div className="bg-gray-100 p-6 rounded-lg text-center">
    <p className="text-gray-700">You don't have any courses available for dropping.</p>
    {enrolledCourses.length > 0 && pendingDropRequestsMap.size > 0 && (
      <p className="text-gray-500 text-sm mt-2">
        All your enrolled courses already have pending drop requests.
      </p>
    )}
  </div>
) : (
  <div className="grid grid-cols-1 gap-4">
    {availableForDrop.map((course) => (
      <div key={course.id} className="bg-white rounded-lg shadow border border-gray-200 hover:shadow-md transition duration-300">
        {/* Course card content */}
      </div>
    ))}
  </div>
)}
```

### Pending Drop Requests Section

Displays pending drop requests with an option to cancel:

```jsx
{pendingRequests.length > 0 && (
  <div>
    <h2 className="text-xl font-semibold mb-4 text-gray-700 flex items-center">
      <FaRegClock className="mr-2 text-yellow-500" />
      Pending Drop Requests
    </h2>
    
    <div className="grid grid-cols-1 gap-4">
      {pendingRequests.map((request) => (
        <div key={request._id} className="bg-yellow-50 rounded-lg shadow border border-yellow-200 hover:shadow-md transition duration-300">
          {/* Request card content */}
        </div>
      ))}
    </div>
  </div>
)}
```

### Drop Request History Section

Displays historical drop requests with their status:

```jsx
{historyRequests.length > 0 && (
  <div>
    <h2 className="text-xl font-semibold mb-4 text-gray-700 flex items-center">
      <FaHistory className="mr-2 text-purple-500" />
      Drop Request History
    </h2>
    <div className="grid grid-cols-1 gap-4">
      {historyRequests.map((request) => (
        <div key={request._id} className={`bg-white rounded-lg shadow border ${
          request.status === 'Approved' ? 'border-green-200' : 
          request.status === 'Rejected' ? 'border-red-200' : 
          'border-gray-200'}`}>
          {/* History request card content */}
        </div>
      ))}
    </div>
  </div>
)}
```

### Information Section

Displays important information about the course drop process:

```jsx
<div className="bg-blue-50 p-5 rounded-lg border border-blue-200">
  <h3 className="font-semibold text-blue-800 mb-3 flex items-center">
    <FaExclamationTriangle className="mr-2" />
    Important Information
  </h3>
  <ul className="list-disc pl-5 text-blue-700 text-sm space-y-2">
    <li>Course drop requests are subject to approval by the administration.</li>
    {/* More information items */}
  </ul>
</div>
```

## Expected Data Structures

### Enrolled Course

```javascript
{
  id: "CS101",
  name: "Introduction to Computer Science",
  credits: 4,
  // Other course properties
}
```

### Drop Request

```javascript
{
  _id: "requestId123",
  courseId: "CS101",
  courseName: "Introduction to Computer Science",
  status: "Pending" | "Approved" | "Rejected",
  requestDate: "2025-04-10T14:30:00.000Z",
  decisionDate: "2025-04-12T09:15:00.000Z",  // Only for Approved/Rejected
  remarks: "Request approved based on valid reasons",  // Optional
  // Other request properties
}
```

## Error Handling

The component handles errors in data fetching and mutations:

- Displays error messages for failed API requests
- Shows user-friendly alerts for mutation failures
- Provides appropriate UI states when data is not available

## Navigation

The component includes a navigation link back to the courses page:

```jsx
<div className="mt-8 text-center">
  <Link
    to="/courses"
    className="inline-flex items-center text-pink-600 hover:text-pink-700"
  >
    Back to My Courses
  </Link>
</div>
```

## Styling

The component uses Tailwind CSS for styling with a consistent color scheme:
- Pink for primary actions and branding
- Yellow for pending status
- Green for approved status
- Red for rejected status
- Blue for information

## Accessibility Features

The component includes:
- Semantic HTML structure
- Color indicators with text alternatives
- Proper button states for loading/disabled conditions
- Responsive design for different screen sizes

## Best Practices

The component follows several best practices:
- Confirmation dialogs for destructive actions
- Clear visual indicators for different statuses
- Informative feedback after actions
- Comprehensive error handling
- Clean separation of concerns with helper components