# PendingRequests Component 

## Overview

The `PendingRequests` component is a React component designed to display and manage pending hostel transfer requests. It provides administrators with the ability to view request details and take action on them (approve or reject). The component handles both the display of requests and the collection of rejection reasons when an administrator chooses to reject a request.

## Component Structure

### Dependencies

```jsx
import React from 'react';
```

The component only requires React as a dependency.

### Props

| Prop | Type | Description |
|------|------|-------------|
| `requests` | Array | Array of pending hostel transfer request objects |
| `onApprove` | Function | Handler function called when a request is approved |
| `onReject` | Function | Handler function called when a request is rejected with a reason |
| `rejectionReasons` | Object | Key-value pairs mapping request IDs to rejection reason text |
| `handleReasonChange` | Function | Handler function called when rejection reason text changes |

## Technical Implementation

### Empty State Handling

The component first checks if there are any pending requests:

```jsx
if (requests.length === 0) {
  return (
    <div className="card bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">
      No pending requests.
    </div>
  );
}
```

This ensures a clear message is shown when there are no requests to process.

### Request Items Display

When requests exist, the component maps through them to create individual request cards:

```jsx
{requests.map(request => (
  <div key={request.id} className="border rounded-lg shadow-sm mb-4 p-4">
    {/* Request details */}
  </div>
))}
```

Each request card contains:
- Student information (name and roll number)
- Hostel transfer details (current hostel and reason)
- Action buttons for approval or rejection
- Conditional textarea for rejection reasons

### Rejection Flow

The component implements a two-step rejection process:

1. Click "Reject" button to show rejection reason textarea:
   ```jsx
   <button
     onClick={() => handleReasonChange(request.id, '')}
     className="bg-red-500 max-h-10 shadow-sm text-white px-4 py-2 rounded hover:scale-105 transition duration-200"
   >
     Reject
   </button>
   ```

2. Enter rejection reason and submit:
   ```jsx
   {rejectionReasons.hasOwnProperty(request.id) && (
     <div className="mt-2">
       <textarea
         value={rejectionReasons[request.id]}
         onChange={(e) => handleReasonChange(request.id, e.target.value)}
         placeholder="Enter reason for rejection"
         className="w-full shadow-sm border border-gray-300 rounded p-2 mb-2"
       />
       <button
         onClick={() => onReject(request)}
         className="bg-red-500 shadow-sm text-white px-4 py-2 rounded hover:scale-105 transition duration-200"
       >
         Submit Rejection
       </button>
     </div>
   )}
   ```

This design ensures administrators provide a reason when rejecting a request.

## Data Structure

Each request object in the `requests` array is expected to have the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Unique identifier for the request |
| `studentName` | String | Name of the student making the transfer request |
| `studentId` | String | Roll number of the student |
| `currentHostel` | String | The student's current hostel assignment |
| `reason` | String | The student's stated reason for requesting a transfer |

The `rejectionReasons` object maps request IDs to strings:

```
{
  "request123": "Room not available in requested hostel",
  "request456": "Insufficient documentation provided"
}
```

## UI Components

### Request Card

Each request is presented in a card with a consistent layout:
- Rounded borders and subtle shadow
- Grid layout for information display
- Visual icons for each information type
- Consistent spacing and alignment

### Information Items

Each piece of information follows a consistent pattern:

```jsx
<div class="flex items-center space-x-3 py-2">
  <div class="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-indigo-200 shadow-sm">
    {/* SVG icon */}
  </div>
  <div>
    <div class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-0.5">{Label}</div>
    <div class="text-sm font-semibold text-gray-800">{Value}</div>
  </div>
</div>
```

This design creates a consistent, scannable interface with:
- Circular icon container with indigo accent colors
- Two-level text hierarchy (label and value)
- Consistent spacing

### Action Buttons

The component provides clearly distinguished action buttons:
- Green "Approve" button for positive action
- Red "Reject" button for negative action
- Hover animations for better interactivity
- Consistent styling with the application design system

