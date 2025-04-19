# AddOrUpdate

## Overview

The `AddOrUpdate` component is a React interface that provides a toggle mechanism between two attendance management functionalities: adding new attendance records and updating existing ones. This component serves as a container that conditionally renders either the `AddAttendance` or `UpdateAttendance` component based on user selection.

## Component Props

| Prop | Type | Description |
|------|------|-------------|
| `selectedStudent` | String | The roll number of the student whose attendance is being managed. This prop is passed down to child components. |

## State Management

The component uses React's `useState` hook to manage a single state variable:

- `AddOrUpdate`: String that tracks the currently selected functionality ("Add" or "Update"). Defaults to "Add".

## Imports

```jsx
import AddAttendance from "./AddAttendance";
import UpdateAttendance from "./UpdateAttendance";
import { useState } from 'react';
import React, { useRef } from 'react';
```

- `AddAttendance`: Component for adding new attendance records
- `UpdateAttendance`: Component for updating existing attendance records
- `useState`: React hook for state management
- `useRef`: React hook imported but not used in the component

## Functionality

### Toggle Mechanism

The component implements a radio button group to toggle between "Add Attendance" and "Update Attendance" modes. Each mode corresponds to a different component being rendered.

### Radio Button Handler

```jsx
const handleRadioChange = (event) => {
    SetAddOrUpdate(event.target.value);
};
```

This function updates the `AddOrUpdate` state when a radio button selection changes, setting it to either "Add" or "Update" based on the selected radio button's value.

### Conditional Rendering

Based on the current value of `AddOrUpdate`, the component renders either:
- The `AddAttendance` component when `AddOrUpdate` is "Add"
- The `UpdateAttendance` component when `AddOrUpdate` is "Update"

Both child components receive the `selectedStudent` prop passed from the parent.

## UI Structure

The component renders:

1. A radio button group styled with Bootstrap classes:
   - "Add Attendance" option
   - "Update Attendance" option
2. A container div with the class `addupdateform` that displays:
   - `AddAttendance` component when "Add" is selected
   - `UpdateAttendance` component when "Update" is selected

## Code Breakdown

### Component Definition

```jsx
function AddOrUpdate({ selectedStudent }){
    // Component implementation
}
```

The component accepts a `selectedStudent` prop which is passed down to child components.

### State Setup

```jsx
const [AddOrUpdate, SetAddOrUpdate] = useState("Add");
```

Initializes the state with "Add" as the default selection.

### Event Handler

```jsx
const handleRadioChange = (event) => {
    SetAddOrUpdate(event.target.value);
};
```

Updates the state based on radio button selection.

### Render Method

The component's JSX structure:

```jsx
return(
    <div className="AddOrUpdate">
        <div className="btn-group" role="group" aria-label="Basic radio toggle button group">
            {/* Radio buttons for Add/Update selection */}
        </div>
        <div className="addupdateform">
            {(AddOrUpdate==="Add") && <AddAttendance selectedStudent={selectedStudent}/>}
            {(AddOrUpdate==="Update") && <UpdateAttendance selectedStudent={selectedStudent}/>}
        </div>
    </div>
);
```

Uses Bootstrap's button group styling for the radio toggles and conditional rendering for the appropriate form component.

### Radio Button Implementation

```jsx
<input type="radio" className="btn-check" name="btnradio" id="btnradio1" value="Add" 
       autoComplete="off" onChange={handleRadioChange} checked={AddOrUpdate==="Add"}/>
<label className="btn btn-outline-primary" htmlFor="btnradio1">
    <strong>Add Attendance</strong>
</label>
```

Each radio button:
- Has a unique ID and shared name for grouping
- Is associated with a styled label
- Has a value that corresponds to a component name
- Includes an onChange handler
- Has its checked state controlled by the component's state

## Usage Notes

1. This component should be used within a context where `selectedStudent` is available
2. The component relies on Bootstrap classes for styling the toggle buttons
3. Child components (`AddAttendance` and `UpdateAttendance`) must be properly implemented to accept the `selectedStudent` prop
4. The unused `useRef` import could be removed for cleaner code
5. Radio button styling uses Bootstrap's `btn-check` pattern for toggle button groups

## Related Components

- `AddAttendance`: Component for adding new attendance records
- `UpdateAttendance`: Component for updating existing attendance records