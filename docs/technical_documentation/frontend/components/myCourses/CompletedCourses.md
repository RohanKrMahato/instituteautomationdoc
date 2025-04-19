
# CompletedCourses Component Documentation

## Overview
The `CompletedCourses` component is a React functional component that retrieves and displays a list of a student's completed courses in a card-based layout. It uses **React Query** for data fetching and handles loading, error, and empty states gracefully.

## File Location
**File Name**: `CompletedCourses.js` (or `.jsx`)

## Dependencies
- **React**: Core library.
- **React Query** (`@tanstack/react-query`): For fetching and caching data.
- **newRequest**: Custom HTTP client from `../../utils/newRequest`.
- **React Icons** (`react-icons/fa`): For visual icons (e.g., `FaCheckCircle`, `FaCalendarAlt`).

## Data Fetching
- Retrieves `userId` from `localStorage` (`currentUser` object).
- Uses `useQuery` with the key `["completedCourses"]` to fetch `/student/{userId}/completed-courses`.
- Returns an array of course objects or an empty list.

## Utility Functions
- `formatDate(dateString)`: Converts ISO date strings to a localized date format or returns `'N/A'` if missing.

## Component Structure
1. **Header**  
   - Title: `<h1>` with "Completed Courses".  
   - Subtitle: `<p>` with "Your academic history".
2. **Loading State**  
   - Animated spinner and message.
3. **Error State**  
   - Displays error message in a styled box.
4. **Empty State**  
   - Message when no completed courses are found.
5. **Courses Grid**  
   - Responsive grid (`grid-cols-1 lg:grid-cols-2`) of course cards.
   - **Card Layout**:
     - **Header**: Course name, code, and grade badge.
     - **Details Row**: Credits and semester with icons.
     - **Department**: Displays the department.
     - **Additional Info**: Credit/Audit status and completion date.

## Usage Example
```jsx
import CompletedCourses from './CompletedCourses';

function Dashboard() {
  return <CompletedCourses />;
}
```

## Notes & Improvements
- **Query Key**: Consider namespacing with `['student', userId, 'completedCourses']` to avoid conflicts.
- **Error Handling**: Distinguish between different error types if needed.
- **Accessibility**: Add ARIA roles and labels for better screen-reader support.
- **Styling**: Tailwind CSS classes are used—ensure Tailwind is configured in the project.
