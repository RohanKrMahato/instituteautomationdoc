# AssignmentLanding Component

## Overview

The `AssignmentLanding` component is a React-based front-end module designed to serve as the entry point for managing assignments at IIT Guwahati. It displays a list of courses for the logged-in user, with role-based actions (faculty can create/view assignments, students can view assignments). The component uses **React Router** for navigation, **React Context** for role-based logic, **Fetch API** for retrieving course data, and **Tailwind CSS** for styling, providing a responsive and user-friendly interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For navigation (`useNavigate`).
- **React Context**: For accessing user role via `RoleContext`.
- **React Icons (react-icons/fa)**: For rendering icons (e.g., book, plus, clipboard).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `AssignmentLanding` component is organized into the following sections:

1. **Header**: Displays a role-specific title ("My Faculty Courses" or "My Courses").
2. **Course List**: A grid of course cards showing course details and role-based action buttons.

## Code Explanation

### Imports

```jsx
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "../../context/Rolecontext";
import { FaBookOpen, FaClipboardList, FaPlus } from "react-icons/fa";
```

- **React**:
  - `useContext`: Accesses `RoleContext` for the user’s role.
  - `useEffect`: Handles side effects for fetching courses.
  - `useState`: Manages state for courses and assignments.
- **React Router**:
  - `useNavigate`: Enables programmatic navigation.
- **RoleContext**: Provides the user’s role (e.g., `"faculty"`, `"student"`).
- **React Icons**: Icons for visual enhancement (book, clipboard, plus).

### State Management

```jsx
const { role } = useContext(RoleContext);
const [assignments, setAssignments] = useState([]);
const [courses, setCourses] = useState([]);
const navigate = useNavigate();
```

