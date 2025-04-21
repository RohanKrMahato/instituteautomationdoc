# ApprovedRequests Component 

## Overview

The `ApprovedRequests` component is designed to display a list of approved hostel transfer requests within a user interface. It handles both cases where requests exist and where no requests are available, providing appropriate visual feedback to the user.

## Component Structure

The `ApprovedRequests` component is a functional React component that:

1. Accepts a `requests` array as a prop
2. Conditionally renders content based on whether there are any requests to display
3. Maps through existing requests to display them in a formatted grid layout
4. Uses SVG icons and styled containers for visual presentation

## Technical Implementation

### Dependencies

```jsx
import React from 'react';
```

The component only requires React as a dependency.

### Props

| Prop | Type | Description |
|------|------|-------------|
| `requests` | Array | An array of request objects, each containing details about a hostel transfer request |

### Component Logic

The component first checks if the `requests` array is empty:

```jsx
if (requests.length === 0) {
  // Render "No approved requests" message
}
```

If there are requests, it maps through each one to create individual request cards:

```jsx
{requests.map(request => (
  // Render request details
))}
```

### Data Structure

Each request object in the `requests` array is expected to have the following properties:

| Property | Description |
|----------|-------------|
| `id` | Unique identifier for the request |
| `rollNo` | Student's roll number |
| `requestedHostel` | The hostel requested by the student (shown as "current Hostel" in UI) |
| `currentHostel` | The student's original hostel (shown as "Old Hostel" in UI) |


## UI Components

### Empty State

When no requests are available:
- Displays a card with "No approved requests" message
- Uses subtle styling with shadow and border
- Text is centered and gray

### Request Cards

Each request is displayed in a card with:
- Green background (`bg-green-100`) indicating approval status
- Grid layout that responds to screen size (1 column on small screens, 2 columns on larger screens)
- Four information sections, each with:
  - An icon in a circular container
  - A label in uppercase gray text
  - The value in semibold darker text

### Visual Design

- Uses Tailwind CSS for styling
- Implements a clean, information-dense layout
- Consistent spacing and alignment
- Color-coded for status indication (green for approved)
- Responsive design with grid layout

## Code Explanation

### Conditional Rendering

The component uses conditional rendering to handle the empty state:

```jsx
if (requests.length === 0) {
  return (
    <div className="card w-full bg-base-100 shadow border border-base-200 rounded-lg text-center text-gray-500 py-4">
      No approved requests.
    </div>
  );
}
```

This provides immediate feedback when no data is available.

### Data Mapping

For non-empty request arrays, the component maps each request to a UI element:

```jsx
{requests.map(request => (
  <div key={request.id} className="mb-4 shadow-sm p-4 border rounded bg-green-100">
    {/* Request details */}
  </div>
))}
```

The `key` attribute uses the request's `id` for efficient React rendering.

### Grid Layout

The component uses CSS Grid to organize information:

```jsx
<div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
  {/* Information sections */}
</div>
```

This creates a responsive layout that adapts to different screen sizes.

### Information Sections

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

This creates a visually appealing and consistent way to display each data point.

### SVG Icons

The component uses inline SVG icons for each information type:
- User icon for Application ID
- Mobile phone/ID card icon for Roll No
- House icons for hostel information

## Usage Example

```jsx
import ApprovedRequests from './ApprovedRequests';

// In a parent component:
const approvedRequestsData = [
  {
    id: 'APP123',
    rollNo: 'B12345',
    requestedHostel: 'Hostel A',
    currentHostel: 'Hostel B',
    approvalTimestamp: '2023-04-15T14:30:00Z'
  },
  // More requests...
];

// Then in render:
<ApprovedRequests requests={approvedRequestsData} />
```