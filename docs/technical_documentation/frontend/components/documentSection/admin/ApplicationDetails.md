

# Technical Documentation: ApplicationDetails Component

## Overview

The `ApplicationDetails` component is a React-based front-end module designed to allow academic administrators (e.g., at IIT Guwahati) to review and manage a specific document application (e.g., bonafide certificate or passport). Rendered as a modal dialog, it displays application details, allows status updates (approve/reject), and supports adding remarks. It integrates with **Tanstack Query** for data fetching and mutations, **React Hot Toast** for notifications, **React Icons** for UI elements, and is styled with **Tailwind CSS** for a modern, responsive design.

## Dependencies

- **React**: For building the component and managing state (`useState`).
- **React Icons**: Provides icons (`FaTimesCircle`, `FaEye`) for buttons.
- **Tanstack Query (@tanstack/react-query)**: For fetching application details and handling status/comment mutations.
- **newRequest**: A custom utility for HTTP requests (assumed to be an Axios wrapper).
- **React Hot Toast**: For success and error notifications.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `ApplicationDetails` component is structured as a modal with the following sections:

1. **Header**: Displays the application ID and includes buttons to view full details or close the modal.
2. **Status Badge**: Shows the current application status (Approved, Rejected, or Pending).
3. **Quick Info Cards**: Summarizes student name, document type, and submission date.
4. **Approval History**: Lists existing remarks with an option to add new ones.
5. **Action Footer**: Provides buttons to approve or reject the application.

## Code Explanation

### Imports

```jsx
import React, { useState } from 'react';
import { FaTimesCircle, FaEye } from 'react-icons/fa';
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import newRequest from '../../../utils/newRequest';
import { toast } from 'react-hot-toast';
```

- **React**: Provides `useState` for managing local state (`newComment`, `loading`, `applicationStatus`).
- **React Icons**: Imports `FaTimesCircle` (close button) and `FaEye` (view full details button).
- **Tanstack Query**: Imports `useQuery` for fetching data, `useMutation` for status updates and comments, and `useQueryClient` for cache management.
- **newRequest**: Utility for API requests (likely Axios-based).
- **toast**: For displaying notifications.

### Component Definition

```jsx
const ApplicationDetails = ({ application, onClose, onViewFull }) => {
```

- **Props**:
  - `application`: Object containing application data (e.g., `id`, `status`, `studentName`, `rollNo`, `type`, `submittedDate`).
  - `onClose`: Callback to close the modal.
  - `onViewFull`: Callback to view full application details.

### State Management

```jsx
const [newComment, setNewComment] = useState('');
const [loading, setLoading] = useState(false);
const [applicationStatus, setApplicationStatus] = useState(application.status);
```

- `newComment`: Stores the text input for a new remark.
- `loading`: Tracks the status update process to prevent multiple submissions.
- `applicationStatus`: Tracks the current status locally, initialized with `application.status`.

### Query Client

```jsx
const queryClient = useQueryClient();
```

- Initializes `queryClient` for invalidating queries after mutations.

### Data Fetching

```jsx
const { data: details } = useQuery({
    queryKey: ['application-details', application.id],
    queryFn: () => newRequest.get(`/acadAdmin/documents/applications/${application.id}`)
        .then(res => res.data),
    onError: (error) => {
        toast.error(error?.response?.data?.message || 'Error fetching application details');
    }
});
```

- Uses `useQuery` to fetch detailed application data, including remarks.
- `queryKey`: `['application-details', application.id]` ensures caching per application.
- `queryFn`: Makes a GET request to `/acadAdmin/documents/applications/${application.id}`.
- `onError`: Shows a toast with the server error message or a fallback.

### Status Update Mutation

```jsx
const updateStatusMutation = useMutation({
    mutationFn: ({ newStatus, remarks }) => {
        return newRequest.patch(`/acadAdmin/documents/applications/${application.id}/status`, {
            status: newStatus,
            remarks
        });
    },
    onSuccess: () => {
        queryClient.invalidateQueries(['applications']);
        queryClient.invalidateQueries(['application-details', application.id]);
        toast.success('Status updated successfully');
    },
    onError: (error) => {
        toast.error(error?.response?.data?.message || 'Error updating status');
    }
});
```

- Defines a mutation to update the application status.
- `mutationFn`: Sends a PATCH request with the new status and a remark.
- `onSuccess`: Invalidates `applications` and `application-details` queries, shows a success toast.
- `onError`: Shows an error toast.

### Add Comment Mutation

```jsx
const addCommentMutation = useMutation({
    mutationFn: (comment) => {
        return newRequest.post(`/acadAdmin/documents/applications/${application.id}/comment`, {
            comment
        });
    },
    onSuccess: () => {
        queryClient.invalidateQueries(['applications']);
        queryClient.invalidateQueries(['application-details', application.id]);
        setNewComment('');
        toast.success('Comment added successfully');
    },
    onError: (error) => {
        toast.error(error?.response?.data?.message || 'Error adding comment');
    }
});
```

