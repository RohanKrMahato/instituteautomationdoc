# FacultyAnnouncements Component

## Overview

The `FacultyCourseAnnouncements` component is a React-based front-end module designed to manage course announcements for faculty members at an academic institution (e.g., IIT Guwahati). It allows faculty to view, add, edit, and delete announcements for a specific course, fetched dynamically using the course ID from the URL. The component integrates with **Tanstack Query** for data fetching and mutations, uses **React Router** for navigation, and is styled with **Tailwind CSS**. It includes form validation, error handling, and a responsive UI.

## Dependencies

- **React**: For building the UI and managing state.
- **React Router (react-router-dom)**: For accessing URL parameters (`useParams`), navigation (`useNavigate`), and linking (`Link`).
- **Tanstack Query (@tanstack/react-query)**: For data fetching (`useQuery`), mutations (`useMutation`), and cache management (`useQueryClient`).
- **newRequest**: A custom utility for HTTP requests (assumed to be an Axios wrapper).
- **React Icons (react-icons/fa)**: For rendering icons (e.g., arrows, bullhorn, calendar).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `FacultyCourseAnnouncements` component is organized into the following sections:

1. **Header**: Displays the course name and a back button to the courses list.
2. **Course Info**: Shows course details (code, department, credits, status).
3. **Announcement Form**: A form to add or edit announcements (toggles visibility).
4. **Announcements List**: Displays all announcements for the course with edit and delete options.

## Code Explanation

### Imports

```jsx
import { useParams, Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { FaArrowLeft, FaBullhorn, ... } from "react-icons/fa";
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import newRequest from "../../utils/newRequest";
```

- **React Router**:
  - `useParams`: Extracts `courseId` from the URL.
  - `Link`: Creates a link back to the courses page.
  - `useNavigate`: Provides programmatic navigation (not used in the current implementation).
- **React** and `useState`: For managing component state.
- **React Icons**: Icons for visual enhancement (e.g., back arrow, bullhorn, check).
- **Tanstack Query**:
  - `useQuery`: Fetches course data.
  - `useMutation`: Handles adding, editing, and deleting announcements.
  - `useQueryClient`: Manages query cache.
- **newRequest**: Utility for API requests.

### State Management

```jsx
const { courseId } = useParams();
const [course, setCourse] = useState(null);
const [isAddingAnnouncement, setIsAddingAnnouncement] = useState(false);
const [isEditing, setIsEditing] = useState(false);
const [editingAnnouncementId, setEditingAnnouncementId] = useState(null);
const [formData, setFormData] = useState({
  title: "",
  content: "",
  importance: "Medium",
});
const [formErrors, setFormErrors] = useState({});
```

- `courseId`: Extracted from the URL parameters.
- `course`: Stores fetched course data.
- `isAddingAnnouncement`: Toggles the visibility of the announcement form.
- `isEditing`: Tracks whether the form is in edit mode.
- `editingAnnouncementId`: Stores the ID of the announcement being edited.
- `formData`: Manages form inputs (title, content, importance).
- `formErrors`: Tracks form validation errors.

### User Data

```jsx
const currentUser = JSON.parse(localStorage.getItem("currentUser"));
const userId = currentUser?.data?.user?.userId;
const facultyName = currentUser?.data?.user?.email;
const facultyNameWithoutDomain = facultyName?.split("@")[0];
```

- Retrieves user data from `localStorage`.
- Extracts `userId` and `facultyName`, deriving `facultyNameWithoutDomain` for use as the `postedBy` field.

### Data Fetching with Tanstack Query

```jsx
const { 
  isLoading, 
  error, 
  data 
} = useQuery({
  queryKey: ["facultyCourseAnnouncements", courseId],
  queryFn: () => 
    newRequest.get(`/faculty/courses/${courseId}/announcements`).then((res) => {
      setCourse(res.data);
      return res.data;
    }),
  enabled: !!courseId
});
```

- Fetches course data and announcements for the given `courseId`.
- `queryKey`: Unique key (`["facultyCourseAnnouncements", courseId]`) for caching.
- `queryFn`: GET request to `/faculty/courses/${courseId}/announcements`.
- `enabled`: Only runs if `courseId` exists.
- Updates `course` state and returns the data.

### Mutations

#### Add Announcement

