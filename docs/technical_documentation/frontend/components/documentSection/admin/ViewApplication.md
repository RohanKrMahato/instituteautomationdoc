# Technical Documentation: ViewApplication Component

## Overview

The `ViewApplication` component is a React-based front-end module designed to display detailed information about a specific document application (e.g., bonafide certificate or passport) for an academic institution (e.g., IIT Guwahati). It operates as a modal dialog, fetching application details via an API and presenting student information, document details, and approval history. The component integrates with **Tanstack Query** for data fetching, **React Hot Toast** for error notifications, and **React Icons** for UI elements. It is styled using **Tailwind CSS** for a modern, responsive design.

## Dependencies

- **React**: For building the component.
- **Tanstack Query (@tanstack/react-query)**: For fetching application details.
- **newRequest**: A custom utility for making HTTP requests (assumed to be an Axios wrapper).
- **React Hot Toast**: For displaying error notifications.
- **React Icons**: Provides icons (`FaTimesCircle`, `FaEdit`) for UI buttons.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `ViewApplication` component is structured as a modal with the following sections:

1. **Header**: Displays the application ID and includes buttons to manage or close the modal.
2. **Status Badge**: Shows the application status (Approved, Rejected, or Pending).
3. **Student Information**: Lists student details (e.g., name, roll number, department).
4. **Document Details**: Shows document-specific information (e.g., purpose for bonafide, travel plans for passport).
5. **Approval History**: Displays remarks and approval details.

## Code Explanation

### Imports

```jsx
import React from 'react';
import { FaTimesCircle, FaEdit } from 'react-icons/fa';
import { useQuery } from "@tanstack/react-query";
import newRequest from '../../../utils/newRequest';
import { toast } from 'react-hot-toast';
```

- **React**: Required for defining the component.
- **React Icons**: Imports `FaTimesCircle` (close button) and `FaEdit` (manage button).
- **useQuery**: For fetching application details from the API.
- **newRequest**: A utility for API requests (likely Axios-based).
- **toast**: For displaying error notifications.

### Component Definition

```jsx
const ViewApplication = ({ application, onClose, onManage }) => {
```

- **Props**:
  - `application`: An object containing at least an `id` field for fetching details.
  - `onClose`: A callback function to close the modal.
  - `onManage`: A callback function to navigate to the application management interface.

### Data Fetching

```jsx
const { data: details, isLoading, error } = useQuery({
    queryKey: ['application-details', application.id],
    queryFn: () => newRequest.get(`/acadAdmin/documents/applications/${application.id}`)
        .then(res => res.data),
    onError: (error) => {
        toast.error(error?.response?.data?.message || 'Error fetching application details');
    }
});
```

- Uses `useQuery` to fetch detailed application data.
- `queryKey`: `['application-details', application.id]` ensures caching per application ID.
- `queryFn`: Makes a GET request to `/acadAdmin/documents/applications/${application.id}` and returns the response data.
- `onError`: Displays a toast notification with the server error message or a generic fallback.
- Returns `details` (renamed from `data`), `isLoading`, and `error`.

### Loading State

```jsx
if (isLoading) {
    return (
        <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white p-8 rounded-xl">
                Loading application details...
            </div>
        </div>
    );
}
```

- Displays a centered modal with a loading message during data fetching.
- Uses Tailwind classes: `fixed inset-0` for full-screen overlay, `bg-gray-900/50 backdrop-blur-sm` for a semi-transparent blurred background, `z-50` for high stacking order, `bg-white p-8 rounded-xl` for the loading container.

### Error State

```jsx
if (error) {
    return (
        <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white p-8 rounded-xl text-red-500">
                Error loading application details. Please try again.
            </div>
        </div>
    );
}
```

- Displays an error message in a modal if the data fetch fails.
- Similar styling to the loading state, with `text-red-500` for error text.

### Main Rendering

```jsx
return (
    <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            ...
        </div>
    </div>
);
```

- Renders a full-screen modal with a semi-transparent blurred background.
- The inner container (`bg-white rounded-xl`) has a max-width (`max-w-4xl`), max-height (`max-h-[90vh]`), and auto-scrolling (`overflow-y-auto`) for large content.
- Adds padding (`p-4`) to prevent content from touching screen edges.

#### Header

```jsx
<div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-center">
    <div>
        <h2 className="text-2xl font-bold text-gray-900">Application Details</h2>
        <p className="text-sm text-gray-500">Application #{application.id}</p>
    </div>
    <div className="flex gap-2">
        <button 
            onClick={onManage}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Manage Application"
        >
            <FaEdit className="text-gray-500" />
        </button>
        <button 
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
            <FaTimesCircle className="text-gray-500" />
        </button>
    </div>
</div>
```

- A sticky header with a bottom border, aligned with flexbox (`justify-between items-center`).
- Left side: Shows "Application Details" and the application ID (`text-sm text-gray-500`).
- Right side: Two buttons:
  - **Manage**: Triggers `onManage` with an edit icon (`FaEdit`), styled with hover effects.
  - **Close**: Triggers `onClose` with a close icon (`FaTimesCircle`), styled similarly.

#### Status Badge

```jsx
<div className="flex justify-center">
    <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium
        ${details.status === 'Approved' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' :
        details.status === 'Rejected' ? 'bg-rose-100 text-rose-800 border border-rose-300' :
        'bg-amber-100 text-amber-800 border border-amber-300'}`}>
        {details.status.charAt(0).toUpperCase() + details.status.slice(1)}
    </span>
