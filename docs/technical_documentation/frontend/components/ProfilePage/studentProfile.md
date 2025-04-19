# Student Profile Component Documentation

## Overview

The `StudentProfile` component is a React functional component that fetches and displays comprehensive details of a student, including personal information and completed courses. It handles loading and error states using React Query.

## File Location

**File Name**: `StudentProfile.js` (or `.jsx`)

## Dependencies

- **React**
- **React Query** (`@tanstack/react-query`): For data fetching and state management.
- **newRequest**: Custom HTTP client imported from `../../utils/newRequest`.
- **CSS Module**: `ProfilePage.module.css` for scoped styling.

## Data Fetching

1. Retrieves the current user from `localStorage` (`currentUser`) to extract `userId` and `email`.
2. Uses `useQuery` to fetch student details from `/student/{userId}`.
3. Uses a second `useQuery` to fetch completed courses from `/student/{userId}/completed-courses`.

Loading and error states (`isLoading`, `error`, `isLoadingCourses`, `errorCourses`) are used to conditionally render content.

## Data Mapping

Maps API response into a `student` object:

- `rollNumber`, `name`, `photo`, `signphoto`, `hostel`, `email`
- `Bloodgr`, `contactno`, `dob`, `roomNo`, `semester`
- `branch`, `yearOfJoining`, `programme`, `courses`

Defaults:

- Placeholder images (`/student.jpg`, `/sign.jpg`) if none provided.
- `batch.substr(0, 4)` to extract joining year.

## JSX Structure

- **Root Fragment** with conditional rendering:
  - Loading and error messages for student data and courses.
- **Profile Container** (`styles.profileContainer`):
  - `<img>` tags for profile photo and signature.
  - **Profile Header** (`styles.profileHeader`):
    - Empty `<div/>` for layout, then profile info (`styles.profileInfo`) listing personal details.
- **Courses Section** (`styles.courseSection`):
  - Table of completed courses with columns: Course Code, Name, Department, Credit/Audit, Semester, Credits, Grade.

## Usage Example

```jsx
import StudentProfile from './StudentProfile';

function App() {
  return <StudentProfile />;
}
```

## Notes & Improvements

- **Console Logs**: Remove `console.log` statements in production.
- **Query Keys**: Use descriptive keys like `['student', userId]` and `['completedCourses', userId]`.
- **Error Handling**: Show distinct error messages for courses (`errorCourses`) instead of repeating `error`.
- **Type Safety**: Convert to TypeScript and define interfaces for API responses.
- **Accessibility**: Add `alt` text for images and proper table semantics.
