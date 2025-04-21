# EditAssignment Component

## Overview

The `EditAssignment` component is a React-based front-end module designed to allow faculty members at IIT Guwahati to edit an existing assignment for a specific course. It fetches assignment details, pre-populates a form with the current data, and submits updates to a backend API. The component uses **React Router** for navigation and URL parameters, **Fetch API** for data operations, and **Tailwind CSS** for styling, providing a clean and responsive user interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`) and navigation (`useNavigate`).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `EditAssignment` component consists of:

1. **Header**: A title indicating the purpose ("Edit Assignment").
2. **Form**: Input fields for title, description, and due date, pre-filled with existing assignment data, and a submit button.

## Code Explanation

### Imports

```jsx
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
```

- **React**:
  - `useState`: Manages form input states.
  - `useEffect`: Fetches assignment data on mount.
- **React Router**:
  - `useParams`: Extracts `courseId` and `assignmentId` from the URL.
  - `useNavigate`: Enables programmatic navigation after submission.

### State Management

```jsx
const { courseId, assignmentId } = useParams();
const navigate = useNavigate();
const [title, setTitle] = useState("");
const [description, setDescription] = useState("");
const [dueDate, setDueDate] = useState("");
```

- `courseId`, `assignmentId`: URL parameters identifying the course and assignment.
- `navigate`: Used to redirect to the assignment list after updating.
- `title`, `description`, `dueDate`: Form input states initialized as empty, later populated with fetched data.

### Data Fetching with useEffect

```jsx
useEffect(() => {
  const fetchAssignment = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}`);
      const data = await res.json();
      if (res.ok) {
        const { title, description, dueDate } = data.assignment;
        setTitle(title);
        setDescription(description);
        setDueDate(dueDate.slice(0, 10)); // format for <input type="date" />
      } else {
        alert(data.message || "Failed to load assignment.");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      alert("Something went wrong fetching assignment.");
    }
  };
  fetchAssignment();
}, [courseId, assignmentId]);
```

- **API Request**:
  - Fetches assignment data from `/api/assignment/${courseId}/${assignmentId}`.
- **Data Handling**:
  - On success, extracts `title`, `description`, and `dueDate`.
  - Sets `title` and `description` directly.
  - Formats `dueDate` to `YYYY-MM-DD` (e.g., "2023-10-15") for `<input type="date" />` compatibility.
- **Error Handling**:
  - Alerts with the server’s error message or a generic "Failed to load assignment" on non-OK responses.
  - Alerts "Something went wrong fetching assignment" on network errors.
- **Dependencies**:
  - Runs when `courseId` or `assignmentId` changes.

### Form Submission

```jsx
const handleSubmit = async (e) => {
  console.log("Submitting form...", { title, description, dueDate });
  e.preventDefault();
  if (!title || !description || !dueDate) {
    alert("Please fill in all fields.");
    return;
  }
  try {
    const res = await fetch(`http://localhost:8000/api/assignment/${courseId}/${assignmentId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, description, dueDate }),
    });
    console.log("Response from server:", res);
    const data = await res.json();
    if (res.ok) {
      alert("Assignment updated successfully!");
      navigate(`/course/${courseId}/assignments`);
    } else {
      alert(data.message || "Failed to update assignment.");
    }
  } catch (err) {
    console.error("Error updating assignment:", err);
    alert("Server error. Please try again.");
  }
};
```

- **Validation**:
  - Prevents submission if any field (`title`, `description`, `dueDate`) is empty.
  - Uses `alert` to notify the user of missing fields.
- **API Request**:
  - Sends a PUT request to `/api/assignment/${courseId}/${assignmentId}`.
  - Includes `title`, `description`, and `dueDate` in the request body.
- **Success Handling**:
  - Alerts "Assignment updated successfully!" and navigates to `/course/${courseId}/assignments`.
- **Error Handling**:
  - Alerts with the server’s error message or a generic "Failed to update assignment" on non-OK responses.
  - Alerts "Server error. Please try again." on network errors.
- **Debugging**:
  - Logs form data and server response (should be removed in production).

### Rendering

```jsx
return (
  <div className="max-w-xl mx-auto bg-white p-6 mt-6 rounded-lg shadow-md">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Edit Assignment</h2>
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block font-medium text-gray-700">Title</label>
        <input
          type="text"
          className="w-full mt-1 p-2 border border-gray-300 rounded-md"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>
      <div>
        <label className="block font-medium text-gray-700">Description</label>
        <textarea
          rows="4"
          className="w-full mt-1 p-2 border border-gray-300 rounded-md"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
      </div>
      <div>
        <label className="block font-medium text-gray-700">Due Date</label>
        <input
          type="date"
          className="w-full mt-1 p-2 border border-gray-300 rounded-md"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />
      </div>
      <button
        type="submit"
        className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition"
      >
        Update Assignment
      </button>
    </form>
  </div>
);
```

- **Container**:
  - A centered card (`max-w-xl`, `mx-auto`) with white background, padding, shadow, and rounded corners.
- **Header**:
  - A bold title ("Edit Assignment") in large, dark gray text.
- **Form**:
  - Contains inputs for title (text), description (textarea), and due date (date picker).
  - Inputs are full-width, bordered, and rounded, with labels.
  - Submit button is blue with a hover effect.
- **Layout**:
  - Uses `space-y-4` for vertical spacing between form fields.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Centered (`mx-auto`), constrained width (`max-w-xl`), white background (`bg-white`), padded (`p-6`), margin-top (`mt-6`), rounded (`rounded-lg`), shadow (`shadow-md`).
  - **Header**: Large, bold, dark gray text (`text-2xl`, `font-bold`, `text-gray-800`, `mb-4`).
  - **Form**:
    - Labels: Medium weight, gray (`font-medium`, `text-gray-700`, `block`).
    - Inputs: Full-width (`w-full`), padded (`p-2`), bordered (`border-gray-300`), rounded (`rounded-md`), with top margin (`mt-1`).
    - Textarea: Four rows (`rows="4"`).
    - Fields spaced vertically (`space-y-4`).
  - **Button**: Blue background (`bg-blue-500`), white text, padded (`py-2 px-4`), rounded (`rounded-md`), hover effect (`hover:bg-blue-600`), smooth transition (`transition`).

## Assumptions

- **API Endpoints**:
  - `GET /api/assignment/${courseId}/${assignmentId}`: Returns assignment data with `title`, `description`, and `dueDate`.
  - `PUT /api/assignment/${courseId}/${assignmentId}`: Updates the assignment with `title`, `description`, and `dueDate`.
- **Routing**:
  - The route `/course/:courseId/assignments` exists for redirection after updating.
- **Authorization**:
  - Backend validates that the user (faculty) is authorized to edit the assignment.
- **Due Date Format**:
  - The backend returns `dueDate` in a format like `YYYY-MM-DDTHH:mm:ss.sssZ`, which is sliced to `YYYY-MM-DD` for the date input.
  - The backend accepts `dueDate` as `YYYY-MM-DD` or converts it appropriately.
- **Assignment Data**:
  - The response includes an `assignment` object with `title`, `description`, and `dueDate`.

## Notes

- **Error Handling**:
  - Uses `alert` for validation and errors, which is not ideal for user experience.
- **Validation**:
  - Basic client-side validation checks for empty fields but lacks advanced checks (e.g., date validity).
- **No Loading State**:
  - Lacks a loading indicator for fetching or submitting, which could confuse users.
- **No Cancel Option**:
  - The form doesn’t provide a way to cancel and return to the assignment list.
- **Debugging**:
  - Console logs for form submission and server response (should be removed in production).
- **Security**:
  - Assumes backend validation for course and assignment access permissions.
- **No User Data**:
  - Unlike `CreateAssignment`, it doesn’t fetch `facultyId`, assuming the backend uses authentication headers.

## Future Improvements
- **Loading State**:
  - Add loading indicators for fetching and submission.
- **Cancel Button**:
  - Add a cancel button to return to the assignment list.
- **Advanced Validation**:
  - Validate due date to ensure it’s in the future.
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-required` for inputs, `aria-label` for the button).
  - Ensure keyboard navigation for form fields.
- **Testing**:
  - Write unit tests for fetching, form validation, submission, and navigation.
- **Remove Debugging**:
  - Eliminate console logs in production.
- **Error Boundary**:
  - Wrap the component in an error boundary to handle unexpected errors.