</div>
```

- Displays the application status (Approved, Rejected, or Pending) in a centered badge.
- Uses conditional Tailwind classes:
  - Approved: Green (`bg-emerald-100 text-emerald-800 border-emerald-300`).
  - Rejected: Red (`bg-rose-100 text-rose-800 border-rose-300`).
  - Pending: Yellow (`bg-amber-100 text-amber-800 border-amber-300`).
- Capitalizes the status text for display (e.g., "approved" → "Approved").

#### Student Information

```jsx
<section className="space-y-4">
    <h3 className="text-lg font-semibold">Student Information</h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Name</p>
            <p className="font-medium">{details.studentDetails?.name}</p>
        </div>
        ...
        {details.documentType === 'Passport' && (
            <>
                <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-500">Father's Name</p>
                    <p className="font-medium">{details.studentDetails?.fathersName}</p>
                </div>
                ...
            </>
        )}
    </div>
</section>
```

- Displays student details in a responsive grid (1 column on mobile, 2 on medium screens).
- Each item is in a light gray card (`bg-gray-50 p-4 rounded-lg`) with a label (`text-sm text-gray-500`) and value (`font-medium`).
- Fields include name, roll number, department, program, email, contact number, batch, semester, hostel, and room number.
- For passport applications, adds father’s name, mother’s name, and date of birth (formatted with `toLocaleDateString`).
- Uses optional chaining (`?.`) to handle missing `studentDetails`.

#### Document Details

```jsx
<section className="space-y-4">
    <h3 className="text-lg font-semibold">Document Details</h3>
    <div className="bg-gray-50 p-4 rounded-lg">
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <dt className="text-sm text-gray-500">Document Type</dt>
                <dd className="font-medium capitalize">{details.documentType}</dd>
            </div>
            {details.documentType === 'Bonafide' ? (
                <>
                    <div>
                        <dt className="text-sm text-gray-500">Purpose</dt>
                        <dd className="font-medium">{details.details?.purpose || 'N/A'}</dd>
                    </div>
                    ...
                </>
            ) : details.documentType === 'Passport' && (
                <>
                    <div>
                        <dt className="text-sm text-gray-500">Application Type</dt>
                        <dd className="font-medium capitalize">{details.details?.applicationType || 'N/A'}</dd>
                    </div>
                    ...
                </>
            )}
        </dl>
    </div>
</section>
```

- Displays document-specific details in a definition list (`<dl>`) with a responsive grid.
- Always shows `documentType` (capitalized).
- For **Bonafide**:
  - Shows purpose, other reason (if purpose is "Other"), and current semester.
- For **Passport**:
  - Shows application type, place of birth, semester, mode, tatkal reason (if mode is "tatkal"), travel plans, travel details, and travel period (if applicable).
  - Formats dates with `toLocaleDateString`.
- Uses `N/A` for missing fields.

#### Approval History

```jsx
<section className="space-y-4">
    <h3 className="text-lg font-semibold">Approval History</h3>
    <div className="space-y-3">
        {details.approvalDetails?.remarks?.map((remark, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-900">{remark}</p>
                <div className="mt-2 text-sm text-gray-500">
                    By: {details.approvalDetails.approvedBy?.name || 'Admin'}
                </div>
            </div>
        ))}
    </div>
</section>
```

- Lists approval remarks in individual cards.
- Each remark includes the comment and the approver’s name (defaults to "Admin" if missing).
- Styled with light gray cards (`bg-gray-50 p-4 rounded-lg`).

### Export

```jsx
export default ViewApplication;
```

- Exports the component for use in other parts of the application.

## Styling

- **Tailwind CSS**: Used for responsive, utility-first styling.
  - **Modal**: `fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50` creates a full-screen blurred overlay.
  - **Container**: `bg-white rounded-xl max-w-4xl max-h-[90vh] overflow-y-auto` ensures a scrollable, constrained modal.
  - **Header**: `sticky top-0 border-b` keeps it visible while scrolling.
  - **Badges**: Color-coded for status (emerald, rose, amber).
  - **Cards**: `bg-gray-50 p-4 rounded-lg` for consistent info blocks.
  - **Buttons**: Hover effects (`hover:bg-gray-100`) and transitions.
- **Responsive Design**: Uses `md:grid-cols-2` for grids and `p-4` for mobile padding.

## Assumptions

- **newRequest**: A pre-configured Axios instance for API requests.
- **API Endpoint**: `GET /acadAdmin/documents/applications/${application.id}` returns detailed application data with fields like `status`, `studentDetails`, `details`, and `approvalDetails`.
- **Data Structure**: Expects nested objects (e.g., `studentDetails.name`, `details.purpose`).
- **Parent Component**: Provides valid `application` (with `id`), `onClose`, and `onManage` props.

## Notes

- **Error Handling**: Robust for API failures, but no fallback for missing `details` fields beyond `N/A`.
- **Dynamic Fields**: Handles bonafide and passport applications differently, assuming only these types.
- **Approval History**: Assumes remarks exist; an empty state UI might be needed.
- **Accessibility**: Lacks ARIA attributes for the modal and buttons.

## Future Improvements

- **Empty States**: Add UI for empty remarks or missing details.
- **Validation**: Validate `application.id` and handle invalid props.
- **Accessibility**: Add `role="dialog"`, `aria-labelledby`, and keyboard navigation (e.g., close on Esc).
- **Dynamic Document Types**: Support more document types via a configuration object.
- **Testing**: Write unit tests for loading, error, and data rendering states.
- **Error Recovery**: Add a retry button for failed API calls.
- **Focus Management**: Trap focus within the modal for accessibility.