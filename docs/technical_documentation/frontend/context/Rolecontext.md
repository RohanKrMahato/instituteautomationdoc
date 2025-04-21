# RoleContext

## Overview

The `RoleContext` and `RoleProvider` components form a React Context API implementation designed to manage user roles within our academic institution automation system. The `RoleProvider` fetches the user's role from `localStorage` and provides it, along with a setter function, to child components via the `RoleContext`. This enables role-based rendering and functionality across the application (e.g., for students, faculty, or admins). The current implementation is partially incomplete, with commented code indicating alternative role initialization approaches.

## Dependencies

- **React**: For building the context and provider.
  - `createContext`: Creates the context object.
  - `useState`: Manages the role state.

## Component Structure

- **RoleContext**: A React context object that holds the role state and setter function.
- **RoleProvider**: A provider component that wraps the application, supplying the role data to child components.

## Code Explanation

### Imports

```jsx
import React, { createContext, useState } from 'react';
```

- **React**:
  - `createContext`: Creates `RoleContext` for sharing role data.
  - `useState`: Manages the `role` state in `RoleProvider`.

### Context Creation

```jsx
export const RoleContext = createContext();
```

- Creates a context object (`RoleContext`) to share `role` and `setRole` with components.
- Exported for use in other parts of the application (e.g., `Navbar`, `AssignmentLanding`).

### RoleProvider Component

```jsx
export function RoleProvider({ children }) {
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));
  let [role, setRole] = useState(""); // Update as needed
  role = currentUser?.role;

  return (
    <RoleContext.Provider value={{ role, setRole }}>
      {children}
    </RoleContext.Provider>
  );
}
```

- **Props**:
  - `children`: The child components that will access the context.
- **User Data**:
  - Retrieves `currentUser` from `localStorage` and parses it as JSON.
  - Assumes `currentUser` has a `role` property (e.g., `"student"`, `"faculty"`, `"acadAdmin"`, `"nonAcadAdmin"`).
- **State Management**:
  - Initializes `role` with an empty string (`""`) using `useState`.
  - Immediately overwrites `role` with `currentUser?.role` using a direct assignment, bypassing the state setter (`setRole`).
  - The `let` declaration for `[role, setRole]` allows reassignment, but this is unconventional and problematic (see Notes).
- **Context Provider**:
  - Wraps `children` with `RoleContext.Provider`, passing `role` and `setRole` as the context value.
- **Commented Code**:
  - Four commented lines suggest alternative role initializations:
    ```jsx
    // const [role, setRole] = useState("student"); // Update as needed
    // const [role, setRole] = useState("faculty"); // Update as needed
    // const [role, setRole] = useState("acadAdmin"); // Update as needed
    // const [role, setRole] = useState("nonAcadAdmin"); // Update as needed
    ```
  - Indicates possible testing or debugging with hardcoded roles.

## Issues and Notes

- **Incorrect State Usage**:
  - The line `role = currentUser?.role` directly mutates the state variable, which is not how React state works. This bypasses `setRole` and won't trigger re-renders when `role` changes.
  - Likely intended to initialize `role` based on `currentUser?.role`.
- **Potential Null `currentUser`**:
  - If `localStorage.getItem("currentUser")` is `null` or invalid JSON, `JSON.parse` will throw an error, crashing the component.
  - `currentUser?.role` uses optional chaining, but no fallback is provided if `role` is undefined.
- **Commented Code**:
  - The hardcoded role options suggest the system supports four roles: `student`, `faculty`, `acadAdmin`, and `nonAcadAdmin`.
  - Likely used for testing before implementing `localStorage`-based role fetching.
- **No Role Updates**:
  - The `setRole` function is provided but never used, and the direct assignment to `role` undermines state management.
- **No Error Handling**:
  - No try-catch for `JSON.parse` or validation for `currentUser`.
- **Context Usage**:
  - Assumes components (e.g., `Navbar`, `AssignmentLanding`) consume `RoleContext` to render role-specific UI or logic.

## Assumptions

- **Authentication**:
  - `currentUser` is stored in `localStorage` by a login process (e.g., `/api/auth/login`).
  - Contains a `role` field with values like `"student"`, `"faculty"`, `"acadAdmin"`, or `"nonAcadAdmin"`.
- **Role-Based Features**:
  - The context is used to enable role-specific functionality (e.g., students see assignments, faculty see submissions).
- **Integration**:
  - Works with components like `Navbar` (for role-based navigation), `AssignmentLanding`, `TimeTable`, or `CourseRegistration`.
- **Static Initialization**:
  - The commented code suggests roles were initially hardcoded for testing.


## Integration with Other Components

- **Navbar**:
  - Can use `RoleContext` to render role-specific links (e.g., assignments for students, submissions for faculty).
- **AssignmentLanding**:
  - Likely uses `role` to filter courses or display role-specific UI.
- **TimeTable**:
  - Could filter courses based on `role` (e.g., student-specific timetable).
- **CourseRegistration**:
  - May restrict registration to students using `role`.
- **FacultyAssignmentSubmissions**:
  - Can use `role` to ensure only faculty access submission views.


## Future Improvements

- **Fix State Management**:
  - Initialize `role` with `currentUser?.role` in `useState`.
- **Error Handling for localStorage**:
  - Add try-catch for `JSON.parse`.
- **Role Validation**:
  - Ensure `role` is one of the valid values.
- **Integration with Authentication**:
  - Sync role with login/logout.
- **Use with Other Components**:
  - Example usage in `Navbar`.
- **Testing**:
  - Write unit tests for `RoleProvider` and context consumption.