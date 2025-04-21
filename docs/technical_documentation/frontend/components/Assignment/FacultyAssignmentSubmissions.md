# FacultyAssignmentSubmissions Component

## Overview

The `FacultyAssignmentSubmissions` component is a React-based front-end module designed to allow faculty members at our academic institution to view student submissions for a specific assignment. It fetches assignment details and submission data from a backend API and displays them in a tabular format. The component uses **React Router** for URL parameters, **Fetch API** for data retrieval, and **Tailwind CSS** for styling, providing a clean and responsive user interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `FacultyAssignmentSubmissions` component consists of:

1. **Header**: Displays the assignment title and due date.
2. **Description**: Shows the assignment description in a formatted box.
3. **Submissions Table**: Lists student submissions with name, roll number, submission time, and content.

## Code Explanation

### Imports

```jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
```

- **React**:
  - `useState`: Manages states for assignment data, loading, and errors.
  - `useEffect`: Fetches assignment data on mount.
- **React Router**:
  - `useParams`: Extracts `courseId` and `assignmentId` from the URL.

### State Management

```jsx
const { courseId, assignmentId } = useParams();
const [assignment, setAssignment] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");
```

- `courseId`, `assignmentId`: URL parameters identifying the course and assignment.
- `assignment`: Stores fetched assignment data, including submissions.
- `loading`: Tracks whether data is being fetched.
- `error`: Stores error messages for display.

### Data Fetching with useEffect