## Code Explanation

### Component Function

The component is structured as a function that accepts props and returns JSX:

```jsx
const PendingRequests = ({ requests, onApprove, onReject, rejectionReasons, handleReasonChange }) => {
  // Component logic and rendering
};
```

This follows React's functional component pattern, using destructuring to access props directly.

### Conditional Rendering

The component uses conditional rendering in two places:

1. To show an empty state message when no requests exist:
   ```jsx
   if (requests.length === 0) {
     return (
       <div className="card bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">
         No pending requests.
       </div>
     );
   }
   ```

2. To show or hide the rejection reason textarea:
   ```jsx
   {rejectionReasons.hasOwnProperty(request.id) && (
     <div className="mt-2">
       {/* Rejection reason textarea and submit button */}
     </div>
   )}
   ```

This ensures the UI shows only relevant elements based on the current state.

### Event Handling

The component delegates event handling to parent components through props:

- `onApprove(request)` is called when an approval button is clicked
- `handleReasonChange(request.id, '')` is called when a rejection button is clicked
- `handleReasonChange(request.id, e.target.value)` is called when rejection reason text changes
- `onReject(request)` is called when a rejection is submitted with a reason

This pattern follows React's unidirectional data flow, where child components notify parents of actions but don't modify state directly.

### Visual Design

The component uses Tailwind CSS classes for styling:
- Card and container elements use `rounded-lg`, `shadow-sm`, and `border` for consistent styling
- Text uses a hierarchy with `text-xs`/`text-sm` sizes and `font-medium`/`font-semibold` weights
- Colors follow a consistent palette with `indigo-600` for icons, `green-500` for approve, and `red-500` for reject
- Spacing is consistent with `space-x-3`, `py-2`, etc.
- Interactive elements have hover effects (`hover:scale-105`) for better user feedback

## Integration Points

The `PendingRequests` component is designed to integrate with a parent component that:

1. Provides the array of pending requests via the `requests` prop
2. Maintains the state of rejection reasons via the `rejectionReasons` prop
3. Handles approval actions via the `onApprove` prop
4. Handles rejection text changes via the `handleReasonChange` prop
5. Processes final rejections via the `onReject` prop

This separation of concerns allows the component to focus on rendering and user interaction, while the parent component manages data and business logic.

## Notes and Observations

1. The component uses a mix of HTML `class` and JSX `className` attributes, which should be standardized to `className` for React consistency.

2. Icon SVGs are embedded directly rather than imported from an icon library. This makes the component more self-contained but could impact maintainability.

3. The design uses a two-step rejection process which is good for accountability but increases interaction complexity.

4. The component displays the "Requested Hostel" information implicitly through the context but doesn't directly show it in the UI.

5. The component's responsive design uses a single-column layout on small screens and a two-column grid on larger screens.

## Usage Example

```jsx
import React, { useState } from 'react';
import PendingRequests from './PendingRequests';

function HostelTransferAdmin() {
  const [pendingRequests, setPendingRequests] = useState([
    // Sample request data
  ]);
  
  const [rejectionReasons, setRejectionReasons] = useState({});
  
  const handleApprove = (request) => {
    // Logic to approve request
  };
  
  const handleReject = (request) => {
    // Logic to reject request using rejectionReasons[request.id]
  };
  
  const handleReasonChange = (requestId, reason) => {
    setRejectionReasons({
      ...rejectionReasons,
      [requestId]: reason
    });
  };
  
  return (
    <div>
      <h2>Pending Transfer Requests</h2>
      <PendingRequests
        requests={pendingRequests}
        onApprove={handleApprove}
        onReject={handleReject}
        rejectionReasons={rejectionReasons}
        handleReasonChange={handleReasonChange}
      />
    </div>
  );
}
```

This example shows how a parent component would provide the necessary props and handle the callbacks from the `PendingRequests` component.