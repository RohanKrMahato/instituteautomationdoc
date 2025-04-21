# CreateAssignment Component

## Overview

The `CreateAssignment` component is a React-based front-end module designed to allow faculty members at IIT Guwahati to create new assignments for a specific course. It provides a form to input assignment details (title, description, due date) and submits the data to a backend API. The component uses **React Router** for navigation and URL parameters, **Fetch API** for submitting data, and **Tailwind CSS** for styling, delivering a clean and responsive user interface.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`) and navigation (`useNavigate`).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `CreateAssignment` component consists of:

1. **Header**: A title indicating the purpose ("Create Assignment").
2. **Form**: Input fields for title, description, and due date, with a submit button.

## Code Explanation

### Imports

```jsx
import React from "react";
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
```

- **React**:
  - `useState`: Manages form input states.
- **React Router**:
  - `useParams`: Extracts `courseId` from the URL.
  - `useNavigate`: Enables programmatic navigation after submission.

### State Management

```jsx
const { courseId } = useParams();
const navigate = useNavigate();
const [title, setTitle] = useState("");
const [description, setDescription] = useState("");
const [dueDate, setDueDate] = useState("");
```

- `courseId`: URL parameter identifying the course.
- `navigate`: Used to redirect to the assignment list after creation.
- `title`, `description`, `dueDate`: Form input states for the assignment details.

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const facultyId = currentUser?.data?.user?.userId;
```

- Retrieves `currentUser` from `localStorage` and extracts `facultyId`.
- Assumes `currentUser` has a nested `data.user` object with `userId`.
- `facultyId` is declared but unused in the current implementation.

### Form Submission

```jsx
const handleSubmit = async (e) => {
  e.preventDefault();
  if (!title || !description || !dueDate) {
    alert("Please fill in all fields.");
    return;
  }
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));
  const facultyId = currentUser?.data?.user?.userId;
  try {
    const res = await fetch(`http://localhost:8000/api/assignment/course/${courseId}/assignments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        description,
        dueDate,
      }),
    });
    const data = await res.json();
    if (res.ok) {
      alert("Assignment created successfully!");
      navigate(`/course/${courseId}/assignments`);
    } else {
      alert(data.message || "Failed to create assignment.");
    }
  } catch (err) {
    console.error("Error creating assignment:", err);
    alert("Server error. Please try again.");
  }
};
```

- **Validation**:
  - Prevents submission if any field (`title`, `description`, `dueDate`) is empty.
  - Uses `alert` to notify the user of missing fields.
- **API Request**:
  - Sends a POST request to `/api/assignment/course/${courseId}/assignments`.
  - Includes `title`, `description`, and `dueDate` in the request body.
- **Success Handling**:
  - Alerts "Assignment created successfully!" and navigates to `/course/${courseId}/assignments`.
- **Error Handling**:
  - Alerts with the server’s error message or a generic "Failed to create assignment" on non-OK responses.
  - Alerts "Server error. Please try again." on network errors.
- **Note**: `facultyId` is fetched but not used in the request (possible oversight).

### Rendering

```jsx
return (
  <div className="max-w-xl mx-auto bg-white p-6 mt-6 rounded-lg shadow-md">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Create Assignment</h2>
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
        className="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition"
      >
        Create Assignment
      </button>
    </form>
  </div>
);
```

- **Container**:
  - A centered card (`max-w-xl`, `mx-auto`) with white background, padding, shadow, and rounded corners.
- **Header**:
  - A bold title ("Create Assignment") in large, dark gray text.
- **Form**:
  - Contains inputs for title (text), description (textarea), and due date (date picker).
  - Inputs are full-width, bordered, and rounded, with labels.
  - Submit button is green with a hover effect.
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
  - **Button**: Green background (`bg-green-500`), white text, padded (`py-2 px-4`), rounded (`rounded-md`), hover effect (`hover:bg-green-600`), smooth transition (`transition`).

## Assumptions

- **API Endpoint**:
  - `POST /api/assignment/course/${courseId}/assignments`: Creates an assignment with `title`, `description`, and `dueDate`.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId`.
- **Routing**:
  - The route `/course/:courseId/assignments` exists for redirection after creation.
- **Authorization**:
  - Backend validates that the user (faculty) is authorized to create assignments for the course.
- **Due Date Format**:
  - The `dueDate` input (HTML `type="date"`) provides a valid date string compatible with the backend.

## Notes

- **Unused Faculty ID**:
  - `facultyId` is retrieved but not included in the API request, suggesting the backend may use authentication headers or session data to verify the user.
- **Error Handling**:
  - Uses `alert` for validation and errors, which is suboptimal for user experience.
- **Validation**:
  - Basic client-side validation checks for empty fields but lacks advanced checks (e.g., date validity).
- **No Loading State**:
  - Submission lacks a loading indicator, which could confuse users during network delays.
- **No Cancel Option**:
  - The form doesn’t provide a way to cancel and return to the assignment list.
- **Security**:
  - Assumes backend validation for course access and assignment creation permissions.

## Future Improvements

- **Better Error Handling**:
  - Replace `alert` with a toast library (e.g., `react-hot-toast`) for better UX:
- **Loading State**:
  - Add a loading indicator during submission.
- **Advanced Validation**:
  - Validate due date to ensure it’s in the future.
- **Testing**:
  - Write unit tests for form validation, submission, and navigation.
- **Error Boundary**:
  - Wrap the component in an error boundary to handle unexpected errors.
- **Form Reset**:
  - Reset form fields after successful submission (though navigation currently makes this unnecessary).