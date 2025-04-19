
# MyCourses Component Documentation

## Overview
The `MyCourses` component displays the courses a student is currently enrolled in for the semester. It handles data fetching with loading, error, and empty states, and provides quick access links for announcements, assignments, attendance, feedback, and course details.

## File Location
**File Name**: `MyCourses.js` (or `.jsx`)

## Dependencies
- **React**: Core UI library.
- **React Query** (`@tanstack/react-query`): For data fetching and state management.
- **newRequest**: Custom HTTP client from `../../utils/newRequest`.
- **React Icons** (`react-icons/fa`): Icons like `FaBookOpen`, `FaBullhorn`, `FaComments`.
- **React Router** (`react-router-dom`): `Link` for navigation.

## Data Fetching
- Retrieves `userId` from `localStorage` (`currentUser` object).
- Uses `useQuery` with key `["courses"]` to fetch `/student/{userId}/courses`.
- Sets `isFeedbackAvailable` based on `res.data.feedbackOpen`.

## Component Structure
1. **Header**  
   - Title `<h1>`: "My Courses"  
   - Subtitle `<p>`: "Current semester enrolled courses"
2. **Loading State**  
   - Spinner with loading message.
3. **Error State**  
   - Error message and link to course registration.
4. **Empty State**  
   - Message when no courses are enrolled and link to registration.
5. **Courses Grid** (`grid-cols-1 lg:grid-cols-2`)  
   - **Course Card**:
     - **Header**: Course name, instructor, and course ID badge.
     - **Stats Row**: Credits, assignments, attendance.
     - **Quick Access**: Links for announcements (with count), assignments, attendance, and feedback (locked or available).
     - **Detail Link**: View course details.
6. **Additional Links**  
   - Link to drop courses.
   - Link to view completed courses.
7. **Feedback Notice**  
   - Notice when feedback is closed.

## Usage Example
```jsx
import MyCourses from './MyCourses';

function Dashboard() {
  return <MyCourses />;
}
```

## Notes
- **Query Key**: Consider namespacing with `['myCourses', userId]` to avoid cache collisions.
- **Console Logs**: Remove `console.log` statements in production.
- **Accessibility**: Add ARIA labels for icons and ensure link text clarity.
- **Tailwind CSS**: Ensure Tailwind is configured in the project.
