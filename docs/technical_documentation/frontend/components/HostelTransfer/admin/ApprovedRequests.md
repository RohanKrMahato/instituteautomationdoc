# ApprovedRequests Component 

## Overview

The `ApprovedRequests` component is a React functional component designed to display a list of approved hostel change requests. It provides a visual interface for users to view approved hostel transfer applications, with relevant details such as application ID, student roll number, previous hostel, and newly approved hostel assignment.

## Component Props

| Prop | Type | Description |
|------|------|-------------|
| `requests` | Array | An array of objects representing approved hostel change requests |

Each request object in the array should have the following structure:

```javascript
{
  id: String,          // Application ID
  rollNo: String,      // Student roll number
  currentHostel: String, // Previous/old hostel name
  requestedHostel: String, // Newly approved hostel name
}
```

## Component Behavior

1. **Empty State Handling**: If the `requests` array is empty, the component displays a card with the message "No approved requests."
2. **Request Display**: When there are approved requests, each request is rendered in a separate card with a green background to visually indicate approval status.
3. **Responsive Layout**: The component uses a grid layout that adjusts based on screen size - displaying in a single column on small screens and two columns on larger screens.

## Visual Elements

The component implements the following visual elements:

- Card containers with subtle shadows and borders
- Green background color for approved request items to indicate positive status
- Responsive grid layout
- Consistent information display pattern:
  - Icon in a circular container
  - Field label in uppercase
  - Field value in semibold text
- Well-spaced content for improved readability
- SVG icons used for visual representation of different data types

## Code Explanation

### Empty State Handling

```jsx
if (requests.length === 0) {
  return (
    <div className="card bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">
      No approved requests.
    </div>
  );
}
```

This section checks if the `requests` array is empty. If no approved requests exist, it returns a simple card with appropriate styling and a message indicating there are no approved requests.

### Main Container Structure

```jsx
return (
  <div className='card bg-base-100 shadow border border-base200 p-6 rounded-lg'>
    {requests.map(request => (
      // Request item rendering
    ))}
  </div>
);
```

The component returns a container card that holds all approved request items. The container has a shadow effect, border, padding, and rounded corners for a clean design. It uses the `map` function to iterate through each request in the array and render individual request cards.

### Individual Request Rendering

```jsx
<div key={request.id} className="mb-4 shadow-sm p-4 border rounded bg-green-100">
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
    {/* Individual fields */}
  </div>
  {/* <p className='mt-2'>Approval Timestamp: {request.approvalTimestamp}</p> */}
</div>
```

Each request is rendered as a card with:
- A unique key derived from the request ID for React's reconciliation process
- Margin at the bottom for separation between cards
- A light shadow and border for depth
- Green background (`bg-green-100`) to indicate approved status
- A responsive grid layout that changes based on screen size


### Field Display Pattern

For each data field (Application ID, Roll Number, etc.), the component follows a consistent pattern:

```jsx
<div class="flex items-center space-x-3 py-2">
  <div class="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-indigo-200 shadow-sm">
    {/* SVG icon */}
  </div>
  <div>
    <div class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-0.5">Field Label</div>
    <div class="text-sm font-semibold text-gray-800">{request.fieldValue}</div>
  </div>
</div>
```

This creates a consistent visual hierarchy with:
1. A flex container for horizontal alignment of icon and text
2. An icon in a circular container with indigo background
3. A separate container for label and value
4. Label text styled as uppercase, gray, and small
5. Value text styled as semibold and slightly larger

### Responsive Design

```jsx
<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
```

This grid layout utilizes Tailwind CSS's responsive classes:
- `grid-cols-1`: By default (on mobile devices), display fields in a single column
- `sm:grid-cols-2`: On small screens and larger, display fields in two columns
- `gap-x-6`: Add horizontal spacing between columns
- `gap-y-1`: Add minimal vertical spacing between rows

## Usage Example

```jsx
import React from 'react';
import ApprovedRequests from './ApprovedRequests';

const HostelTransferPage = () => {
  const approvedRequestsData = [
    {
      id: 'APP123456',
      rollNo: 'CS20B001',
      currentHostel: 'Hostel A',
      requestedHostel: 'Hostel B',
      approvalTimestamp: '2025-04-15T14:30:00Z'
    },
    // More approved requests...
  ];

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Approved Hostel Change Requests</h2>
      <ApprovedRequests requests={approvedRequestsData} />
    </div>
  );
};

export default HostelTransferPage;
```

## Note

1. The component uses Tailwind CSS utility classes for styling.
2. SVG icons are embedded directly in the JSX for better load performance.