```jsx
useEffect(() => {
  const fetchAssignment = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/assignment/${courseId}/${assignmentId}`
      );
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const rawText = await response.text();
        console.error("Raw response text:", rawText);
        throw new Error("Invalid JSON response");
      }
      const data = await response.json();
      if (!data.success) {
        throw new Error(data.message || "Failed to fetch assignment");
      }
      setAssignment(data.assignment);
    } catch (err) {
      console.error("Error fetching assignment:", err);
      setError("Could not load assignment.");
    } finally {
      setLoading(false);
    }
  };
  fetchAssignment();
}, [courseId, assignmentId]);
```

- **API Request**:
  - Fetches assignment data from `/api/assignment/${courseId}/${assignmentId}`.
- **Response Validation**:
  - Checks if the response is JSON (`content-type` includes `application/json`).
  - Logs raw text and throws an error if invalid.
- **Data Handling**:
  - Checks for `data.success` to confirm the request was successful.
  - Sets `assignment` state with `data.assignment` on success.
- **Error Handling**:
  - Sets `error` state to "Could not load assignment" on failure.
  - Logs errors for debugging.
- **Cleanup**:
  - Sets `loading` to `false` in the `finally` block.
- **Dependencies**:
  - Runs when `courseId` or `assignmentId` changes.

### Rendering

#### Loading and Error States

```jsx
if (loading) return <p className="text-center py-6">Loading assignment...</p>;
if (error) return <p className="text-red-500 text-center py-6">❌ {error}</p>;
if (!assignment) return <p className="text-red-500 text-center py-6">❌ Assignment not found.</p>;
```

- **Loading**: Displays a centered "Loading assignment..." message.
- **Error**: Shows a red error message with the `error` state.
- **No Assignment**: Displays a red "Assignment not found" message if `assignment` is null.

#### Main UI

```jsx
return (
  <div className="p-6 max-w-5xl mx-auto bg-white rounded-2xl shadow-lg border border-gray-200 space-y-6">
    <div>
      <h2 className="text-3xl font-extrabold text-gray-900 mb-1">
        Submissions for: {assignment.title}
      </h2>
      <p className="text-gray-600 text-sm mb-2">
        <strong>📅 Due Date:</strong>{" "}
        {new Date(assignment.dueDate).toLocaleDateString()}
      </p>
      <div className="bg-gray-50 border border-gray-200 rounded p-4 text-gray-800 whitespace-pre-line text-sm leading-relaxed">
        {assignment.description}
      </div>
    </div>
    <div>
      <h3 className="text-xl font-semibold mb-2">📥 Student Submissions</h3>
      {console.log("Assignment data:", assignment)}
      {assignment.submissions.length === 0 ? (
        <p className="text-gray-500">No submissions yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 rounded-md">
            <thead>
              <tr className="bg-gray-100 text-sm text-gray-700">
                <th className="p-3 border border-gray-300 text-left">Student Name</th>
                <th className="p-3 border border-gray-300 text-left">Roll No</th>
                <th className="p-3 border border-gray-300 text-left">Submitted At</th>
                <th className="p-3 border border-gray-300 text-left">Answer</th>
              </tr>
            </thead>
            <tbody>
              {assignment.submissions.map((submission, idx) => {
                console.log("Submission data:", submission);
                return (
                  <tr key={idx} className="hover:bg-gray-50 text-sm">
                    <td className="p-3 border border-gray-300">{submission.studentName}</td>
                    <td className="p-3 border border-gray-300">{submission.studentRollNo}</td>
                    <td className="p-3 border border-gray-300">
                      {submission.submittedAt
                        ? new Date(submission.submittedAt).toLocaleString("en-IN", {
                            dateStyle: "medium",
                            timeStyle: "short",
                          })
                        : "N/A"}
                    </td>
                    <td className="p-3 border border-gray-300 whitespace-pre-line text-gray-700">
                      {submission.content}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  </div>
);
```

- **Container**:
  - A centered card (`max-w-5xl`, `mx-auto`) with white background, rounded corners, shadow, and border.
- **Header**:
  - Displays the assignment title in large, bold text and the due date in smaller gray text.
- **Description**:
  - Shows the assignment description in a gray box with preserved whitespace (`whitespace-pre-line`).
- **Submissions**:
  - Displays "No submissions yet" if the `submissions` array is empty.
  - Renders a responsive table (`overflow-x-auto`) with columns for:
    - Student Name
    - Roll No
    - Submitted At (formatted as medium date and short time, e.g., "15 Oct 2023, 14:30")
    - Answer (submission content with preserved whitespace).
  - Rows have a hover effect (`hover:bg-gray-50`).
- **Debugging**:
  - Logs `assignment` and `submission` data (should be removed in production).

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Centered (`mx-auto`), wide (`max-w-5xl`), white background (`bg-white`), padded (`p-6`), rounded (`rounded-2xl`), shadow (`shadow-lg`), bordered (`border-gray-200`), with vertical spacing (`space-y-6`).
  - **Header**:
    - Title: Extra bold, large, dark gray (`text-3xl`, `font-extrabold`, `text-gray-900`).
    - Due Date: Small, gray (`text-sm`, `text-gray-600`), with bold label.
  - **Description**: Light gray background (`bg-gray-50`), bordered (`border-gray-200`), padded (`p-4`), rounded, with relaxed line height (`leading-relaxed`) and preserved whitespace (`whitespace-pre-line`).
  - **Submissions**:
    - Title: Bold, medium size (`text-xl`, `font-semibold`).
    - Empty State: Gray text (`text-gray-500`).
    - Table: Full-width (`min-w-full`), bordered (`border-gray-300`), rounded (`rounded-md`).
    - Table Header: Light gray background (`bg-gray-100`), small text (`text-sm`), left-aligned, bordered.
    - Table Rows: Small text, bordered, with hover effect (`hover:bg-gray-50`).
    - Answer Column: Preserves whitespace (`whitespace-pre-line`), gray text (`text-gray-700`).

## Assumptions

- **API Endpoint**:
  - `GET /api/assignment/${courseId}/${assignmentId}`: Returns an object with `success`, `message`, and `assignment` properties.
  - `assignment` includes `title`, `description`, `dueDate`, and `submissions` array.
  - `submissions` contains objects with `studentName`, `studentRollNo`, `submittedAt`, and `content`.
- **Response Format**:
  - Expects JSON with a `success` boolean to indicate status.
  - `dueDate` and `submittedAt` are valid date strings (e.g., ISO format).
- **Authorization**:
  - Backend validates that the user (faculty) is authorized to view submissions.
- **Submissions**:
  - The `submissions` array may be empty but is always present.
- **Routing**:
  - The route `/course/:courseId/assignment/:assignmentId` is valid for faculty access.

## Notes

- **Error Handling**:
  - Robustly checks for JSON content type and `success` flag.
  - Uses a generic error message for display, which could be more specific.
- **Debugging**:
  - Console logs for raw response text, errors, and data (should be removed in production).
- **No Navigation**:
  - Lacks a back button to return to the assignment list.
- **No Interaction**:
  - Submissions are view-only; no grading or editing functionality is provided.
- **Key for Table Rows**:
  - Uses `idx` as the key, which is less reliable than a unique identifier like `studentRollNo`.

## Future Improvements

- **Better Error Handling**:
  - Display specific error messages from the server.
- **Remove Debugging**:
  - Eliminate console logs in production:
- **Interactive Features**:
  - Add grading functionality (e.g., input fields for marks).
- **Sorting and Filtering**:
  - Allow sorting submissions by name, roll number, or submission time.
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-label` for table headers).
  - Ensure table is keyboard-navigable.
- **Testing**:
  - Write unit tests for fetching, error handling, and rendering submissions.
- **Empty State Enhancement**:
  - Add a more informative message.