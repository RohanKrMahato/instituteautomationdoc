
# CourseWrapper Component Documentation

## Overview
The `CourseWrapper` component renders different course-related views based on the user's role. It leverages React Context and React Router for role-based routing.

## File Location
**File Name**: `CourseWrapper.js`

## Dependencies
- **React**: Core library.
- **React Router** (`react-router-dom`): For navigation (`useNavigate`).
- **RoleContext**: Custom context to access the user's role.
- **Child Components**:
  - `MyCourses` (for students)
  - `FacultyCourses` (for faculty)
  - `Unauthorized` (for other roles)

## Logic
- Retrieves `role` from `RoleContext`.
- Uses a `switch` statement:
  - `student` → renders `<MyCourses />`
  - `faculty` → renders `<FacultyCourses />`
  - Any other role → renders `<Unauthorized role={role} />`

## Usage Example
```jsx
import CourseWrapper from './CourseWrapper';

function Dashboard() {
  return <CourseWrapper />;
}
```

## Notes
- **Navigation**: `useNavigate` is imported but not currently used; may be used for future redirections.
- **Extensibility**: Add more cases to the switch for additional roles (e.g., 'admin').
- **Error Handling**: The `Unauthorized` component receives the unrecognized role as a prop.