```jsx
const addAnnouncementMutation = useMutation({
  mutationFn: (announcementData) => {
    return newRequest.post(`/faculty/courses/${courseId}/announcements/add`, announcementData);
  },
  onSuccess: () => {
    queryClient.invalidateQueries(["facultyCourseAnnouncements", courseId]);
    resetForm();
    setIsAddingAnnouncement(false);
  },
  onError: (error) => {
    // Handle error state
  }
});
```

- Posts a new announcement to `/faculty/courses/${courseId}/announcements/add`.
- On success:
  - Invalidates the course announcements query to refresh the list.
  - Resets the form and hides it.

#### Edit Announcement

```jsx
const editAnnouncementMutation = useMutation({
  mutationFn: ({ announcementId, announcementData }) => {
    return newRequest.put(`/faculty/courses/${courseId}/announcements/${announcementId}/update`, announcementData);
  },
  onSuccess: () => {
    queryClient.invalidateQueries(["facultyCourseAnnouncements", courseId]);
    resetForm();
    setIsEditing(false);
    setEditingAnnouncementId(null);
  },
  onError: (error) => {
    // Handle error state
  }
});
```

- Updates an existing announcement via PUT to `/faculty/courses/${courseId}/announcements/${announcementId}/update`.
- On success:
  - Refreshes the announcements list.
  - Resets the form and edit state.

#### Delete Announcement

```jsx
const deleteAnnouncementMutation = useMutation({
  mutationFn: (announcementId) => {
    return newRequest.delete(`/faculty/courses/${courseId}/announcements/${announcementId}/delete`);
  },
  onSuccess: () => {
    queryClient.invalidateQueries(["facultyCourseAnnouncements", courseId]);
  },
  onError: (error) => {
    // Handle error state
  }
});
```

- Deletes an announcement via DELETE to `/faculty/courses/${courseId}/announcements/${announcementId}/delete`.
- On success:
  - Refreshes the announcements list.

### Form Handlers

#### Input Change

```jsx
const handleInputChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({
    ...prev,
    [name]: value
  }));
  if (formErrors[name]) {
    setFormErrors(prev => ({
      ...prev,
      [name]: ""
    }));
  }
};
```

- Updates `formData` with input values and clears corresponding errors.

#### Reset Form

```jsx
const resetForm = () => {
  setFormData({
    title: "",
    content: "",
    importance: "Medium"
  });
  setFormErrors({});
};
```

- Resets `formData` to initial values and clears errors.

#### Cancel Form

```jsx
const handleCancel = () => {
  setIsAddingAnnouncement(false);
  setIsEditing(false);
  setEditingAnnouncementId(null);
  resetForm();
};
```

- Hides the form, exits edit mode, and resets state.

#### Form Validation

```jsx
const validateForm = () => {
  const errors = {};
  if (!formData.title.trim()) errors.title = "Title is required";
  if (!formData.content.trim()) errors.content = "Content is required";
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};
```

- Validates that `title` and `content` are non-empty.
- Stores errors in `formErrors` and returns `true` if valid.

#### Form Submission

```jsx
const handleSubmit = (e) => {
  e.preventDefault();
  if (!validateForm()) return;
  const announcementData = {
    ...formData,
    postedBy: facultyNameWithoutDomain,
  };
  if (isEditing && editingAnnouncementId) {
    editAnnouncementMutation.mutate({ 
      announcementId: editingAnnouncementId, 
      announcementData 
    });
  } else {
    addAnnouncementMutation.mutate(announcementData);
  }
};
```

- Prevents default form submission.
- Validates the form; if invalid, exits early.
- Constructs `announcementData` with `postedBy`.
- Submits via `editAnnouncementMutation` if editing, or `addAnnouncementMutation` if adding.

#### Edit Announcement

```jsx
const handleEditAnnouncement = (announcement) => {
  setIsEditing(true);
  setEditingAnnouncementId(announcement.id);
  setFormData({
    title: announcement.title,
    content: announcement.content,
    importance: announcement.importance
  });
  setIsAddingAnnouncement(true);
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
```

- Populates the form with the announcement’s data, sets edit mode, and scrolls to the top.

#### Delete Announcement

```jsx
const handleDeleteAnnouncement = (announcementId) => {
  if (window.confirm("Are you sure you want to delete this announcement?")) {
    deleteAnnouncementMutation.mutate(announcementId);
  }
};
```

- Prompts for confirmation before deleting an announcement.

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

