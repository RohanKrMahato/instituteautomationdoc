

# Technical Documentation: ApplicationsList Component

## Overview

The `ApplicationsList` component is a React-based front-end module designed to display a list of document applications (e.g., bonafide certificates or passports) for an academic institution (e.g., IIT Guwahati). It provides filtering, searching, and bulk action capabilities for managing applications. The component integrates with **Tanstack Query** for data fetching and mutations, **React Hot Toast** for notifications, and **React Icons** for UI elements. It is styled with **Tailwind CSS** for a modern, responsive design.

## Dependencies

- **React**: For building the component and managing state (`useState`, `useEffect`).
- **React Icons**: Provides icons (`FaEye`, `FaEdit`, `FaFileExport`, `FaCheck`, `FaTimes`) for buttons.
- **Tanstack Query (@tanstack/react-query)**: For fetching applications and handling bulk status updates.
- **newRequest**: A custom utility for HTTP requests (assumed to be an Axios wrapper).
- **React Hot Toast**: For success and error notifications.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `ApplicationsList` component is organized into three main sections:

1. **Filters**: Allows filtering by document type, status, and searching by roll number.
2. **Bulk Actions**: Displays options to approve or reject selected applications.
3. **Applications Table**: A table listing applications with checkboxes, details, and action buttons.

## Code Explanation

### Imports

```jsx
import React, { useState, useEffect } from "react";
import { FaEye, FaEdit, FaFileExport, FaCheck, FaTimes } from "react-icons/fa";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import newRequest from '../../../utils/newRequest';
import { toast } from 'react-hot-toast';
```

- **React**: Provides `useState` for state management and `useEffect` for debouncing search input.
- **React Icons**: Imports icons for view (`FaEye`), edit (`FaEdit`), approve (`FaCheck`), reject (`FaTimes`), and export (`FaFileExport`, unused in this code).
- **Tanstack Query**: Imports `useQuery` for fetching data, `useMutation` for updating statuses, and `useQueryClient` for cache management.
- **newRequest**: Utility for API requests.
- **toast**: For displaying notifications.

### Component Definition

```jsx
const ApplicationsList = ({ onSelect, onView }) => {
```

- **Props**:
  - `onSelect`: Callback function to handle managing an application (e.g., navigate to edit view).
  - `onView`: Callback function to view application details.

### State Management

```jsx
const [selectedItems, setSelectedItems] = useState([]);
const [searchInput, setSearchInput] = useState("");
const [filters, setFilters] = useState({
    type: "all",
    status: "all",
    search: "",
});
```

- `selectedItems`: Array of selected application IDs for bulk actions.
- `searchInput`: Immediate value of the search input field.
- `filters`: Object storing filter criteria:
  - `type`: Document type (`all`, `Bonafide`, `Passport`).
  - `status`: Application status (`all`, `pending`, `approved`, `rejected`).
  - `search`: Debounced roll number search term.

### Debounced Search

```jsx
useEffect(() => {
    const timeoutId = setTimeout(() => {
        setFilters(prev => ({
            ...prev,
            search: searchInput
        }));
    }, 500);
    return () => clearTimeout(timeoutId);
}, [searchInput]);
```

- Debounces `searchInput` updates to `filters.search` by 500ms to reduce API calls.
- Uses `setTimeout` to delay updates and `clearTimeout` to clean up on input change or unmount.

### Query Client

```jsx
const queryClient = useQueryClient();
```

- Initializes `queryClient` for invalidating queries after mutations.

### Data Fetching

```jsx
const { data: applications = [], isLoading } = useQuery({
    queryKey: ['applications', filters],
    queryFn: async () => {
        const queryParams = new URLSearchParams();
        if (filters.type !== 'all') {
            queryParams.append('type', filters.type);
        }
        if (filters.status !== 'all') {
            const properStatus = filters.status.charAt(0).toUpperCase() + filters.status.slice(1).toLowerCase();
            queryParams.append('status', properStatus);
        }
        if (filters.search) {
            queryParams.append('rollNo', filters.search);
        }
        const url = `/acadAdmin/documents/applications/filter?${queryParams.toString()}`;
        const response = await newRequest.get(url);
        return response.data;
    }
});
```

- Uses `useQuery` to fetch applications based on `filters`.
- `queryKey`: `['applications', filters]` ensures cache updates when filters change.
- `queryFn`:
  - Builds query parameters using `URLSearchParams`.
  - Adds `type` if not `all`.
  - Capitalizes `status` (e.g., `pending` → `Pending`) if not `all`.
  - Adds `rollNo` for search.
  - Makes a GET request to `/acadAdmin/documents/applications/filter` with parameters.