- Defines a mutation to add a comment.
- `mutationFn`: Sends a POST request with the comment text.
- `onSuccess`: Invalidates queries, clears `newComment`, shows a success toast.
- `onError`: Shows an error toast.

### Status Change Handler

```jsx
const handleStatusChange = async (newStatus) => {
    if (loading || applicationStatus === newStatus) return;
    setLoading(true);
    try {
        const properStatus = newStatus.charAt(0).toUpperCase() + newStatus.slice(1).toLowerCase();
        await updateStatusMutation.mutateAsync({
            newStatus: properStatus, 
            remarks: `Application ${properStatus.toLowerCase()}`
        });
        setApplicationStatus(properStatus);
    } catch (error) {
        console.error('Error updating status:', error);
    } finally {
        setLoading(false);
    }
};
```

- Handles status updates (approve/reject).
- Prevents action if already `loading` or if `newStatus` matches `applicationStatus`.
- Capitalizes `newStatus` (e.g., `approved` → `Approved`).
- Calls the status mutation with a remark.
- Updates local `applicationStatus` on success.
- Logs errors and resets `loading`.

### Comment Handler

```jsx
const handleAddComment = async () => {
    if (!newComment.trim()) return;
    addCommentMutation.mutate(newComment);
};
```

- Adds a new comment if `newComment` is non-empty.
- Triggers the comment mutation.

### Remarks Fallback

```jsx
const remarks = details?.approvalDetails?.remarks || [];
```

- Ensures `remarks` is an array, defaulting to empty if `approvalDetails` is undefined.

### Rendering

```jsx
return (
    <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            ...
        </div>
    </div>
);
```

- Renders a full-screen modal with a semi-transparent blurred background (`bg-gray-900/50 backdrop-blur-sm`).
- Inner container is a white card (`bg-white rounded-xl`) with max-width (`max-w-4xl`), max-height (`max-h-[90vh]`), and auto-scrolling (`overflow-y-auto`).

#### Header

```jsx
<div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-center">
    <div>
        <h2 className="text-2xl font-bold text-gray-900">Review Application</h2>
        <p className="text-sm text-gray-500">Application #{application.id}</p>
    </div>
    <div className="flex gap-2">
        <button 
            onClick={onViewFull}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="View Full Application"
        >
            <FaEye className="text-gray-500" />
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

- A sticky header with a bottom border.
- Left: Shows "Review Application" and the application ID.
- Right: Buttons for viewing full details (`FaEye`) and closing (`FaTimesCircle`), with hover effects.

#### Status Badge

```jsx
<div className="flex justify-center">
    <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium
        ${applicationStatus === 'Approved' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' :
        applicationStatus === 'Rejected' ? 'bg-rose-100 text-rose-800 border border-rose-300' :
        'bg-amber-100 text-amber-800 border border-amber-300'}`}>
        {applicationStatus.charAt(0).toUpperCase() + applicationStatus.slice(1)}
    </span>
</div>
```

- Displays the current `applicationStatus` as a centered badge.
- Uses conditional Tailwind classes: green for Approved, red for Rejected, yellow for Pending.
- Capitalizes the status text.

#### Quick Info Cards

```jsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm text-gray-500 mb-1">Student</p>
        <p className="font-medium">{application.studentName}</p>
        <p className="text-sm text-gray-500">{application.rollNo}</p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm text-gray-500 mb-1">Document Type</p>
        <p className="font-medium capitalize">{application.type}</p>
    </div>
    <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm text-gray-500 mb-1">Submitted On</p>
        <p className="font-medium">{application.submittedDate}</p>
    </div>
</div>
```

- Shows student name/roll number, document type, and submission date in a responsive grid (1 column on mobile, 3 on medium screens).
- Styled as light gray cards (`bg-gray-50 p-4 rounded-lg`).

#### Approval History

```jsx
<div className="space-y-4">
    <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Approval History</h3>
        <div className="flex gap-2">
            <input
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Add a remark..."
            />
            <button 
                onClick={handleAddComment}
                className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                disabled={!newComment.trim() || loading}
            >
                Add Remark
            </button>
        </div>
    </div>
    {remarks.length > 0 ? (
        <div className="space-y-3">
            {remarks.map((remark, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-900">{remark}</p>
                    <div className="mt-2 text-sm text-gray-500">
                        By: {details?.approvalDetails?.approvedBy?.name || 'Admin'}
                    </div>
                </div>
            ))}
        </div>
    ) : (
        <div className="text-gray-500 italic">No remarks available</div>
    )}
</div>
```

- Displays remarks with an input and button to add new ones.
- Input is bound to `newComment`, and the button is disabled if empty or loading.
- Remarks are shown in cards with the approver’s name (defaults to "Admin").
- Shows an empty state message if no remarks exist.

####