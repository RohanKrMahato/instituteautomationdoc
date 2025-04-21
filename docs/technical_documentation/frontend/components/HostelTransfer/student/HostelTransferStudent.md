# HostelTransferStudent Component 

## Overview

The `HostelTransferStudent` component is a comprehensive React interface for managing hostel transfer requests from a student's perspective. It provides functionality for:

1. Viewing pending, approved, and rejected transfer requests
2. Submitting new hostel transfer requests
3. Filtering available hostels based on student gender

The component uses React Query for data fetching, local state management for UI interactions, and follows a responsive design pattern.

## Component Structure

### Dependencies

```jsx
import React, { useEffect, useState } from 'react';
import { useQuery } from "@tanstack/react-query";
import newRequest from "../../../utils/newRequest";
import ApprovedRequests from './ApprovedRequests';
import RejectedRequests from './RejectedRequests';
```

- React and hooks for component structure and state management
- React Query (`@tanstack/react-query`) for data fetching
- Custom `newRequest` utility for API calls
- Child components for displaying approved and rejected requests

### Data Flow

1. User data is retrieved from localStorage
2. Student details are fetched using React Query
3. Transfer requests are fetched and processed
4. UI state is managed with React useState hooks
5. Form data is collected and submitted via API calls

## Technical Implementation

### State Management

The component manages multiple state variables:

```jsx
const [activeTab, setActiveTab] = useState('pending');
const [availableHostels, setAvailableHostels] = useState([]);
const [selectedHostel, setSelectedHostel] = useState('');
const [currentHostel, setCurrentHostel] = useState('');
const [requests, setRequests] = useState([]);
const [pendingRequests, setPendingRequests] = useState([]);
const [approvedRequests, setApprovedRequests] = useState([]);
const [rejectedRequests, setRejectedRequests] = useState([]);
const [showForm, setShowForm] = useState(false);
const [reason, setReason] = useState('');
const [requestPending, setRequestPending] = useState(false);
const [responseMessage, setResponseMessage] = useState('');
```

These state variables handle:
- Tab navigation
- Hostel selection options
- Request data categorization
- Form visibility and input values
- Loading and error states
- Feedback messages

### Data Fetching

React Query is used to fetch student data and transfer requests:

```jsx
const { isLoading, error, data } = useQuery({
  queryKey: [`${userId}`],
  queryFn: () =>
    newRequest.get(`/student/${userId}`).then((res) => {
      return res.data;
    }),
});

const { isLoading: isLoadingRequests, error: errorRequests, data: transferRequests } = useQuery({
  queryKey: ["transferRequests"],
  queryFn: () =>
    newRequest.get(`/hostel/${userId}/transfer-requests`).then((res) => {
      return res.data;
    }),
});
```

This approach provides:
- Automatic caching
- Loading and error states
- Consistent data fetching patterns

### Side Effects

The component uses multiple `useEffect` hooks to:

1. Determine available hostels based on student gender:
   ```jsx
   useEffect(() => {
     if (data) {
       setCurrentHostel(data?.hostel);
       const gender = allHostels.boy.includes(data?.hostel) ? 'boy' : 'girl';
       const filteredHostels = allHostels[gender].filter(hostel => hostel !== data?.hostel);
       setAvailableHostels(filteredHostels);
     }
   }, [data]);
   ```

2. Process fetched transfer requests:
   ```jsx
   useEffect(() => {
     if (!isLoadingRequests && !errorRequests && transferRequests) {
       setRequests(transferRequests.map(item => ({
         id: item._id,
         rollNo: item.rollNo,
         requestedHostel: item.requestedHostel,
         currentHostel: item.currentHostel,
         reason: item.reason,
         status: item.status
       })));
     }
   }, [transferRequests, isLoadingRequests, errorRequests]);
   ```

3. Categorize requests by status:
   ```jsx
   useEffect(() => {
     if (requests) {
       setPendingRequests(requests.filter(req => req.status === 'Pending'));
       setApprovedRequests(requests.filter(req => req.status === 'Approved'));
       setRejectedRequests(requests.filter(req => req.status === 'Rejected'));
     }
   }, [requests]);
   ```