- Defaults `applications` to an empty array if undefined.

### Bulk Status Mutation

```jsx
const updateStatusMutation = useMutation({
    mutationFn: ({ id, status }) => {
        const properStatus = status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
        return newRequest.patch(`/acadAdmin/documents/applications/${id}/status`, {
            status: properStatus,
            remarks: `Status changed to ${properStatus}`
        });
    },
    onSuccess: () => {
        queryClient.invalidateQueries(['applications']);
        toast.success('Applications updated successfully');
        setSelectedItems([]);
    },
    onError: (error) => {
        toast.error(error?.response?.data?.message || 'Error updating applications');
    }
});
```

- Defines a mutation to update an application’s status.
- `mutationFn`: Sends a PATCH request to `/acadAdmin/documents/applications/${id}/status` with capitalized status and a remark.
- `onSuccess`: Invalidates the `applications` query, shows a success toast, and clears selected items.
- `onError`: Shows an error toast with the server message or a fallback.

### Bulk Action Handler

```jsx
const handleBulkAction = async (action) => {
    const status = action === 'approve' ? 'approved' : 'rejected';
    await Promise.all(
        selectedItems.map(id => updateStatusMutation.mutate({ id, status }))
    );
};
```

- Handles bulk approval or rejection.
- Maps selected IDs to mutation calls with the appropriate status (`approved` or `rejected`).
- Uses `Promise.all` to execute mutations concurrently.

### Data Transformation

```jsx
const filteredApps = applications.map(app => ({
    id: app._id,
    type: app.documentType.toLowerCase(),
    studentName: app.studentId?.userId?.name || 'N/A',
    rollNo: app.studentId?.rollNo || 'N/A',
    submittedDate: new Date(app.createdAt).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    }),
    status: app.status,
    department: app.studentId?.department || 'N/A',
    semester: app.details?.semester || '',
    remarks: app.approvalDetails?.remarks || []
}));
```

- Transforms raw API data into a format for display.
- Maps fields like `_id` to `id`, lowercases `documentType`, and formats `createdAt` as a readable date.
- Uses optional chaining (`?.`) and fallbacks (`'N/A'`) for missing data.

### Rendering

```jsx
return (
    <div className="p-6">
        ...
    </div>
);
```

- Wraps content in a padded container (`p-6`).

#### Filters

```jsx
<div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
    <div className="flex flex-col md:flex-row gap-4 items-end">
        <div className="flex-1 space-y-1">
            <label className="text-sm text-gray-600">Search by Roll Number</label>
            <input
                type="text"
                placeholder="Enter roll number..."
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                autoFocus
            />
        </div>
        <div className="w-48 space-y-1">
            <label className="text-sm text-gray-600">Document Type</label>
            <select
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500"
                value={filters.type}
                onChange={(e) => setFilters((prev) => ({ ...prev, type: e.target.value }))}
            >
                <option value="all">All Types</option>
                <option value="Bonafide">Bonafide</option>
                <option value="Passport">Passport</option>
            </select>
        </div>
        <div className="w-48 space-y-1">
            <label className="text-sm text-gray-600">Status</label>
            <select
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500"
                value={filters.status}
                onChange={(e) => setFilters((prev) => ({ ...prev, status: e.target.value }))}
            >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
            </select>
        </div>
    </div>
</div>
```

- Renders a filter panel with:
  - A search input for roll number (debounced).
  - A dropdown for document type (`all`, `Bonafide`, `Passport`).
  - A dropdown for status (`all`, `pending`, `approved`, `rejected`).
- Styled with Tailwind: white card (`bg-white p-4 rounded-lg shadow-sm`), responsive flexbox (`md:flex-row`), and focus states (`focus:ring-2 focus:ring-blue-500`).

#### Bulk Actions

```jsx
{selectedItems.length > 0 && (
    <div className="mb-4 p-4 bg-blue-50 border border-blue-100 rounded-lg flex items-center justify-between">
        <span className="text-blue-700">
            Selected: {selectedItems.length} applications
        </span>
        <div className="flex gap-2">
            <button
                onClick={() => handleBulkAction("approve")}
                className="px-4 py-1.5 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center gap-2"
            >
                <FaCheck size={12} /> Approve
            </button>
            <button
                onClick={() => handleBulkAction("reject")}
                className="px-4 py-1.5 bg-red-500 text-white rounded-lg hover:bg-red-600 flex items-center gap-2"
            >
                <FaTimes size={12} /> Reject
            </button>
        </div>
    </div>
)}
```

