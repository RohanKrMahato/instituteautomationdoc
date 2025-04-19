# BonafidePage Component

## Overview

The `BonafidePage` component is a React-based front-end module designed to facilitate the application process for a bonafide certificate for students at an academic institution (e.g., IIT Guwahati). It allows students to submit applications, view their application history, and displays their personal information. The component integrates with **Tanstack Query** for data fetching and mutation, uses **React Hot Toast** for notifications, and is styled with **Tailwind CSS** and **DaisyUI**. It features a tabbed interface for switching between application submission and status views.

## Dependencies

- **React**: For building the UI and managing state.
- **Tanstack Query (@tanstack/react-query)**: For data fetching, caching, and mutations.
- **React Hot Toast**: For displaying success and error notifications.
- **newRequest**: A custom utility for making HTTP requests (assumed to be an Axios wrapper).
- **React Icons**: For rendering icons from the `react-icons/fa` library.
- **DocumentLayout**: A custom component for consistent page layout.
- **Tailwind CSS** and **DaisyUI**: For styling the component.

## Component Structure

The `BonafidePage` component is organized into two main views, controlled by a tabbed interface:

1. **Application Form**: Allows students to submit a bonafide certificate application with details like semester and purpose.
2. **Application Status**: Displays a table of past applications with their status, purpose, and remarks.

The component also displays student information and handles form validation, data fetching, and mutations.

## Code Explanation

### Imports

```jsx
import React, { useState } from 'react';
import DocumentLayout from '../../components/documentSection/DocumentLayout';
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import newRequest from "../../utils/newRequest";
import { toast } from 'react-hot-toast';
import { FaCircle, FaUser, FaIdBadge, ... } from "react-icons/fa";
```

- **React** and `useState`: For managing component state.
- **DocumentLayout**: Wraps the page content for consistent styling.
- **Tanstack Query**: Provides `useQuery` for fetching data, `useMutation` for submitting applications, and `useQueryClient` for cache management.
- **newRequest**: A utility for API requests (likely Axios-based).
- **react-hot-toast**: For displaying toast notifications.
- **react-icons/fa**: Icons for visual enhancement (e.g., user, calendar, etc.).

### State Management

```jsx
const initialFormData = {
  currentSemester: '',
  certificateFor: '',
  otherReason: ''
};
const [formData, setFormData] = useState(initialFormData);
const [formErrors, setFormErrors] = useState({});
const [activeTab, setActiveTab] = useState('application');
```

- `formData`: Stores form input values (semester, certificate purpose, and other reason if applicable).
- `formErrors`: Tracks validation errors for form fields.
- `activeTab`: Controls the active view (`application` or `status`).

### User Data

```jsx
const {data:userData} = JSON.parse(localStorage.getItem("currentUser"));
const {userId} = userData.user;
```

- Retrieves user data from `localStorage` and extracts `userId` for API requests.
- Assumes `currentUser` is stored as a JSON string with a `user` object containing `userId`.

### Data Fetching with Tanstack Query

#### Student Data

```jsx
const { isLoading, error, data: studentData } = useQuery({
  queryKey: [`bonafide-${userId}`],
  queryFn: () => newRequest.get(`/student/${userId}/bonafide`).then((res) => res.data),
});
```

- Uses `useQuery` to fetch student information for the given `userId`.
- `queryKey`: Unique key (`bonafide-${userId}`) for caching.
- `queryFn`: Makes a GET request to `/student/${userId}/bonafide` and returns the response data.
- Returns `isLoading`, `error`, and `studentData` (renamed from `data`).

#### Application History

```jsx
const { data: applications = [] } = useQuery({
  queryKey: ['bonafide-applications'],
  queryFn: () => newRequest.get(`/student/${userId}/bonafide/applications`).then((res) => res.data),
});
```

- Fetches the student's bonafide application history.
- `queryKey`: `bonafide-applications` for caching.
- `queryFn`: GET request to `/student/${userId}/bonafide/applications`.
- Defaults `data` to an empty array if undefined.

### Mutation for Application Submission

```jsx
const queryClient = useQueryClient();
const createApplication = useMutation({
  mutationFn: (formData) => {
    return newRequest.post(`/student/${userId}/bonafide/apply`, formData);
  },
  onSuccess: () => {
    queryClient.invalidateQueries(['bonafide-applications']);
    toast.success('Bonafide application submitted successfully');
    setFormData(initialFormData);
    setActiveTab('status');
  },
  onError: (error) => {
    toast.error(error?.response?.data?.message || 'Error submitting application');
  },
});
```

- `useQueryClient`: Provides access to the query cache.
- `useMutation`: Handles the POST request to submit a bonafide application.
  - `mutationFn`: Sends `formData` to `/student/${userId}/bonafide/apply`.
  - `onSuccess`: Invalidates the `bonafide-applications` query to refresh the history, shows a success toast, resets the form, and switches to the status tab.
  - `onError`: Displays an error toast with the server message or a generic error.