- `getImportanceClass`: Returns a Tailwind background color class based on importance.
- `getImportanceLabel`: Returns a user-friendly label for the importance level.

### Rendering

#### Loading State

```jsx
if (isLoading) {
  return (
    <div className="p-6 flex justify-center items-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading course data...</p>
      </div>
    </div>
  );
}
```

- Displays a spinner and message during data fetching.

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
        <Link to="/faculty/courses" className="...">Return to My Courses</Link>
      </div>
    </div>
  );
}
```

- Shows an error message with a link back to the courses page if the fetch fails.

#### Main UI

```jsx
return (
  <div className="p-6 max-w-4xl mx-auto">
    {/* Header */}
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center">
        <Link to="/courses" className="mr-4 text-pink-500 hover:text-pink-600">
          <FaArrowLeft className="text-xl" />
        </Link>
        <h1 className="text-3xl font-bold text-gray-800">{course?.courseName} Announcements</h1>
      </div>
      {!isAddingAnnouncement && (
        <button onClick={() => setIsAddingAnnouncement(true)} className="...">
          <FaPlus /> New Announcement
        </button>
      )}
    </div>

    {/* Course Info */}
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        ...
      </div>
    </div>

    {/* Form */}
    {isAddingAnnouncement && (
      <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
        <form onSubmit={handleSubmit}>
          ...
        </form>
      </div>
    )}

    {/* Announcements List */}
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Published Announcements</h2>
    {!course?.announcements || course.announcements.length === 0 ? (
      <div className="bg-gray-100 rounded-lg p-8 text-center">...</div>
    ) : (
      <div className="space-y-6">
        {course.announcements.map((announcement) => (
          <div key={announcement.id} className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
            ...
          </div>
        ))}
      </div>
    )}
  </div>
);
```

- **Header**: Includes a back button and a button to toggle the form.
- **Course Info**: Displays course details in a responsive grid.
- **Form**: Conditionally rendered for adding/editing announcements with validation.
- **Announcements List**: Shows announcements with importance badges, edit/delete buttons, and meta information.

## Styling

- **Tailwind CSS**: Used for responsive, modern styling.
  - Containers: `max-w-4xl`, `p-6`, `rounded-lg`, `shadow-md`.
  - Buttons: Pink theme (`bg-pink-500`, `hover:bg-pink-600`), transitions.
  - Forms: Bordered inputs (`border-gray-300`), error states (`border-red-500`), focus rings.
  - Cards: White background, shadows, borders.
  - Badges: Color-coded importance (`bg-red-500`, `bg-blue-500`), status (`bg-green-100`).
- **Responsive Design**: Uses Tailwind’s responsive classes (e.g., `md:grid-cols-4`).

## Assumptions

- **newRequest**: A pre-configured Axios instance for API requests.
- **API Endpoints**:
  - `GET /faculty/courses/${courseId}/announcements`: Fetches course and announcements.
  - `POST /faculty/courses/${courseId}/announcements/add`: Adds a new announcement.
  - `PUT /faculty/courses/${courseId}/announcements/${announcementId}/update`: Updates an announcement.
  - `DELETE /faculty/courses/${courseId}/announcements/${announcementId}/delete`: Deletes an announcement.
- **localStorage**: Stores `currentUser` with a nested `data.user` object containing `userId` and `email`.
- **Course Data**: Includes `courseName`, `courseCode`, `department`, `credits`, `status`, and `announcements` array.

## Notes

- **Commented-Out Attachments**: The code includes commented-out logic for handling file attachments, suggesting planned but unimplemented functionality.
- **Error Handling**: Minimal for mutations; consider adding user-facing error messages (e.g., toasts).
- **Navigation**: `useNavigate` is imported but unused; could be used for redirects on error.
- **Security**: Assumes `userId` and course access are validated server-side.

## Future Improvements

- **Error Notifications**: Use a toast library (e.g., `react-hot-toast`) for mutation errors.
- **Attachments**: Implement the commented-out attachment functionality (e.g., file uploads to a server).
- **Loading States**: Add spinners for mutation operations.
- **Confirmation Modals**: Replace `window.confirm` with a custom modal for deletions.
- **Accessibility**: Add ARIA attributes and keyboard navigation.
- **Testing**: Write unit tests for form validation, mutations, and rendering logic.
- **Dynamic Routing**: Use `navigate` to redirect on unauthorized access or errors.