#  MyComplaints Component 

## Overview

The `MyComplaints` component is a React-based interface for displaying all complaints submitted by students and faculty members within an educational institution's complaint management system. It serves as a personal dashboard where users can view, search, and manage their submitted complaints.

## Component Structure

The component is built using React with hooks for state management and side effects. It acts as a wrapper around the `ComplaintList` component, providing filtering and search functionality specific to the current user's complaints.

## Dependencies

```jsx
import React, { useState, useEffect } from "react";
import ComplaintList from "../common/ComplaintList";
```

- React and its hooks for component structure and state management
- `ComplaintList` component for rendering the actual complaint items in a consistent format

## Props

```jsx
/**
 * @param {Object} props Component props
 * @param {Array} props.complaintData - Full array of complaint data
 * @param {boolean} props.isLoading - Loading state
 * @param {function} props.refetch - Function to refetch complaint data
 * @param {string} props.role - User role (student or faculty)
 */
```

The component accepts several props to control its behavior:
- `complaintData`: Array of complaints belonging to the current user
- `isLoading`: Boolean indicating if data is being loaded
- `refetch`: Function to reload complaint data after changes
- `role`: User role (student or faculty) for permission-based rendering

## State Management

```jsx
const [filteredComplaints, setFilteredComplaints] = useState([]);
const [searchQuery, setSearchQuery] = useState("");
const [selectedComplaint, setSelectedComplaint] = useState(null);
```

The component maintains three state variables:
- `filteredComplaints`: Stores the filtered list of complaints based on search criteria
- `searchQuery`: Controls the search functionality
- `selectedComplaint`: Tracks the currently selected complaint for detailed view

## Side Effects

The component uses `useEffect` to filter complaints whenever the source data or search query changes:

```jsx
useEffect(() => {
  if (complaintData) {
    let filtered = [...complaintData]; // For student/faculty, we show all their complaints
    
    // Apply search filter if there's a search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(complaint => {
        const titleMatch = complaint.title?.toLowerCase().includes(query);
        const categoryMatch = complaint.category?.toLowerCase().includes(query);
        const subCategoryMatch = complaint.subCategory?.toLowerCase().includes(query);
        const statusMatch = complaint.status?.toLowerCase().includes(query);
        
        return titleMatch || categoryMatch || subCategoryMatch || statusMatch;
      });
    }
    
    setFilteredComplaints(filtered);
  }
}, [complaintData, searchQuery]);
```

This effect:
- Creates a copy of the complaint data
- Applies search filtering when a query is present
- Searches across multiple fields (title, category, subcategory, status)
- Uses case-insensitive matching
- Updates the filtered complaints state

## Search Implementation

The search functionality allows users to filter their complaints by:
- Complaint title
- Category
- Subcategory
- Status (Pending, In Progress, Resolved)

The search is performed in real-time as the user types, providing immediate feedback.

## Integration with ComplaintList

```jsx
return (
  
);
```

The component renders the `ComplaintList` component with all necessary props:
- The filtered complaints array
- Loading state
- Search query state and setter
- Selected complaint state and setter
- Refetch function for data updates
- User role for permission-based rendering

## Differences from Admin Views

Unlike the admin-focused complaint views (PendingComplaints, InProgressComplaints, ResolvedComplaints), the MyComplaints component:
- Shows all complaints for the current user regardless of status
- Does not implement pagination (assumes a manageable number of complaints per user)
- Filters on the client side rather than making new API requests
- Includes status as a searchable field

## Usage

This component should be included in the student and faculty views of the complaint management system. It provides users with a complete view of all their submitted complaints, allowing them to:
1. Search through their complaints using various criteria
2. View detailed information about specific complaints
3. Track the status of their complaints
4. Delete their complaints if needed (via the ComplaintDetails component)

The component integrates with the broader complaint system by:
1. Displaying complaints submitted by the current user
2. Providing search functionality across multiple fields
3. Allowing users to view complaint details
4. Refreshing data when changes occur (e.g., after deleting a complaint)