### Loading and Error States

```jsx
if (isLoading) {
  return (
    <DocumentLayout title="Bonafide Certificate">
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading student information...</p>
        </div>
      </DocumentLayout>
    );
}
if (error) {
  return (
    <DocumentLayout title="Bonafide Certificate">
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <FaExclamationCircle className="h-5 w-5 text-red-500" />
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">
              Error loading student information. Please try again later.
            </p>
          </div>
        </div>
      </div>
    </DocumentLayout>
  );
}
```

- **Loading**: Displays a spinner and message while `studentData` is being fetched.
- **Error**: Shows an error alert with an icon if the student data fetch fails.
- Both use `DocumentLayout` for consistent page structure.

### Student Information

```jsx
const studentInfo = [
  { label: "Name", value: studentData?.name || "Loading...", icon: FaUser },
  { label: "Roll No", value: studentData?.rollNo || "Loading...", icon: FaIdBadge },
  ...
];
```

- Defines an array of student details (e.g., name, roll number, hostel) with corresponding icons.
- Uses optional chaining (`?.`) to handle undefined `studentData` and defaults to "Loading...".

### Certificate Reasons

```jsx
const certificateReasons = [
  'Bank Account Opening',
  'Passport Application',
  'Visa Application',
  'Education Loan',
  'Scholarship Application',
  'Other'
];
```

- Lists predefined reasons for requesting a bonafide certificate.
- Includes an "Other" option that triggers a text input for custom reasons.

### Form Validation

```jsx
const validateForm = () => {
  const errors = {};
  if (!formData.currentSemester) {
    errors.currentSemester = 'Please select a semester';
  }
  if (!formData.certificateFor) {
    errors.certificateFor = 'Please select a purpose';
  }
  if (formData.certificateFor === 'Other' && !formData.otherReason?.trim()) {
    errors.otherReason = 'Please specify the reason';
  }
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};
```

- Validates form inputs:
  - `currentSemester`: Must be selected.
  - `certificateFor`: Must be selected.
  - `otherReason`: Required if `certificateFor` is "Other" and must not be empty.
- Stores errors in `formErrors` and returns `true` if no errors.

### Input Handling

```jsx
const handleInputChange = (e) => {
  const { name, value } = e.target;
  setFormData((prev) => ({
    ...prev,
    [name]: value,
    ...(name === 'certificateFor' && value !== 'Other' ? { otherReason: '' } : {})
  }));
  if (formErrors[name]) {
    setFormErrors(prev => ({ ...prev, [name]: '' }));
  }
};
```

- Updates `formData` with input values.
- Clears `otherReason` if `certificateFor` changes to a non-"Other" value.
- Removes corresponding errors from `formErrors` when the user types.

### Form Submission

```jsx
const handleSubmit = (e) => {
  e.preventDefault();
  if (validateForm()) {
    const submissionData = {
      currentSemester: formData.currentSemester,
      certificateFor: formData.certificateFor,
      otherReason: formData.certificateFor === 'Other' ? formData.otherReason : undefined
    };
    createApplication.mutate(submissionData);
  }
};
```

- Prevents default form submission.
- Validates the form; if valid, submits `submissionData` (excluding `otherReason` unless needed).
- Triggers the `createApplication` mutation.

### Helper Component: `InfoDisplay`

```jsx
const InfoDisplay = ({ label, value, icon: Icon }) => (
  <div className="flex items-center space-x-3 py-2">
    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-indigo-200 shadow-sm">
      <Icon className="w-5 h-5 text-indigo-600" />
    </div>
    <div>
      <div className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-0.5">{label}</div>
      <div className="text-sm font-semibold text-gray-800">{value}</div>
    </div>
  </div>
);
```

- Renders a student info item with an icon, label, and value.
- Uses Tailwind for styling (e.g., rounded icon container, text formatting).

### Application Form Rendering

```jsx
const renderApplicationForm = () => (
  <form onSubmit={handleSubmit} className="space-y-10">
    <div className="card ...">...</div>
    <div className="card ...">
      <h3 className="...">Student Information</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
        {studentInfo.map((item, index) => (
          <InfoDisplay key={index} label={item.label} value={item.value} icon={item.icon} />
        ))}
      </div>
    </div>
    <div className="card ...">
      <h3 className="...">Additional Details Required</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="form-control ...">
          <select name="currentSemester" ...>...</select>
          {formErrors.currentSemester && <label ...>{formErrors.currentSemester}</label>}
        </div>
        <div className="form-control ...">
          <select name="certificateFor" ...>...</select>
          {formErrors.certificateFor && <label ...>{formErrors.certificateFor}</label>}
        </div>
        {formData.certificateFor === 'Other' && (
          <div className="form-control ...">
            <input type="text" name="otherReason" ... />
            {formErrors.otherReason && <label ...>{formErrors.otherReason}</label>}
          </div>
        )}
      </div>
    </div>
    <div className="flex justify-end gap-4 mt-8">
      <button type="button" ...>Reset Form</button>
      <button type="submit" ...>Submit Application</button>
    </div>
  </form>
);
```

