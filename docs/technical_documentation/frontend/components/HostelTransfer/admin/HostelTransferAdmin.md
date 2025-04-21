# Hostel Transfer Admin 

## Overview

The `HostelTransferAdmin` component is a React-based interface for managing hostel transfer requests within an administrative dashboard. It provides a tabbed interface for viewing and handling requests at different stages: pending, approved, and rejected.

## Component Architecture

The component uses React Query for data fetching and React's state management to organize and display hostel transfer requests. The interface is divided into three tabs that allow administrators to:

1. View pending requests and take action (approve or reject)
2. View previously approved requests
3. View previously rejected requests

## Technical Details

### Data Flow

```
API Request → React Query → Component State → UI Rendering
```

### Dependencies

- **@tanstack/react-query**: Handles data fetching, caching, and state management for API calls
- **React**: Core library for the component-based UI
- **Custom Utility**: `newRequest` for API communication

### State Management

The component maintains several state variables:

| State Variable | Purpose |
|----------------|---------|
| `requests` | Stores all transfer requests |
| `pendingRequests` | Filtered list of requests with "Pending" status |
| `approvedRequests` | Filtered list of requests with "Approved" status |
| `rejectedRequests` | Filtered list of requests with "Rejected" status |
| `activeTab` | Controls which tab is currently displayed |

### API Integration

- **GET `/hostel/transfer-requests`**: Fetches all transfer requests
- **PUT `/hostel/transfer-requests/:id`**: Updates a request's status and related information

## Component Workflow

1. **Initialization**: 
   - Component mounts and triggers the React Query hook to fetch transfer requests
   - Default tab is set to 'pending'

2. **Data Processing**:
   - When data is received, it's transformed and stored in the `requests` state
   - A separate effect sorts requests into appropriate categories based on status

3. **User Interaction**:
   - Admin can switch between tabs to view different request statuses
   - For pending requests, admin can approve or reject with additional information
   - Action updates are sent to the API and local state is updated accordingly

## Request Handling

The `handleAction` function processes admin decisions:

```javascript
handleAction(id, newStatus, newReason, newHostel, rollNo)
```

| Parameter | Description |
|-----------|-------------|
| `id` | Request identifier |
| `newStatus` | Updated status (Approved/Rejected) |
| `newReason` | Justification for the decision |
| `newHostel` | New hostel assignment (for approved requests) |
| `rollNo` | Student identification number |

## UI Components

The main component imports and conditionally renders three sub-components:

1. `PendingRequests`: Displays actionable pending requests
2. `ApprovedRequests`: Displays history of approved requests
3. `RejectedRequests`: Displays history of rejected requests

## Code Explanation

### Initial Setup and Data Fetching

```javascript
// State initialization with useState hooks
const [requests, setRequests] = useState([]);
const [pendingRequests, setPendingRequests] = useState([]);
const [approvedRequests, setApprovedRequests] = useState([]);
const [rejectedRequests, setRejectedRequests] = useState([]);
const [activeTab, setActiveTab] = useState('pending');

// Data fetching with React Query
const { isLoading, error, data } = useQuery({
  queryKey: ["transfer-requests"],
  queryFn: () => newRequest.get(`/hostel/transfer-requests`).then((res) => res.data),
});
```

The component initializes state variables and sets up a React Query hook to fetch data from the API. The `queryKey` is used for caching purposes, and the `queryFn` defines how to fetch the data.

### Data Processing

```javascript
useEffect(() => {
  if (!isLoading && !error && data) {
    setRequests(data.map(item => ({
      id: item._id,
      rollNo: item.rollNo,
      requestedHostel: item.requestedHostel,
      currentHostel: item.currentHostel,
      reason: item.reason,
      status: item.status
    })));
  }
}, [data, isLoading, error]);

useEffect(() => {
  if (requests) {
    setPendingRequests(requests.filter(req => req.status === 'Pending'));
    setApprovedRequests(requests.filter(req => req.status === 'Approved'));
    setRejectedRequests(requests.filter(req => req.status === 'Rejected'));
  }
}, [requests]);
```

Two `useEffect` hooks process the data:
1. The first transforms raw API data into a more usable format
2. The second categorizes requests based on their status

### Request Action Handler

```javascript
const handleAction = (id, newStatus, newReason, newHostel, rollNo) => {
  newRequest.put(`/hostel/transfer-requests/${id}`, { 
    status: newStatus, 
    reason: newReason, 
    newHostel: newHostel, 
    rollNo: rollNo
  })
    .then(response => {
      console.log('Status updated successfully');
      // Update local state based on new status
      setPendingRequests(prev => prev.filter(req => req.id !== id));
      if (newStatus === 'Approved') {
        setApprovedRequests(prev => [...prev, { ...response.data, status: newStatus }]);
      } else if (newStatus === 'Rejected') {
        setRejectedRequests(prev => [...prev, { ...response.data, status: newStatus }]);
      }
    })
    .catch(error => {
      console.error('Error updating status:', error);
    });
};
```

This function:
1. Sends an update to the API with the new status and additional information
2. Updates local state to maintain UI consistency without requiring a new fetch
3. Moves the request from pending to either approved or rejected based on the action

### UI Rendering

```javascript
return (
  <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md">
    {/* Tab navigation buttons */}
    <div class="flex justify-around mb-6 p-1 space-x-1">
      {/* Tab buttons with conditional styling based on activeTab */}
    </div>

    {/* Conditional rendering based on active tab */}
    {activeTab === 'pending' && (
      <PendingRequests
        requests={pendingRequests}
        handleAction={handleAction}
      />
    )}

    {activeTab === 'approved' && (
      <ApprovedRequests requests={approvedRequests} />
    )}

    {activeTab === 'rejected' && (
      <RejectedRequests requests={rejectedRequests} />
    )}
  </div>
);
```

The UI consists of:
1. A container with styling
2. Tab navigation buttons that update the `activeTab` state
3. Conditional rendering of different components based on the active tab