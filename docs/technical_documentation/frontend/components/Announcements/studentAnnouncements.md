# studentAnnouncements Component

## Overview

The `CourseAnnouncements` component is a React-based front-end module designed to display course announcements for students in our academic institution. It fetches announcements for a specific course using the course ID from the URL, displays course details, and renders a list of announcements with their importance, date, and optional attachments. The component uses **Tanstack Query** for data fetching, **React Router** for navigation, and **Tailwind CSS** for styling, providing a clean and responsive user interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`), navigation (`useNavigate`), and linking (`Link`).
- **Tanstack Query (@tanstack/react-query)**: For data fetching (`useQuery`).
- **newRequest**: A custom utility for HTTP requests (assumed to be an Axios wrapper).
- **React Icons (react-icons/fa)**: For rendering icons (e.g., arrow, bullhorn, calendar).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `CourseAnnouncements` component is organized into the following sections:

1. **Header**: Displays the course name with a back button to the courses list.
2. **Course Info**: Shows course details (code, department, credits).
3. **Announcements List**: Renders all announcements for the course, including importance badges, meta information, and attachments.

## Code Explanation

### Imports

```jsx
import { useParams, Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { FaArrowLeft, FaBullhorn, ... } from "react-icons/fa";
import { useQuery } from '@tanstack/react-query';
import newRequest from "../../utils/newRequest";
```

- **React Router**:
  - `useParams`: Extracts `courseId` from the URL.
  - `Link`: Creates a link back to the courses page.
  - `useNavigate`: Provides programmatic navigation (not used in the current implementation).
- **React**:
  - `useState`: Manages course data state.
  - `useEffect`: Imported but unused (potential for future enhancements).
- **React Icons**: Icons for visual enhancement (e.g., back arrow, bullhorn, paperclip).
- **Tanstack Query**:
  - `useQuery`: Fetches course data and announcements.
- **newRequest**: Utility for API requests (likely Axios-based).

### State Management

```jsx
const { courseId } = useParams();
const navigate = useNavigate();
const [course, setCourse] = useState(null);
```

- `courseId`: Extracted from the URL parameters.
- `navigate`: Declared but unused (could be used for redirects).
- `course`: Stores fetched course data, including announcements.

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const userId = currentUser?.data?.user?.userId;
```

- Retrieves user data from `localStorage` and extracts `userId`.
- Assumes `currentUser` is stored as a JSON string with a nested `data.user` object containing `userId`.

### Data Fetching with Tanstack Query

```jsx
const { 
  isLoading, 
  error, 
  data 
} = useQuery({
  queryKey: ["courseAnnouncements", courseId],
  queryFn: () => 
    newRequest.get(`/student/courses/${courseId}`).then((res) => {
      console.log("Course data received:", res.data);
      setCourse(res.data);
      return res.data;
    }),
  enabled: !!courseId
});
```

- Fetches course data and announcements for the given `courseId`.
- `queryKey`: Unique key (`["courseAnnouncements", courseId]`) for caching.
- `queryFn`: Makes a GET request to `/student/courses/${courseId}`, logs the response, updates `course` state, and returns the data.
- `enabled`: Only runs if `courseId` exists.

### Utility Functions

#### Format Date

```jsx
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};
```

- Formats a date string (e.g., "2023-10-15") to a readable format (e.g., "October 15, 2023").

#### Importance Styling

```jsx
const getImportanceClass = (importance) => {
  switch (importance) {
    case 'Critical': return 'bg-red-500';
    case 'High': return 'bg-orange-500';
    case 'Medium': return 'bg-blue-500';
    case 'Low': return 'bg-green-500';
    default: return 'bg-blue-500';
  }
};

const getImportanceLabel = (importance) => {
  switch (importance) {
    case 'Critical': return 'Critical Announcement';
    case 'High': return 'Important Announcement';
    case 'Medium': return 'Announcement';
    case 'Low': return 'Information';
    default: return 'Announcement';
  }
};
```

- `getImportanceClass`: Returns a Tailwind background color class based on importance (e.g., `bg-red-500` for Critical).
- `getImportanceLabel`: Returns a user-friendly label for the importance level (e.g., "Critical Announcement").

### Rendering

#### Loading State

```jsx
if (isLoading) {
  return (
    <div className="p-6 flex justify-center items-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading announcements...</p>
      </div>
    </div>
  );
}
```

- Displays a spinner and message while fetching course data.

#### Error State

```jsx
if (error) {
  return (
    <div className="p-6 flex justify-center items-center min-h-screen">
      <div className="text-center bg-white p-8 rounded-lg shadow-lg border border-red-200 max-w-md">
        <FaExclamationTriangle className="text-5xl text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-3">Course Not Found</h2>
        <p className="text-gray-600 mb-6">
          {error.response?.data?.message || "The course you're looking for doesn't exist or you don't have access to it."}
        </p>
        <Link to="/courses" className="...">Return to My Courses</Link>
      </div>
    </div>
  );
}
```

- Shows an error message with a link back to the courses page if the fetch fails.
- Displays a server-provided message or a generic fallback.

#### Main UI

```jsx
return (
  <div className="p-6 max-w-4xl mx-auto">
    {/* Header */}
    <div className="flex items-center mb-6">
      <Link to="/courses" className="mr-4 text-pink-500 hover:text-pink-600">
        <FaArrowLeft className="text-xl" />
      </Link>
      <h1 className="text-3xl font-bold text-gray-800">{course?.courseName} Announcements</h1>
    </div>

    {/* Course Info */}
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p className="text-sm text-gray-500">Course Code</p>
          <p className="font-medium">{course?.courseCode}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Department</p>
          <p className="font-medium">{course?.department}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Credits</p>
          <p className="font-medium">{course?.credits}</p>
        </div>
      </div>
    </div>

    {/* Announcements List */}
    {!course?.announcements || course.announcements.length === 0 ? (
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <FaBullhorn className="text-5xl text-gray-400 mx-auto mb-4" />
        <p className="text-gray-700">No announcements yet for this course.</p>
      </div>
    ) : (
      <div className="space-y-6">
        {course.announcements.map((announcement) => (
          <div key={announcement.id} className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
            <div className={`${getImportanceClass(announcement.importance)} text-white text-xs font-semibold py-1 px-3`}>
              {getImportanceLabel(announcement.importance)}
            </div>
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">{announcement.title}</h2>
              <div className="flex flex-wrap items-center text-sm text-gray-600 mb-4">
                <div className="flex items-center mr-4 mb-2">
                  <FaUserCircle className="mr-1" />
                  <span>{announcement.postedBy}</span>
                </div>
                <div className="flex items-center mr-4 mb-2">
                  <FaCalendarAlt className="mr-1" />
                  <span>{formatDate(announcement.date)}</span>
                </div>
                <div className="flex items-center mb-2">
                  <FaTag className="mr-1" />
                  <span>{announcement.importance}</span>
                </div>
              </div>
              <div className="text-gray-700 mb-4">
                <p>{announcement.content}</p>
              </div>
              {announcement.attachments && announcement.attachments.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h3 className="text-sm font-medium flex items-center text-gray-700 mb-2">
                    <FaPaperclip className="mr-1" />
                    Attachments
                  </h3>
                  <ul className="space-y-2">
                    {announcement.attachments.map((attachment, index) => (
                      <li key={index}>
                        <a href={attachment.url} className="text-blue-500 hover:underline flex items-center" target="_blank" rel="noopener noreferrer">
                          <span className="mr-1">📎</span>
                          {attachment.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);
```

- **Header**: Includes a back button and course name.
- **Course Info**: Displays course details in a responsive grid (1 column on mobile, 3 on medium screens).
- **Announcements List**:
  - Shows a placeholder if no announcements exist.
  - Renders each announcement with an importance badge, title, meta information (posted by, date, importance), content, and optional attachments.

## Styling

- **Tailwind CSS**: Used for responsive, modern styling.
  - Containers: `p-6`, `max-w-4xl`, `mx-auto`, `rounded-lg`, `shadow-md`.
  - Buttons/Links: Pink theme (`bg-pink-500`, `hover:bg-pink-600`), transitions.
  - Cards: White background (`bg-white`), shadows, borders (`border-gray-200`).
  - Badges: Color-coded importance (`bg-red-500`, `bg-blue-500`).
  - Text: Consistent typography (`text-gray-700`, `font-semibold`).
- **Responsive Design**: Uses Tailwind’s responsive classes (e.g., `md:grid-cols-3`).

## Assumptions

- **newRequest**: A pre-configured Axios instance for API requests.
- **API Endpoint**:
  - `GET /student/courses/${courseId}`: Returns course details and announcements.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId`.
- **Course Data**: Includes `courseName`, `courseCode`, `department`, `credits`, and an `announcements` array with fields like `id`, `title`, `content`, `postedBy`, `date`, `importance`, and optional `attachments`.

## Notes

- **Navigation**: `useNavigate` is imported but unused; could be used for redirects on unauthorized access.
- **Debugging**: Console logs are included for `userId`, `courseId`, and course data (should be removed in production).
- **Attachments**: Supports rendering attachments with name and URL, assuming they are provided in the API response.
- **Error Handling**: Displays server-provided error messages or a generic fallback.
- **Security**: Assumes `userId` and course access are validated server-side.

## Future Improvements

- **Error Notifications**: Add a toast library (e.g., `react-hot-toast`) for user-friendly error messages.
- **Empty State Action**: Include a message encouraging students to check back later for announcements.
- **Navigation**: Use `navigate` to redirect on unauthorized access or invalid course IDs.
- **Accessibility**: Add ARIA attributes and keyboard navigation for links and attachments.
- **Testing**: Write unit tests for data fetching, rendering, and importance styling.
- **Performance**: Consider memoizing `formatDate` or computed styles with `useMemo` for large announcement lists.
- **Dynamic Sorting**: Allow sorting announcements by date or importance.
- **Remove Debugging**: Eliminate console logs in production code.