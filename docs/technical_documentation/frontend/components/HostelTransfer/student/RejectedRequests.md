# RejectedRequests Component 

## Overview

The `RejectedRequests` component is a React functional component designed to display a list of rejected hostel change requests. It provides a user-friendly interface to visualize rejected requests, including relevant information such as application ID, roll number, current hostel, requested hostel, and the reason for rejection.

## Component Props

| Prop | Type | Description |
|------|------|-------------|
| `requests` | Array | An array of objects representing rejected hostel change requests |

Each request object in the array should have the following structure:

```javascript
{
  id: String,          // Application ID
  rollNo: String,      // Student roll number
  currentHostel: String, // Name of current hostel
  requestedHostel: String, // Name of requested hostel
  reason: String       // Reason for rejection
}
```

## Component Behavior

1. If the `requests` array is empty (no rejected requests), the component displays a card with the message "No rejected requests."
2. If there are rejected requests, each request is rendered in a separate card with a red background, displaying all relevant information in a grid layout.

## Visual Elements

The component uses:
- Cards with shadow and border for both empty state and request items
- A grid layout that responds to different screen sizes (single column on small screens, two columns on larger screens)
- Consistent styling with rounded borders, shadows, and proper spacing
- Red background color for rejected requests to visually indicate their status
- Icons for each data field to enhance visual recognition

## Code Explanation

### Empty State Handling

```jsx
if (requests.length === 0) {
  return (
    <div className="card w-full bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">
      No rejected requests.
    </div>
  );
}
```

This code checks if the requests array is empty. If so, it returns a simple card with a message indicating there are no rejected requests.

### Main Component Structure

```jsx
return (
  <div className='card w-full bg-base-100 shadow border border-base200 p-6 rounded-lg'>
    {requests.map(request => (
      // Request item rendering
    ))}
  </div>
);
```

The component returns a container card that houses all rejected request items. It uses the `map` function to iterate through each request in the array and render them individually.

### Request Item Rendering

Each request is rendered as a card with:
- A unique key based on the request ID
- A red background to visually indicate rejection
- A grid layout for organizing information
- Icons and labels for each field

### Data Display Pattern

For each data field (Application ID, Roll Number, Current Hostel, etc.), the component follows a consistent pattern:

```jsx
<div class="flex items-center space-x-3 py-2">
  <div class="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-indigo-200 shadow-sm">
    {/* Icon SVG */}
  </div>
  <div>
    <div class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-0.5">Field Label</div>
    <div class="text-sm font-semibold text-gray-800">{request.fieldValue}</div>
  </div>
</div>
```

This creates a consistent visual hierarchy with:
1. An icon in a circular container on the left
2. A label above the actual data value
3. Proper spacing and alignment of elements

### Responsive Design

The grid layout uses:
```jsx
<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
```

This ensures that on small screens (mobile), the information displays in a single column, while on larger screens (tablets and above), it displays in two columns for better space utilization.

## Usage Example

```jsx
import React from 'react';
import RejectedRequests from './RejectedRequests';

const MyComponent = () => {
  const rejectedRequestsData = [
    {
      id: 'APP123456',
      rollNo: 'CS20B001',
      currentHostel: 'Hostel A',
      requestedHostel: 'Hostel B',
      reason: 'No vacancy available in requested hostel'
    },
    // More rejected requests...
  ];

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Rejected Hostel Change Requests</h2>
      <RejectedRequests requests={rejectedRequestsData} />
    </div>
  );
};

export default MyComponent;
```