- Conditionally renders when items are selected.
- Shows the number of selected applications.
- Provides buttons for bulk approval (`bg-green-500`) and rejection (`bg-red-500`), with icons and hover effects.

#### Applications Table

```jsx
<div className="bg-white rounded-lg shadow-sm border border-gray-200">
    <table className="min-w-full divide-y divide-gray-200">
        <thead>
            <tr className="bg-gray-50">
                <th className="w-12 px-4 py-3">
                    <input
                        type="checkbox"
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        onChange={(e) => {
                            setSelectedItems(
                                e.target.checked ? filteredApps.map((app) => app.id) : []
                            );
                        }}
                        checked={selectedItems.length === filteredApps.length && filteredApps.length > 0}
                    />
                </th>
                ...
            </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
            {isLoading ? (
                <tr>
                    <td colSpan="8" className="px-4 py-8 text-center">
                        <div className="flex items-center justify-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                        </div>
                    </td>
                </tr>
            ) : filteredApps.length === 0 ? (
                <tr>
                    <td colSpan="8" className="px-4 py-8 text-center text-gray-500">
                        {searchInput ? `No applications found for roll number "${searchInput}"` : 'No applications found matching the filters.'}
                    </td>
                </tr>
            ) : (
                filteredApps.map((app) => (
                    <tr key={app.id} className="hover:bg-gray-50">
                        ...
                    </tr>
                ))
            )}
        </tbody>
    </table>
</div>
```

- Renders a table with columns for checkbox, type, student, roll number, department, submitted date, status, and actions.
- **Header**:
  - Includes a master checkbox to select/deselect all applications.
  - Styled with `bg-gray-50` and uppercase headers (`text-xs text-gray-500 uppercase`).
- **Body**:
  - **Loading**: Shows a spinner (`animate-spin`).
  - **Empty**: Displays a message, customized for search or general filters.
  - **Data**: Maps `filteredApps` to rows with:
    - Checkbox for selection.
    - Type badge (purple for passport, blue for bonafide).
    - Student name, roll number, department, and formatted date.
    - Status badge (emerald for Approved, rose for Rejected, amber for Pending).
    - Action buttons for view (`FaEye`) and manage (`FaEdit`).

### Export

```jsx
export default ApplicationsList;
```

- Exports the component for use in other parts of the application.

## Styling

- **Tailwind CSS**:
  - **Container**: `p-6` for padding.
  - **Filters**: White card (`bg-white rounded-lg shadow-sm border`), responsive flexbox (`md:flex-row`).
  - **Bulk Actions**: Blue card (`bg-blue-50 border-blue-100`) with green/red buttons.
  - **Table**: White card with borders (`border-gray-200`), hover rows (`hover:bg-gray-50`), and color-coded badges.
  - **Inputs**: Bordered with focus rings (`focus:ring-2 focus:ring-blue-500`).
- **Responsive Design**: Adjusts filter layout and table width for mobile/desktop.

## Assumptions

- **newRequest**: A pre-configured Axios instance.
- **API Endpoints**:
  - `GET /acadAdmin/documents/applications/filter`: Filters applications by `type`, `status`, and `rollNo`.
  - `PATCH /acadAdmin/documents/applications/${id}/status`: Updates status with remarks.
- **Data Structure**: Expects fields like `_id`, `documentType`, `studentId.userId.name`, `status`.
- **Parent Component**: Provides `onSelect` and `onView` callbacks.

## Notes

- **Unused Icon**: `FaFileExport` is imported but not used.
- **Search Debouncing**: Effective but could show a loading indicator during delay.
- **Error Handling**: Robust for mutations, but fetch errors rely on Tanstack Query defaults.
- **Accessibility**: Lacks ARIA attributes for table and checkboxes.

## Future Improvements

- **Remove Unused Import**: Remove `FaFileExport` or add export functionality.
- **Loading Feedback**: Show a loading state for search debounce.
- **Error UI**: Display fetch errors explicitly (e.g., via toast).
- **Accessibility**: Add `aria-label` for buttons, `role="grid"` for table, and keyboard navigation.
- **Sorting**: Allow sorting by columns (e.g., date, status).
- **Pagination**: Add pagination for large datasets.
- **Testing**: Write tests for filtering, bulk actions, and table rendering.