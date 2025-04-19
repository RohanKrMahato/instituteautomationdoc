# AdminSubscriptionRequests Component

## Overview

The `AdminSubscriptionRequests` component is a React-based interface designed for managing meal plan subscription requests in a university or institutional food service system. This component allows administrators to view, filter, approve, and reject meal plan change requests submitted by students.

## Features

- **Request Visualization**: Displays all subscription requests in a card-based grid layout
- **Filtering System**: Allows filtering requests by status (All, Pending, Approved, Rejected)
- **Search Functionality**: Enables searching for specific students by name or ID
- **Request Actions**: Provides options to approve or reject pending requests
- **Rejection Workflow**: Includes a modal dialog for providing rejection reasons

## Component Structure

### State Management

The component uses React's `useState` hooks to manage the following state variables:

| State Variable | Type | Description |
|----------------|------|-------------|
| `requests` | Array | Collection of subscription request objects |
| `selectedRequest` | Object/null | Currently selected request for actions |
| `searchTerm` | String | Text input for filtering requests by student name/ID |
| `filterStatus` | String | Selected status filter ("ALL", "PENDING", "APPROVED", "REJECTED") |
| `rejectionReason` | String | Text explanation when rejecting a request |
| `showRejectionDialog` | Boolean | Controls visibility of the rejection modal |
| `isProcessing` | Boolean | Indicates when an action is being processed |

### Data Structure

Each request object contains:

```javascript
{
  _id: String,              // Unique identifier
  studentId: {              // Student information
    name: String,           // Student name
    studentId: String       // Student ID number
  },
  currentPlan: String,      // Current meal plan description
  newPlan: String,          // Requested meal plan description
  status: String,           // Request status (PENDING, APPROVED, REJECTED)
  createdAt: String,        // ISO date string for request creation time
  rejectionReason: String   // Optional explanation if request is rejected
}
```

## Key Functions

### Filtering Logic

```javascript
const filteredRequests = requests.filter(request => {
  const matchesSearch = 
    (request.studentId?.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (request.studentId?.studentId || '').toString().includes(searchTerm);
  
  const matchesFilter = 
    filterStatus === 'ALL' || 
    request.status === filterStatus;
  
  return matchesSearch && matchesFilter;
});
```

### Action Handler

```javascript
const handleRequestAction = async (status) => {
  if (!selectedRequest) return;

  if (status === 'REJECTED') {
    setShowRejectionDialog(true);
    return;
  }

  // Simulate API call with timeout
  setIsProcessing(true);
  setTimeout(() => {
    const updatedRequests = requests.map(req => 
      req._id === selectedRequest._id ? { ...req, status } : req
    );
    setRequests(updatedRequests);
    setSelectedRequest(null);
    setIsProcessing(false);
  }, 800); // Simulate network delay
};
```

### Rejection Confirmation

```javascript
const handleRejectConfirm = async () => {
  // Simulate API call with timeout
  setIsProcessing(true);
  setTimeout(() => {
    const updatedRequests = requests.map(req => 
      req._id === selectedRequest._id 
        ? { ...req, status: 'REJECTED', rejectionReason } 
        : req
    );
    setRequests(updatedRequests);
    setSelectedRequest(null);
    setRejectionReason('');
    setShowRejectionDialog(false);
    setIsProcessing(false);
  }, 800); // Simulate network delay
};
```

## UI Components

### Status Badge Generator

```javascript
const getStatusBadge = (status) => {
  const statusConfig = {
    PENDING: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-200' },
    APPROVED: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-200' },
    REJECTED: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-200' }
  };
  
  const config = statusConfig[status] || { bg: 'bg-gray-100', text: 'text-gray-800', border: 'border-gray-200' };
  
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.bg} ${config.text} ${config.border}`}>
      {status}
    </span>
  );
};
```

## Usage

The component is designed to be included in an admin dashboard. It works with demo data in its current implementation but could be modified to fetch data from an API.

```jsx
import AdminSubscriptionRequests from './components/AdminSubscriptionRequests';

function AdminDashboard() {
  return (
    <div className="dashboard-container">
      <h1>Admin Dashboard</h1>
      <AdminSubscriptionRequests />
    </div>
  );
}
```

## Styling

The component utilizes:
- Tailwind CSS for utility-based styling
- Custom CSS imported from `./styles/AdminSubscriptionRequests.css`
- FontAwesome React icons (`react-icons/fa`) for visual elements

## Implementation Notes

1. Currently uses hardcoded demo data in `demoRequests`
2. Simulates API calls with `setTimeout()` 
3. Uses responsive design with grid layout that adjusts based on screen size


## Dependencies

- React
- react-icons/fa
- Tailwind CSS (implied by class usage)