### Form Handling

The component handles form submission with validation and error handling:

```jsx
const handleTransferRequest = async (e) => {
  e.preventDefault();
  setResponseMessage('');

  if (!selectedHostel || !reason.trim()) {
    setResponseMessage('Please fill all fields.');
    return;
  }

  setRequestPending(true);

  try {
    const newReq = {
      status: 'Pending',
      studentId: data?.rollNo,
      currentHostel,
      requestedHostel: selectedHostel,
      reason,
    };

    await newRequest.post('/hostel/transfer', newReq);
    setPendingRequests([...pendingRequests, newReq]);
    handleDiscard();
  } catch (error) {
    setResponseMessage('An error occurred while processing your request. Please try again.');
  } finally {
    setRequestPending(false);
  }
};
```

This implementation:
- Prevents default form submission
- Validates required fields
- Handles loading states
- Uses try/catch for error handling
- Updates UI state on success
- Provides user feedback

## UI Components

### Tab Navigation

```jsx
<div className="flex justify-around w-full mb-6">
  <button 
    onClick={() => setActiveTab('pending')}
    className={`flex items-center px-5 py-2.5 shadow rounded-md text-sm font-medium transition-all duration-200 ease-out focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-50 ${activeTab === 'pending' ? 'bg-indigo-700 text-white' : 'bg-gray-200'} text-indigo-700`}>
    Pending
  </button>
  {/* Similar buttons for "approved" and "rejected" tabs */}
</div>
```

The tabs:
- Display different request categories
- Use conditional styling based on active state
- Include accessibility features (focus styles)

### Content Sections

Each tab displays a different view:

1. **Pending Tab**:
   - Shows pending requests or empty state
   - Displays "Apply for Transfer" button when no pending requests exist
   - Shows the transfer request form when activated

2. **Approved Tab**:
   - Uses the `ApprovedRequests` component to display approved transfers

3. **Rejected Tab**:
   - Uses the `RejectedRequests` component to display rejected transfers

### Transfer Request Form

```jsx
<div className="mt-6 bg-gray-50 p-6 rounded-lg shadow-md w-[80%]">
  <div className="flex items-center space-x-3 pt-1 pb-3 mb-2 border-b">
    <div className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-0.5">Current Hostel : {currentHostel}</div>
  </div>
  <form onSubmit={handleTransferRequest} className="space-y-4">
    {/* Form fields */}
    <div className="flex justify-end space-x-4">
      <button type="button" className="bg-gray-400 text-white py-2 px-4 rounded-lg hover:bg-gray-500 transition" onClick={handleDiscard}>Discard</button>
      <button
        type="submit"
        className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition"
        disabled={requestPending}
      >
        {requestPending ? 'Submitting...' : 'Submit'}
      </button>
    </div>
  </form>
</div>
```

The form includes:
- Current hostel information
- Dropdown for selecting new hostel (filtered by gender)
- Textarea for reason input
- Submit and cancel buttons
- Loading state indication
- Responsive design

## Data Structures

### Student Data

Expected structure from student API:
```
{
  hostel: string,  // Current hostel name
  rollNo: string   // Student roll number
}
```

### Transfer Request Data

Structure after processing:
```
{
  id: string,              // Request ID
  rollNo: string,          // Student roll number
  requestedHostel: string, // Target hostel
  currentHostel: string,   // Original hostel
  reason: string,          // Justification for transfer
  status: string           // "Pending", "Approved", or "Rejected"
}
```

### Hostel Categories

```jsx
const allHostels = {
  boy: ['Brahmaputra', 'Lohit', 'Gaurang', 'Disang', 'Kapili', 'Manas', 'Dihing', 'Barak', 'Siang', 'Kameng', 'Umiam', 'Married Scholar'],
  girl: ['Dhansiri', 'Disang', 'Subhansiri'],
};
```

This structure allows the component to:
- Determine student gender based on current hostel
- Filter available hostels based on gender
- Exclude current hostel from available options

## Integration Points

1. **API Endpoints**:
   - `/student/${userId}` - Fetches student details
   - `/hostel/${userId}/transfer-requests` - Fetches transfer requests
   - `/hostel/transfer` - Creates new transfer requests