- `role`: Extracted from `RoleContext` to determine user permissions.
- `assignments`: Unused state (likely intended for future enhancements).
- `courses`: Stores the list of fetched courses.
- `navigate`: Used for redirecting users (e.g., to login or course-specific pages).

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const userId = currentUser?.data?.user?.userId;
```

- Retrieves `currentUser` from `localStorage` and extracts `userId`.
- Assumes `currentUser` has a nested `data.user` object with `userId`.

### Data Fetching with useEffect

```jsx
useEffect(() => {
  console.log("User ID:", userId);
  console.log("Role:", role);
  if (!userId) {
    alert("Please log in first.");
    navigate("/login");
    return;
  }

  const fetchCourses = async () => {
    try { 
      const response = await fetch(`http://localhost:8000/api/assignment/${role}/${userId}/courses`);
      const data = await response.json();
      if (response.ok) {
        setCourses(data.courses);
      } else {
        alert("Failed to fetch courses");
      }
    } catch (error) {
      console.error("Error fetching courses:", error);
      alert("Failed to connect to the server.");
    }
  };

  fetchCourses();
}, [role, userId]);
```

- **Authentication Check**:
  - If `userId` is missing, alerts the user and redirects to `/login`.
- **Course Fetching**:
  - Fetches courses from `/api/assignment/${role}/${userId}/courses`.
  - Updates `courses` state with the response data if successful.
  - Shows an alert on failure or network error.
- **Dependencies**: Runs when `role` or `userId` changes.
- **Debugging**: Logs `userId` and `role` (should be removed in production).

### Rendering

```jsx
return (
  <div className="p-6">
    <h1 className="text-3xl font-bold mb-6 text-gray-800">
      {role === "faculty" ? "My Faculty Courses" : "My Courses"}
    </h1>

    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {courses.map((course) => (
        <div
          key={course.courseCode}
          className="bg-white p-6 rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition duration-300"
        >
          <div className="flex items-center gap-3 mb-4">
            <FaBookOpen className="text-blue-500 text-3xl" />
            <h2 className="text-2xl font-semibold text-gray-900">{course.courseName}</h2>
          </div>
          <p className="text-gray-600 text-sm font-medium mb-3">
            Course Code: <span className="text-gray-800">{course.courseCode}</span>
          </p>
          {role === "faculty" ? (
            <div className="space-y-3">
              <button
                onClick={() => navigate(`/course/${course.courseCode}/create-assignment`)}
                className="block text-center bg-green-500 text-white py-2 px-4 rounded-md font-medium hover:bg-green-600 transition duration-300"
              >
                <FaPlus className="inline-block mr-2" /> Create Assignment
              </button>
              <button
                onClick={() => navigate(`/course/${course.courseCode}/assignments`)}
                className="block text-center bg-blue-500 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-600 transition duration-300"
              >
                View Assignments
              </button>
            </div>
          ) : (
            <button
              onClick={() => navigate(`/course/${course.courseCode}/assignments`)}
              className="block text-center bg-blue-500 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-600 transition duration-300"
            >
              View Assignments
            </button>
          )}
        </div>
      ))}
    </div>
  </div>
);
```

- **Header**:
  - Displays "My Faculty Courses" for faculty or "My Courses" for students.
  - Uses large, bold typography (`text-3xl`, `font-bold`).
- **Course Grid**:
  - Renders courses in a responsive grid (1 column on mobile, 2 on medium, 3 on large screens).
  - Each course is a card with:
    - A book icon and course name.
    - Course code in a meta section.
    - Role-specific buttons:
      - Faculty: "Create Assignment" (green) and "View Assignments" (blue).
      - Student: "View Assignments" (blue).
- **Navigation**:
  - Faculty buttons navigate to `/course/${courseCode}/create-assignment` or `/course/${courseCode}/assignments`.
  - Student button navigates to `/course/${courseCode}/assignments`.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Padded (`p-6`) for spacing.
  - **Header**: Large, bold, gray text (`text-3xl`, `font-bold`, `text-gray-800`).
  - **Grid**: Responsive columns (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`), with gaps (`gap-6`).
  - **Cards**:
    - White background (`bg-white`), padding (`p-6`), rounded (`rounded-lg`), shadow (`shadow-lg`), border (`border-gray-200`).
    - Hover effect for shadow (`hover:shadow-xl`, `transition duration-300`).
    - Course name: Large and bold (`text-2xl`, `font-semibold`).
    - Course code: Small, gray, with a darker value (`text-sm`, `text-gray-600`, `text-gray-800`).
  - **Buttons**:
    - Full-width (`block`), centered text (`text-center`).
    - Green for create (`bg-green-500`, `hover:bg-green-600`) and blue for view (`bg-blue-500`, `hover:bg-blue-600`).
    - Rounded (`rounded-md`), padded (`py-2 px-4`), with transitions.
  - **Icons**: Blue book icon (`text-blue-500`, `text-3xl`), inline icons for buttons (`inline-block mr-2`).

## Assumptions

- **API Endpoint**:
  - `GET /api/assignment/${role}/${userId}/courses`: Returns an array of courses with `courseCode` and `courseName`.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId`.
- **RoleContext**: Provides a valid `role` (`"faculty"` or `"student"`).
- **Routing**:
  - Routes exist for `/login`, `/course/:courseCode/assignments`, and `/course/:courseCode/create-assignment`.
- **Course Data**: Each course object has at least `courseCode` and `courseName`.

## Notes

- **Unused Assignments State**:
  - The `assignments` state is declared but unused, suggesting potential plans to display assignments directly on this page.
- **Error Handling**:
  - Uses `alert` for errors, which is suboptimal for UX.
  - Lacks a loading state while fetching courses.
- **Debugging**:
  - Console logs for `userId` and `role` should be removed in production.
- **Navigation**:
  - Assumes routes are configured correctly for navigation targets.
- **Security**:
  - Relies on backend validation to ensure only authorized users access courses.

## Future Improvements

- **Loading State**:
  - Add a loading spinner while fetching courses
- **Error Handling**:
  - Replace `alert` with a toast library (e.g., `react-hot-toast`)
- **Use Assignments State**:
  - Fetch and display assignments per course if intended
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-label` for buttons).
  - Ensure keyboard navigation for buttons.
- **Testing**:
  - Write unit tests for course fetching, role-based rendering, and navigation.
- **Remove Debugging**:
  - Eliminate console logs in production.
- **Dynamic Routing**:
  - Use consistent route patterns (e.g., `/courses/:courseId/...` instead of `:courseCode`).
- **Error Boundary**:
  - Wrap the component in an error boundary for robustness.