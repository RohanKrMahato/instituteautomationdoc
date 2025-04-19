
# FacultyCourses Component Documentation

## Overview
The `FacultyCourses` component displays the courses a faculty member is teaching during the current semester. It handles data fetching, loading, error, and empty states, and provides action links for announcements, assignments, attendance, students, feedback, and detailed views.

## File Location
**File Name**: `FacultyCourses.js` (or `.jsx`)

## Dependencies
- **React**: Core UI library.
- **React Query** (`@tanstack/react-query`): For data fetching and caching.
- **newRequest**: Custom HTTP client from `../../utils/newRequest`.
- **React Icons** (`react-icons/fa`): Icons for UI (e.g., `FaBookOpen`, `FaBullhorn`).
- **React Router** (`react-router-dom`): `Link` for navigation.

## Data Fetching
- Retrieves `userId` from `localStorage` (`currentUser` object).
- Uses `useQuery` with key `["faculty-courses"]` to fetch `/faculty/{userId}/courses`.
- Sets `isFeedbackAvailable` based on `res.data.feedbackOpen`.

## Component Structure
1. **Header**  
   - Title and subtitle explaining the view.
2. **Loading State**  
   - Spinner animation and loading message.
3. **Error / Empty States**  
   - Styled message with optional return link.
4. **Courses Grid** (`grid-cols-1 lg:grid-cols-2`)  
   - **Course Card**:
     - **Header**: Course name, code, and credits badge.
     - **Stats Row**: Students, assignments, avg. attendance.
     - **Instructor Actions**: Links for announcements, assignments, attendance, students.
     - **Feedback Link**: Conditional link if feedback is available.
     - **Detail Link**: View course details.
5. **Management Links**  
   - Links to request new course and view teaching schedule.
6. **Feedback Notice**  
   - Message when feedback is closed.

## Usage Example
```jsx
import FacultyCourses from './FacultyCourses';

function Dashboard() {
  return <FacultyCourses />;
}
```

## Notes
- **Query Key**: Consider including `userId` in the key: `['faculty-courses', userId]`.
- **Navigation**: `useNavigate` import is unused; can be removed or implemented for redirects.
- **Accessibility**: Add ARIA labels for icons and links.
- **Tailwind CSS**: Ensure project is configured.