2. **Child Components**:
   - `ApprovedRequests` - Displays approved transfer requests
   - `RejectedRequests` - Displays rejected transfer requests

3. **Authentication**:
   - User data retrieved from localStorage (`currentUser`)

## Error Handling

The component implements several error handling mechanisms:

1. React Query error states for API requests
2. Form validation for required fields
3. Try/catch blocks for API requests
4. User feedback messages for errors
5. Loading states during asynchronous operations

## Code Explanation

### User Authentication and Data Fetching

The component starts by retrieving the logged-in user's data:

```jsx
const { data: userData } = JSON.parse(localStorage.getItem("currentUser"));
const { email, userId } = userData.user;
```

It then uses React Query to fetch the student's details:

```jsx
const { isLoading, error, data } = useQuery({
  queryKey: [`${userId}`],
  queryFn: () =>
    newRequest.get(`/student/${userId}`).then((res) => {
      return res.data;
    }),
});
```

This establishes the foundational data needed for the component's operation.

### Gender-Based Hostel Filtering

The component determines available hostels based on the student's current hostel:

```jsx
useEffect(() => {
  if (data) {
    setCurrentHostel(data?.hostel);
    const gender = allHostels.boy.includes(data?.hostel) ? 'boy' : 'girl';
    const filteredHostels = allHostels[gender].filter(hostel => hostel !== data?.hostel);
    setAvailableHostels(filteredHostels);
  }
}, [data]);
```

This clever approach:
1. Infers gender based on current hostel name
2. Filters hostel list to match gender
3. Removes current hostel from available options

### Transfer Request Processing

The component fetches and processes transfer requests:

```jsx
const { isLoading: isLoadingRequests, error: errorRequests, data: transferRequests } = useQuery({
  queryKey: ["transferRequests"],
  queryFn: () =>
    newRequest.get(`/hostel/${userId}/transfer-requests`).then((res) => {
      return res.data;
    }),
});

useEffect(() => {
  if (!isLoadingRequests && !errorRequests && transferRequests) {
    setRequests(transferRequests.map(item => ({
      id: item._id,
      rollNo: item.rollNo,
      requestedHostel: item.requestedHostel,
      currentHostel: item.currentHostel,
      reason: item.reason,
      status: item.status
    })));
  }
}, [transferRequests, isLoadingRequests, errorRequests]);
```

This code:
1. Fetches transfer requests using React Query
2. Processes data when available
3. Maps API response to a consistent data structure

### Request Categorization

```jsx
useEffect(() => {
  if (requests) {
    setPendingRequests(requests.filter(req => req.status === 'Pending'));
    setApprovedRequests(requests.filter(req => req.status === 'Approved'));
    setRejectedRequests(requests.filter(req => req.status === 'Rejected'));
  }
}, [requests]);
```

This effect categorizes requests by status whenever the main requests array changes, ensuring the UI displays the correct data in each tab.

### Conditional UI Rendering

The component uses conditional rendering extensively:

```jsx
{activeTab === 'pending' && (
  <>
    {pendingRequests.length === 0 ? (
      <p className="card w-full bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">No pending requests</p>
    ) : (
      <div className="space-y-3">
        {pendingRequests.map((req, index) => (
          <div key={index} className="p-4 bg-gray-200 rounded-lg shadow">
            <p><strong>Current Hostel:</strong> {req.currentHostel}</p>
            <p><strong>Requested Hostel:</strong> {req.requestedHostel}</p>
            <p><strong>Reason:</strong> {req.reason}</p>
            <p><strong>Status:</strong> {req.status}</p>
          </div>
        ))}
      </div>
    )}

    {pendingRequests.length === 0 && !showForm && (
      <button className="mt-4 bg-indigo-700 text-white py-2 px-4 rounded-lg shadow hover:bg-blue-600 transition" onClick={handleOpenForm}>
        Apply for Transfer
      </button>
    )}
  </>
)}
```

This approach:
1. Shows content only for the active tab
2. Handles empty states with friendly messages
3. Displays the "Apply" button only when appropriate
4. Renders request details in a consistent format