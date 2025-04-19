#  PendingComplaints Component 

## Overview

The `PendingComplaints` component is a React-based interface for displaying and managing complaints with a "Pending" status within an educational institution's complaint management system. It is designed for administrative users to monitor and process new complaints that haven't yet been assigned to support staff.

## Component Structure

The component is built using React with hooks for state management and React Query for data fetching. It implements a paginated and searchable list of pending complaints with integration to the `ComplaintList` component for displaying the actual complaint items.

## Dependencies

```jsx
import React, { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import ComplaintList from "../common/ComplaintList";
```

The component relies on:
- React and its hooks for component structure and state management
- React Query for data fetching and state synchronization
- `ComplaintList` component for rendering the complaint items in a consistent format

## Props

```jsx
/**
 * @param {Object} props Component props
 * @param {boolean} props.isLoading - Initial loading state
 * @param {function} props.refetch - Function to refetch all complaint data
 * @param {string} props.role - User role
 */
```

The component accepts several props to control its behavior:
- `isLoading`: Initial loading state passed from the parent component
- `refetch`: Function to refetch all complaint data (used to update counts in the tab bar)
- `role`: User role for permission-based rendering in child components

## State Management

```jsx
const [searchQuery, setSearchQuery] = useState("");
const [selectedComplaint, setSelectedComplaint] = useState(null);

// Pagination state
const [page, setPage] = useState(1);
const [limit, setLimit] = useState(10);
const [pagination, setPagination] = useState(null);
```

The component maintains several state variables:
- `searchQuery`: Controls the search functionality
- `selectedComplaint`: Tracks the currently selected complaint for detailed view
- `page` and `limit`: Control the pagination of complaints
- `pagination`: Stores pagination metadata from the API response

## Data Fetching

The component uses React Query to fetch pending complaints:

```jsx
const {
  data: responseData,
  isLoading,
  refetch
} = useQuery({
  queryKey: ["pendingComplaints", page, limit],
  queryFn: async () => {
    const response = await fetch("http://localhost:8000/api/complaints/admin/status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
      body: JSON.stringify({ 
        status: "Pending",
        page, 
        limit 
      }),
      credentials: "include",
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.message || "Failed to fetch pending complaints");
    }
    return result;
  },
});
```

This setup:
- Fetches complaints with "Pending" status from the API
- Includes pagination parameters in the request
- Uses the access token from localStorage for authentication
- Updates the query when pagination parameters change
- Provides loading state and refetch functionality

## Derived State

The component derives two important pieces of state:

1. Complaints array from the response data:
```jsx
const complaints = responseData?.data || [];
```

2. Filtered complaints based on search query:
```jsx
const filteredComplaints = searchQuery.trim() 
  ? complaints.filter(complaint => {
      const query = searchQuery.toLowerCase().trim();
      const titleMatch = complaint.title?.toLowerCase().includes(query);
      const categoryMatch = complaint.category?.toLowerCase().includes(query);
      const subCategoryMatch = complaint.subCategory?.toLowerCase().includes(query);
      const assigneeMatch = complaint.assignedName?.toLowerCase().includes(query);
      
      return titleMatch || categoryMatch || subCategoryMatch || assigneeMatch;
    })
  : complaints;
```

This filtering logic:
- Only applies when a search query is present
- Searches across multiple fields (title, category, subcategory, assignee)
- Uses case-insensitive matching
- Returns all complaints when no search query is present

## Side Effects

The component uses `useEffect` to update the pagination state when the response data changes:

```jsx
useEffect(() => {
  if (responseData?.pagination) {
    setPagination(responseData.pagination);
  }
}, [responseData]);
```

This ensures that the pagination controls reflect the current state of the data.

## Event Handlers

```jsx
// Handle page change
const handlePageChange = (newPage) => {
  setPage(newPage);
};

// Handle page size change
const handleLimitChange = (newLimit) => {
  setLimit(newLimit);
  setPage(1); // Reset to first page when changing limit
};
```

These functions manage pagination:
- `handlePageChange`: Updates the current page
- `handleLimitChange`: Updates the number of items per page and resets to the first page

## UI Structure

The component's UI is organized into two main sections:

1. **Complaint List**: Renders the `ComplaintList` component with appropriate props
2. **Pagination Controls**: Displays pagination information and navigation buttons

### Complaint List Integration

```jsx
 {
    refetch();  // Refetch the current tab data
    refetchAll(); // Also refetch all data to update counts in the tab bar
  }}
  role={role}
/>
```

The `ComplaintList` component receives:
- The filtered complaints array
- Loading state
- Search query state and setter
- Selected complaint state and setter
- A refetch function that updates both the current tab and the parent component
- The user role for permission-based rendering

### Pagination Controls

The pagination controls are conditionally rendered when pagination data is available:

```jsx
{pagination && (
  
    {/* Items per page selector */}
    
      Items per page:
       handleLimitChange(Number(e.target.value))}
      >
        5
        10
        25
        50
      
      
        Showing {((pagination.currentPage - 1) * pagination.pageSize) + 1} - {Math.min(pagination.currentPage * pagination.pageSize, pagination.totalItems)} of {pagination.totalItems}
      
    
    
    {/* Page navigation buttons */}
    
      {/* Navigation buttons */}
    
  
)}
```

The pagination controls include:
- Items per page selector (5, 10, 25, 50)
- Current range and total items display
- Navigation buttons (first, previous, next, last)
- Current page and total pages indicator
- Responsive layout that stacks on small screens

## Integration with ComplaintDetails

When a user selects a complaint from the list, the `ComplaintList` component renders the `ComplaintDetails` component, which provides:

- Detailed view of the complaint information
- Ability to assign the complaint to support staff (for pending complaints)
- Status visualization with appropriate colors and icons
- Image gallery for attached images

## Usage

This component should be included in the administrative section of the complaint management system, specifically in the tab for viewing pending complaints. It is designed to work within a tabbed interface where administrators can switch between different complaint statuses (Pending, In Progress, Resolved).

The component integrates with the broader complaint system by:
1. Fetching and displaying complaints with "Pending" status
2. Providing search functionality across multiple fields
3. Implementing pagination for efficient data handling
4. Allowing administrators to view complaint details and assign them to support staff
5. Refreshing both its own data and parent component data when changes occur

