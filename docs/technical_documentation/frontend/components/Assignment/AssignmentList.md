# AssignmentList Component

## Overview

The `AssignmentList` component is a React-based front-end module designed to display a list of assignments for a specific course at IIT Guwahati. It supports role-based functionality, allowing faculty to create, edit, and delete assignments, while students can view assignments. The component fetches course and assignment data using the **Fetch API**, uses **React Router** for navigation, **React Context** for role-based logic, and **Tailwind CSS** for styling, providing a responsive and user-friendly interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For URL parameters (`useParams`), navigation (`useNavigate`, `Link`), and route replacement (`replace`, unused).
- **Axios**: Imported but unused (potential leftover from previous implementation).
- **React Context**: For accessing user role via `RoleContext`.
- **React Icons (react-icons/fa)**: For rendering icons (e.g., clipboard, calendar, edit, trash).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `AssignmentList` component is organized into the following sections:

1. **Header**: Displays the course name and a title ("Assignments").
2. **Create Assignment Button**: Visible to faculty for creating new assignments.
3. **Assignment List**: A list of assignment cards with details and role-specific actions.

## Code Explanation

### Imports

```jsx
import { useParams, Link, useNavigate, replace } from "react-router-dom";
import axios from 'axios';
import { useContext, useEffect, useState } from "react";
import { FaClipboardList, FaCalendarAlt, FaEdit, FaTrash, FaPlus, FaEye } from "react-icons/fa";
import { RoleContext } from "../../context/Rolecontext";
```

- **React Router**:
  - `useParams`: Extracts `courseId` from the URL.
  - `Link`: Creates links for navigation (e.g., create/edit assignment).
  - `useNavigate`: Enables programmatic navigation.
  - `replace`: Imported but unused.
- **Axios**: Imported but not used (likely a leftover).
- **React**:
  - `useContext`: Accesses `RoleContext` for the user’s role.
  - `useEffect`: Fetches course and assignment data.
  - `useState`: Manages state for assignments and course data.
- **React Icons**: Icons for visual feedback (clipboard, calendar, edit, trash, plus, eye).
- **RoleContext**: Provides the user’s role (e.g., `"faculty"`, `"student"`).

### State Management

```jsx
const { courseId } = useParams();
const { role } = useContext(RoleContext);
const navigate = useNavigate();
const [assignments, setAssignments] = useState([]);
const [course, setCourse] = useState(null);
```