- Renders a form with:
  - A header card with form metadata.
  - A student information grid using `InfoDisplay`.
  - Input fields for semester, certificate purpose, and conditional "Other" reason.
  - Reset and submit buttons.
- Uses Tailwind and DaisyUI for styling (e.g., `card`, `select`, `btn`).

### Status Rendering

```jsx
const renderStatus = () => (
  <div className="space-y-8">
    <div className="flex ...">
      <h3 className="...">Application Status History</h3>
      <div className="...">Total Applications: {applications.length}</div>
    </div>
    <div className="overflow-x-auto ...">
      <table className="...">
        <thead>...</thead>
        <tbody>
          {applications.length === 0 ? (
            <tr><td colSpan="5" ...>No applications found.</td></tr>
          ) : (
            applications.map((app, index) => (
              <tr key={index} ...>
                <td ...>{index + 1}.</td>
                <td ...>{new Date(app.applicationDate).toLocaleString(...)}</td>
                <td ...><span ...>{app.certificateFor}</span></td>
                <td ...><span ...>{app.currentStatus}</span></td>
                <td ...>{app.remarks ? ... : <span ...>No remarks</span>}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  </div>
);
```

- Displays a table of past applications with columns for serial number, date, purpose, status, and remarks.
- Handles empty states with a message.
- Formats dates and statuses with Tailwind styling (e.g., color-coded status badges).

### Main Render

```jsx
return (
  <DocumentLayout title="Bonafide Certificate">
    <div className="mb-8 flex justify-center sm:justify-start">
      <div className="inline-flex rounded-lg p-1 shadow-inner space-x-1 border border-indigo-200">
        <button className={`... ${activeTab === 'application' ? '...' : '...'}`} onClick={() => setActiveTab('application')}>
          <FaPlus ... /> New Application
        </button>
        <button className={`... ${activeTab === 'status' ? '...' : '...'}`} onClick={() => setActiveTab('status')}>
          <FaListAlt ... /> Application Status
        </button>
      </div>
    </div>
    <div className="bg-white rounded-xl p-6 md:p-8 shadow-lg border border-base-200 min-h-[400px]">
      {activeTab === 'application' ? renderApplicationForm() : renderStatus()}
    </div>
  </DocumentLayout>
);
```

- Renders the page with:
  - A tabbed navigation bar to switch between views.
  - A content area that conditionally renders the form or status table.
- Uses `DocumentLayout` for consistent page structure.

## Styling

- **Tailwind CSS** and **DaisyUI**: Used for responsive, modern styling.
  - Cards: `card`, `shadow`, `border`.
  - Buttons: `btn`, `btn-primary`, `btn-outline`.
  - Tables: `table-auto`, `hover:bg-indigo-50`.
  - Forms: `select`, `input`, `form-control`.
- **Custom Styling**: Gradients (e.g., `bg-gradient-to-r`), shadows, and color-coded badges (green for Approved, red for Rejected, yellow for Pending).
- **Icons**: Used for visual cues (e.g., `FaUser`, `FaCircle`).

## Assumptions

- **newRequest**: A pre-configured Axios instance for API requests.
- **API Endpoints**:
  - `GET /student/${userId}/bonafide`: Returns student details.
  - `GET /student/${userId}/bonafide/applications`: Returns application history.
  - `POST /student/${userId}/bonafide/apply`: Submits a new application.
- **localStorage**: Stores `currentUser` with a `user.userId` field.
- **DocumentLayout**: A wrapper component that accepts a `title` prop.

## Notes

- **Form Validation**: Client-side validation ensures required fields are filled.
- **Error Handling**: Robust handling for loading, errors, and mutation failures.
- **Responsive Design**: Uses Tailwind's responsive classes (e.g., `sm:grid-cols-2`, `md:col-span-2`).
- **Security**: Assumes `userId` is securely stored and validated server-side.

## Future Improvements

- **Server-Side Validation**: Add backend validation to complement client-side checks.
- **Loading States for Mutations**: Show a spinner during form submission.
- **Download Certificate**: Add functionality to download approved certificates as PDFs.
- **Pagination**: Implement pagination for the application history table if data grows large.
- **Accessibility**: Add ARIA attributes and keyboard navigation support.
- **Testing**: Write unit tests for form validation, tab switching, and API interactions.