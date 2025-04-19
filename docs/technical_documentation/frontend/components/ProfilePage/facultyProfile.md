
# Faculty Profile Component Documentation

## Overview

The `FacultyProfile` component is a React functional component that fetches and displays detailed information about a faculty member, including personal details, fields of interest, education, experience, courses taught, publications, research students, achievements, and conferences. It leverages **React Query** for data fetching and manages loading and error states gracefully.

## Component Location

**File Name**: `FacultyProfile.js` (or `.jsx`)

## Dependencies

- **React**: UI library for building the component.
- **React Query** (`@tanstack/react-query`): For data fetching, caching, and synchronization.
- **newRequest**: Custom HTTP request utility (e.g., Axios instance) imported from `../../utils/newRequest`.
- **CSS Module**: `ProfilePage.module.css` for scoped styling via CSS Modules.

## Data Fetching

1. **Current User**: Reads the current user object from `localStorage` under the key `currentUser` and extracts `userId`.
2. **Faculty Details**: Uses `useQuery` with `queryKey: [\`\${userId}\`]` to fetch `/faculty/{userId}` endpoint.  
3. **Courses Taught**: Uses a second `useQuery` with `queryKey: ['courses']` to fetch `/faculty/{userId}/courses` endpoint.

Both queries expose `isLoading`, `error`, and `data` states which the component uses to conditionally render loading spinners or error messages.

## Data Mapping

The fetched data is mapped into a `faculty` object:
- `name`, `photo`, `designation`, `email`, `department`, `yearOfJoining`
- `fieldsOfInterests`, `education`, `courses`, `experience`, `publications`
- `researchStudents`, `achievements`, `conferences`

A placeholder photo (`/student.jpg`) is used if `profilePhoto` is missing.

## Inline Styling

An inline style object `inlineHeaderStyle` provides customized styling for section headers if needed:
```js
const inlineHeaderStyle = {
  color: "#007bff",
  marginBottom: "8px",
  fontSize: "18px",
  fontWeight: "600",
};
```

## JSX Structure

- **Root Fragment**: Wraps conditional rendering of loading, error, and main content.
- **Loading & Error**:
  ```jsx
  {isLoading ? <p>Loading...</p> 
    : error ? <p>Error: {error.message}</p> 
    : ( /* content below */ )}
  ```

- **Profile Container** (`styles.profileContainer`):
  - **Profile Header** (`styles.profileHeader`):
    - `<img>`: Faculty photo
    - `<div>`: Profile info—name, designation, department, year of joining, and email.

- **Dynamic Sections** (rendered if corresponding data exists):
  - **Fields of Interest**: Plain text.
  - **Education**: Unordered list of qualifications.
  - **Experience**: Unordered list of work/expertise entries.
  - **Courses Taught** (`styles.courseSection`): Table with columns:
    - Course Code, Name, Department, Credits, Year, Session, Students enrolled, Average attendance.
  - **Publications**: List of title, journal, and year.
  - **Research Students**: List of names.
  - **Achievements**: List of achievements.
  - **Conferences**: List of conference name, year, and role.

Each section uses CSS module classes for consistent styling.

## Usage Example

```jsx
import FacultyProfile from './FacultyProfile';

function Dashboard() {
  return (
    <div>
      <FacultyProfile />
    </div>
  );
}
```

## Notes & Potential Improvements

- **Error Handling**: The courses query error displays the faculty error message. Consider using `errorCourses` instead of `error` for clarity.
- **Placeholder Images**: Ensure `/student.jpg` exists in the `public/` directory.
- **Query Keys**: Use more descriptive query keys (e.g., `['faculty', userId]` and `['facultyCourses', userId]`) to avoid cache collisions.
- **Prop Validation**: If converting to TypeScript, define types for fetched data for stronger type safety.
- **Accessibility**: Add `alt` text descriptions or ARIA labels if necessary.

---