- `courseId`: URL parameter for the course.
- `role`: User role from `RoleContext`.
- `navigate`: Used for redirecting to assignment details or submissions.
- `assignments`: Stores the list of fetched assignments.
- `course`: Stores course details (e.g., `courseName`).

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const userId = currentUser?.data?.user?.userId;
```

- Retrieves `currentUser` from `localStorage` and extracts `userId`.
- Assumes `currentUser` has a nested `data.user` object with `userId`.

### Data Fetching with useEffect

#### Fetch Assignments

```jsx
useEffect(() => {
  const fetchAssignments = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/assignment/course/${courseId}/assignments`);
      const data = await res.json();
      if (res.ok) {
        setAssignments(data.assignments || []);
      } else {
        alert("Failed to fetch assignments.");
      }
    } catch (err) {
      console.error("Error fetching assignments:", err);
      alert("Error fetching assignments.");
    }
  };
  fetchAssignments();
}, [courseId]);
```

- Fetches assignments from `/api/assignment/course/${courseId}/assignments`.
- Updates `assignments` state with the response data (defaults to empty array if undefined).
- Shows an alert on failure.
- Runs when `courseId` changes.

#### Fetch Course Details

```jsx
useEffect(() => {
  const fetchCourse = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/assignment/course/${courseId}`);
      const data = await res.json();
      if (res.ok) {
        setCourse(data.data);
      } else {
        setCourse(null);
      }
    } catch (err) {
      console.error("Error fetching course:", err);
    }
  };
  fetchCourse();
}, [courseId]);
```

- Fetches course details from `/api/assignment/course/${courseId}`.
- Updates `course` state with the response data or sets to `null` on failure.
- Runs when `courseId` changes.

### Handlers

#### Delete Assignment

```jsx
const handleDelete = async (assignmentId) => {
  const confirmDelete = window.confirm("Are you sure you want to delete this assignment?");
  if (!confirmDelete) return;
  try {
    console.log("Deleting assignment...", { courseId, assignmentId });
    const res = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}`, {
      method: "DELETE",
    });
    console.log("Response from server:", res);
    const data = await res.json();
    if (res.ok) {
      alert("Assignment deleted successfully!");
      window.location.href = `/course/${courseId}/assignments`;
    } else {
      alert(data.message || "Failed to delete assignment.");
    }
  } catch (err) {
    console.error("Error deleting assignment:", err);
    alert("Server error. Please try again.");
  }
};
```

- Prompts for confirmation before deleting.
- Sends a DELETE request to `/api/assignment/${courseId}/${assignmentId}`.
- On success, alerts and reloads the page using `window.location.href` (commented `navigate` suggests an alternative).
- Alerts with an error message on failure.

#### View Assignment

```jsx
const handleViewAssignment = (assignmentId) => {
  if (role === "faculty") {
    navigate(`/course/${courseId}/assignment/${assignmentId}/submissions`);
  } else {
    navigate(`/course/${courseId}/assignment/${assignmentId}`);
  }
};
```

- Navigates based on role:
  - Faculty: To `/course/${courseId}/assignment/${assignmentId}/submissions` (view submissions).
  - Student: To `/course/${courseId}/assignment/${assignmentId}` (view assignment details).

### Rendering

#### Course Not Found

```jsx
if (!course) {
  return (
    <div className="p-6 text-center">
      <h2 className="text-2xl font-bold text-red-500">❌ Course Not Found</h2>
      <Link
        to="/assignmentlanding"
        className="mt-4 inline-block bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-300"
      >
        🔙 Back to Courses
      </Link>
    </div>
  );
}
```

- Displays an error message and a link to `/assignmentlanding` if `course` is null.

#### Main UI

```jsx
return (
  <div className="p-6">
    <h2 className="text-3xl font-bold mb-6 text-gray-800">{course.courseName} - Assignments</h2>
    {role === "faculty" && (
      <div className="mb-6">
        <Link
          to={`/course/${courseId}/create-assignment`}
          className="inline-block bg-green-500 text-white py-2 px-4 rounded-md font-medium hover:bg-green-600 transition duration-300"
        >
          <FaPlus className="inline-block mr-2" /> Create Assignment
        </Link>
      </div>
    )}
    <div className="space-y-4">
      {assignments.length > 0 ? (
        assignments.map((assignment) => (
          <div
            key={assignment._id}
            className="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition duration-300"
          >
            <div className="flex items-center gap-3 mb-2">
              <FaClipboardList className="text-blue-500 text-2xl" />
              <h3 className="text-xl font-semibold text-gray-900">{assignment.title}</h3>
            </div>
            <p className="text-gray-700 mb-2">
              <strong>Description:</strong>{" "}
              {assignment.description?.length > 100
                ? assignment.description.substring(0, 100) + "..."
                : assignment.description}
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Due Date:</strong> 📅{" "}
              {assignment.dueDate ? new Date(assignment.dueDate).toLocaleString() : "N/A"}
            </p>
            <p className="text-gray-700 mb-4">
              <strong>Submissions:</strong>{" "}
              {Array.isArray(assignment.submissions) ? assignment.submissions.length : 0}
            </p>
            <button
              onClick={() => handleViewAssignment(assignment.assignmentNumber)}
              className="w-full text-center bg-blue-500 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-600 transition duration-300"
            >
              <FaEye className="inline-block mr-2" /> View Assignment
            </button>
            {role === "faculty" && (
              <div className="flex gap-4 mt-3">
                <Link
                  to={`/course/${courseId}/assignment/${assignment.assignmentNumber}/edit`}
                  className="flex-1 text-center bg-yellow-500 text-white py-2 px-4 rounded-md font-medium hover:bg-yellow-600 transition duration-300"
                >
                  <FaEdit className="inline-block mr-2" /> Edit
                </Link>
                <button
                  onClick={() => handleDelete(assignment.assignmentNumber)}
                  className="flex-1 text-center bg-red-500 text-white py-2 px-4 rounded-md font-medium hover:bg-red-600 transition duration-300"
                >
                  <FaTrash className="inline-block mr-2" /> Delete
                </button>
              </div>
            )}
          </div>
        ))
      ) : (
        <p className="text-gray-600 text-center">📭 No assignments available for this course.</p>
      )}
    </div>
  </div>
);
```

- **Header**: Shows the course name and "Assignments" title.
- **Create Button**: Faculty-only link to `/course/${courseId}/create-assignment`.
- **Assignment List**:
  - If no assignments, displays a placeholder message.
  - Each assignment card includes:
    - Title with a clipboard icon.
    - Truncated description (first 100 characters).
    - Due date (formatted or "N/A").
    - Number of submissions.
    - "View Assignment" button (role-based navigation).
    - Faculty-only: "Edit" link and "Delete" button.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Padded (`p-6`).
  - **Header**: Large, bold, gray text (`text-3xl`, `font-bold`, `text-gray-800`).
  - **Cards**:
    - White background (`bg-white`), padding (`p-6`), rounded (`rounded-lg`), shadow (`shadow-md`), border (`border-gray-200`).
    - Hover effect (`hover:shadow-lg`, `transition duration-300`).
    - Title: Bold and large (`text-xl`, `font-semibold`).
    - Text: Gray for details (`text-gray-700`), with bold labels.
  - **Buttons**:
    - Create: Green (`bg-green-500`, `hover:bg-green-600`).
    - View: Blue (`bg-blue-500`, `hover:bg-blue-600`).
    - Edit: Yellow (`bg-yellow-500`, `hover:bg-yellow-600`).
    - Delete: Red (`bg-red-500`, `hover:bg-red-600`).
    - All buttons are rounded (`rounded-md`), padded (`py-2 px-4`), with transitions.
  - **Icons**: Blue for clipboard (`text-blue-500`), inline for buttons (`inline-block mr-2`).
  - **Empty State**: Centered, gray text (`text-gray-600`, `text-center`).

## Assumptions

- **API Endpoints**:
  - `GET /api/assignment/course/${courseId}/assignments`: Returns an array of assignments with `_id`, `assignmentNumber`, `title`, `description`, `dueDate`, and `submissions`.
  - `GET /api/assignment/course/${courseId}`: Returns course details with `courseName`.
  - `DELETE /api/assignment/${courseId}/${assignmentId}`: Deletes an assignment.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId`.
- **RoleContext**: Provides a valid `role` (`"faculty"` or `"student"`).
- **Routing**:
  - Routes exist for `/course/:courseId/assignments`, `/course/:courseId/create-assignment`, `/course/:courseId/assignment/:assignmentId`, `/course/:courseId/assignment/:assignmentId/submissions`, and `/course/:courseId/assignment/:assignmentId/edit`.
- **Assignment Data**:
  - Includes `assignmentNumber` for navigation and deletion, distinct from `_id`.
  - `submissions` is an array (or undefined).

## Notes

- **Unused Imports**:
  - `axios` and `replace` are imported but unused, suggesting potential refactoring or prior implementation attempts.
- **Navigation**:
  - `handleDelete` uses `window.location.href` instead of `navigate`, causing a full page reload (commented `navigate` suggests an alternative).
- **Error Handling**:
  - Uses `alert` and `window.confirm`, which are not ideal for UX.
  - Lacks loading states for fetching assignments or course data.
- **Debugging**:
  - Console logs are present (e.g., for assignments, deletion), which should be removed in production.
- **Assignment Identifier**:
  - Uses `assignmentNumber` for navigation/deletion but `_id` for the key, indicating a possible distinction in the backend.
- **Security**:
  - Assumes backend validation for assignment deletion and role-based access.

## Future Improvements
- **Error Handling**:
  - Replace `alert` and `window.confirm` with a toast library (e.g., `react-hot-toast`) and custom modal
- **Remove Unused Imports**:
  - Remove `axios` and `replace` to clean up the code.
- **Dynamic Sorting**:
  - Allow sorting assignments by due date or title.
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-label` for buttons).
  - Ensure keyboard navigation for buttons and links.
- **Testing**:
  - Write unit tests for fetching, deletion, and role-based rendering.
- **Remove Debugging**:
  - Eliminate console logs in production.
- **Consistent IDs**:
  - Clarify the use of `_id` vs. `assignmentNumber` to avoid confusion.
- **Empty State Enhancement**:
  - Add a call-to-action for faculty to create an assignment:
