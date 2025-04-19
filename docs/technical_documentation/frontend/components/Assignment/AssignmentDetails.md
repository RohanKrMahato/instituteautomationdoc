# AssignmentDetail Component

## Overview

The `AssignmentDetail` component is a React-based front-end module designed to manage student interactions with a specific course assignment at an academic institution (e.g., IIT Guwahati). It fetches assignment and student data, allows students to submit text-based assignments, displays submission status, and supports undoing submissions if before the deadline. The component uses **React Router** for URL parameters, **Fetch API** for data operations, and **Tailwind CSS** for styling, providing a responsive and user-friendly interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`).
- **React Icons (react-icons/fa)**: For rendering icons (e.g., check circle, undo, file upload).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `AssignmentDetail` component is organized into the following sections:

1. **Assignment Details**: Displays the assignment title, course code, description, and due date.
2. **Submission Status**: Shows whether the assignment has been submitted, with submission details.
3. **Submission Form**: Allows text input and file uploads (file upload not fully implemented), with submit/undo buttons.
4. **Deadline Indicator**: Informs users if the submission deadline has passed.

## Code Explanation

### Imports

```jsx
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { FaCheckCircle, FaUndo, FaFileUpload } from "react-icons/fa";
```

- **React Router**:
  - `useParams`: Extracts `courseId` and `assignmentId` from the URL.
- **React**:
  - `useState`: Manages state for assignment, submission, student, and user data.
  - `useEffect`: Handles side effects for fetching data.
- **React Icons**: Icons for visual feedback (submission, undo, file upload).

### State Management

```jsx
const { courseId, assignmentId } = useParams();
const [assignment, setAssignment] = useState(null);
const [submissionText, setSubmissionText] = useState('');
const [submitted, setSubmitted] = useState(false);
const [submissionTime, setSubmissionTime] = useState(null);
const [file, setFile] = useState(null);
const [student, setStudent] = useState(null);
const [isBeforeDeadline, setIsBeforeDeadline] = useState(true);
const [user, setUser] = useState(null);
```

- `courseId`, `assignmentId`: URL parameters for the course and assignment.
- `assignment`: Stores fetched assignment data.
- `submissionText`: Tracks the text input for the submission.
- `submitted`: Indicates if the student has submitted the assignment.
- `submissionTime`: Stores the submission timestamp.
- `file`: Intended for file uploads (not fully implemented).
- `student`: Stores student data (e.g., roll number).
- `isBeforeDeadline`: Tracks if the current time is before the assignment’s due date.
- `user`: Stores user data (e.g., name).

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const userId = currentUser?.data?.user?.userId;
```

- Retrieves `currentUser` from `localStorage` and extracts `userId`.
- Assumes `currentUser` has a nested `data.user` object with `userId`.

### Data Fetching with useEffect

#### Fetch Student Data

```jsx
useEffect(() => {
  const fetchStudentData = async () => {
    if (!userId) return;
    try {
      const response = await fetch(`http://localhost:8000/api/assignment/student/${userId}`);
      const data = await response.json();
      if (response.ok && data.student) {
        setStudent(data.student);
      } else {
        console.error("Failed to fetch student data");
      }
    } catch (error) {
      console.error("Error fetching student data:", error);
    }
  };
  fetchStudentData();
}, [userId]);
```

- Fetches student data (e.g., roll number) from `/api/assignment/student/${userId}`.
- Updates `student` state if successful.
- Runs when `userId` changes.

#### Fetch User Data

```jsx
useEffect(() => {
  const fetchUserData = async () => {
    if (!userId) return;
    try {
      const response = await fetch(`http://localhost:8000/api/assignment/${userId}`);
      const data = await response.json();
      if (response.ok && data.user) {
        setUser(data.user);
        if (data.user.role === 'student') {
          const studentResponse = await fetch(`http://localhost:8000/api/assignment/student/${userId}`);
          const studentData = await studentResponse.json();
          if (studentResponse.ok && studentData.student) {
            setStudent(studentData.student);
          } else {
            console.error("Failed to fetch student data");
          }
        }
      } else {
        console.error("Failed to fetch user data");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };
  fetchUserData();
}, [userId, student]);
```

- Fetches user data from `/api/assignment/${userId}`.
- If the user is a student, fetches additional student data.
- Updates `user` and `student` states.
- Dependency on `student` may cause redundant fetches (see Notes).

#### Fetch Assignment Data

```jsx
useEffect(() => {
  const fetchAssignment = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}`);
      const data = await response.json();
      if (response.ok && data.assignment) {
        const dueDate = new Date(data.assignment.dueDate);
        const today = new Date();
        setIsBeforeDeadline(today <= dueDate);
        const submittedAssignment = data.assignment.submissions?.find(sub => sub.studentRollNo === student?.rollNo);
        if (submittedAssignment) {
          setSubmitted(true);
          setSubmissionTime(submittedAssignment.submittedAt);
          setSubmissionText(submittedAssignment.content);
        }
        setAssignment(data.assignment);
      } else {
        console.error("Failed to fetch assignment:", data.message || "Unknown error");
        alert("Assignment not found.");
      }
    } catch (error) {
      console.error("Error fetching assignment:", error);
      alert("Failed to load assignment.");
    }
  };
  if (courseId && assignmentId) {
    fetchAssignment();
  }
}, [courseId, assignmentId, userId, student]);
```

- Fetches assignment data from `/api/assignment/${courseId}/${assignmentId}`.
- Checks if the deadline has passed and updates `isBeforeDeadline`.
- Checks for an existing submission by matching `student.rollNo`.
- Updates `assignment`, `submitted`, `submissionTime`, and `submissionText` states.
- Runs when `courseId`, `assignmentId`, `userId`, or `student` changes.

### Handlers

#### File Change (Not Fully Implemented)

```jsx
const handleFileChange = (event) => {
  setFile(event.target.files[0]);
};
```

- Stores a selected file in `file` state.
- No UI or submission logic uses this (incomplete feature).

#### Submit Assignment

```jsx
const handleSubmit = async () => {
  if (!submissionText && !file) {
    alert("Please provide a submission (text or file).");
    return;
  }
  const submissionData = {
    studentRollNo: student.rollNo,
    studentName: user.name,
    content: submissionText,
  };
  try {
    const response = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(submissionData),
    });
    if (response.ok) {
      setSubmitted(true);
      setSubmissionTime(new Date().toLocaleString());
      alert("Assignment submitted successfully!");
    } else {
      alert("Submission failed.");
    }
  } catch (error) {
    console.error("Error submitting assignment:", error);
    alert("Error submitting assignment.");
  }
};
```

- Validates that either `submissionText` or `file` is provided (file check is redundant since file isn’t sent).
- Constructs `submissionData` with student roll number, name, and text content.
- Sends a POST request to `/api/assignment/${courseId}/${assignmentId}/submit`.
- Updates `submitted` and `submissionTime` on success.

#### Undo Submission

```jsx
const handleUndo = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}/undo/${student.rollNo}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      setSubmitted(false);
      setSubmissionText('');
      setSubmissionTime(null);
      alert("Submission undone.");
    } else {
      alert("Failed to undo submission.");
    }
  } catch (error) {
    console.error("Error undoing submission:", error);
    alert("Error undoing submission.");
  }
};
```

- Sends a DELETE request to `/api/assignment/${courseId}/${assignmentId}/undo/${student.rollNo}`.
- Resets `submitted`, `submissionText`, and `submissionTime` on success.

### Rendering

```jsx
if (!assignment) return <p>Loading...</p>;

return (
  <div className="p-6 max-w-2xl mx-auto bg-white rounded-lg shadow-md border border-gray-300">
    <h2 className="text-3xl font-bold text-gray-900 mb-2">{assignment.title}</h2>
    <p className="text-gray-600 text-sm mb-4">
      <strong>Course:</strong> {assignment.courseCode}
    </p>
    <p className="text-gray-700 leading-relaxed mb-4">{assignment.description}</p>
    <p className="text-gray-600 text-sm mb-6">
      <strong>Due Date:</strong> {new Date(assignment.dueDate).toLocaleDateString('en-US', {...})}
    </p>

    {submitted && (
      <div className="p-4 mb-4 bg-green-100 border border-green-300 rounded-md">
        <p className="text-green-700 font-semibold">✅ Assignment Submitted Successfully!</p>
        <p className="text-gray-600 text-sm">📌 Submitted on: {submissionTime}</p>
        <p className="text-gray-600 text-sm">Content: {submissionText}</p>
      </div>
    )}

    {isBeforeDeadline ? (
      <div className="space-y-4">
        <label className="block text-gray-700 font-medium">
          <FaFileUpload className="inline-block mr-2" />
          Submission Text:
          <textarea
            value={submissionText}
            onChange={(e) => setSubmissionText(e.target.value)}
            className="block w-full mt-2 border border-gray-300 rounded-md p-2"
            disabled={submitted}
          />
        </label>
        <div className="flex gap-4">
          {!submitted ? (
            <button onClick={handleSubmit} className="...">Submit Assignment</button>
          ) : (
            <button onClick={handleUndo} className="...">Undo Submission</button>
          )}
        </div>
      </div>
    ) : (
      <p className="text-red-500 font-medium">⏳ Submission deadline has passed.</p>
    )}
  </div>
);
```

- **Loading State**: Displays "Loading..." if `assignment` is null.
- **Assignment Details**: Shows title, course code, description, and formatted due date.
- **Submission Status**: Displays a green box with submission details if `submitted` is true.
- **Submission Form**:
  - Conditionally rendered if `isBeforeDeadline` is true.
  - Includes a textarea for `submissionText` (disabled if submitted).
  - Shows a "Submit" button if not submitted, or an "Undo" button if submitted.
- **Deadline Passed**: Displays a red message if the deadline has passed.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Centered card (`max-w-2xl`, `mx-auto`, `bg-white`, `rounded-lg`, `shadow-md`, `border-gray-300`).
  - **Typography**:
    - Title: Large and bold (`text-3xl`, `font-bold`, `text-gray-900`).
    - Labels/Meta: Small and gray (`text-sm`, `text-gray-600`).
    - Description: Relaxed line height (`leading-relaxed`).
  - **Submission Status**: Green background (`bg-green-100`, `border-green-300`), green text (`text-green-700`).
  - **Buttons**: Green for submit (`bg-green-500`, `hover:bg-green-600`), red for undo (`bg-red-500`, `hover:bg-red-600`), with transitions.
  - **Textarea**: Full-width, bordered (`border-gray-300`), rounded (`rounded-md`).
  - **Deadline Message**: Red and bold (`text-red-500`, `font-medium`).

## Assumptions

- **API Endpoints**:
  - `GET /api/assignment/${courseId}/${assignmentId}`: Returns assignment data with `title`, `courseCode`, `description`, `dueDate`, and `submissions` array.
  - `GET /api/assignment/${userId}`: Returns user data with `name` and `role`.
  - `GET /api/assignment/student/${userId}`: Returns student data with `rollNo`.
  - `POST /api/assignment/${courseId}/${assignmentId}/submit`: Accepts a submission with `studentRollNo`, `studentName`, and `content`.
  - `DELETE /api/assignment/${courseId}/${assignmentId}/undo/${studentRollNo}`: Removes a submission.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId`.
- **Assignment Data**: Includes a `submissions` array with `studentRollNo`, `content`, and `submittedAt`.
- **Backend Validation**: Ensures only authorized students can submit/undo assignments.

## Notes

- **File Upload**: The `file` state and `handleFileChange` are present but unused in submission logic, indicating an incomplete feature.
- **Redundant User Fetch**: The `fetchUserData` effect fetches user data and redundantly fetches student data, duplicating `fetchStudentData`. This could be consolidated.
- **Dependency Issue**: Including `student` in `fetchUserData`’s dependencies may cause unnecessary refetches when `student` updates.
- **Debugging**: Console logs are scattered throughout (should be removed in production).
- **Error Handling**: Uses `alert` for errors, which is not ideal for UX.
- **No Loading State for Submissions**: Submission and undo operations lack loading indicators.

## Future Improvements

- **Loading States**:
  - Add loading indicators for submit/undo operations:
- **Remove Debugging**:
  - Eliminate console logs in production code.
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-label` for buttons, `aria-disabled` for the textarea).
  - Ensure keyboard navigation works.
- **Testing**:
  - Write unit tests for fetching, submission, undo, and deadline logic.
- **Dynamic Submission Display**:
  - Show submitted files if supported by the backend.
- **Error Boundary**:
  - Wrap the component in an error boundary to handle unexpected errors gracefully.