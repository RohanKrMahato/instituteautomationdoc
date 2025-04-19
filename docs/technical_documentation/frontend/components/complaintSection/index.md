# ComplaintSection index.js 

## Overview

The `ComplaintSection` component is a React-based interface that serves as the main container for the complaint management system within an educational institution's platform. It provides role-based views and navigation for different user types (students, faculty, and administrators) to manage complaints through various stages of the resolution process.

## Component Structure

The component is built using React with hooks for state management and React Query for data fetching. It implements a tabbed interface that dynamically renders different views based on the user's role and selected tab.

## Dependencies

```jsx
import React, { useContext, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { RoleContext } from "../../context/Rolecontext.jsx";

// Import tab components
import PendingComplaints from "./tabs/PendingComplaints.jsx";
import InProgressComplaints from "./tabs/InProgressComplaints.jsx";
import ResolvedComplaints from "./tabs/ResolvedComplaints.jsx";
import MyComplaints from "./tabs/MyComplaints.jsx";
import NewComplaintSelection from "./tabs/NewComplaintSelection.jsx";
import SupportStaffManagement from "./supportStaff/SupportStaffManagement.jsx";
```

The component relies on:
- React and its hooks for component structure and state management
- React Query for data fetching and state synchronization
- RoleContext for accessing the current user's role
- Various tab components for different views of the complaint system

## Role-Based Access

The component uses the RoleContext to determine the user's role and render appropriate views:

```jsx
const { role } = useContext(RoleContext);
const isStudentOrFaculty = role === "student" || role === "faculty";
const defaultActivePage = isStudentOrFaculty ? "My Complaints" : "Pending";
```

- For students and faculty: Shows "My Complaints" and "New Complaint" tabs
- For administrators: Shows "Pending," "In Progress," "Resolved," and "Support Staff" tabs
- For academic administrators: Returns null (no complaint section is shown)

## State Management

```jsx
const [activePage, setActivePage] = useState(defaultActivePage);

// For student/faculty view
const [page, setPage] = useState(1);
const [limit, setLimit] = useState(10);
```

The component maintains several state variables:
- `activePage`: Tracks the currently selected tab
- `page` and `limit`: Control pagination for student/faculty views

## Data Fetching

The component uses React Query to fetch complaint data:

```jsx
const endpoint = role === "student" || role === "faculty" 
    ? "http://localhost:8000/api/complaints/" 
    : "http://localhost:8000/api/complaints/admin";

const {
    data: responseData,
    isLoading,
    isError,
    refetch,
} = useQuery({
    queryKey: ["complaints", role, isStudentOrFaculty ? page : null, isStudentOrFaculty ? limit : null],
    queryFn: async () => {
        if (isStudentOrFaculty) {
            // For students/faculty, fetch paginated data for "My Complaints"
            // ...
        } else {
            // For admin, fetch a larger dataset for counts
            // ...
        }
    },
});
```

This setup:
- Uses different endpoints based on user role
- Fetches paginated data for students/faculty
- Fetches a larger dataset for administrators to calculate notification counts
- Provides loading and error states
- Includes a refetch function to refresh data

## Derived State

```jsx
const complaintData = responseData?.data || [];
const pagination = responseData?.pagination;
```

The component extracts complaint data and pagination information from the API response.

## Pagination Handlers

```jsx
const handlePageChange = (newPage) => {
    setPage(newPage);
};

const handleLimitChange = (newLimit) => {
    setLimit(newLimit);
    setPage(1); // Reset to first page when changing limit
};
```

These functions manage pagination for student and faculty views.

## UI Structure

The component's UI is organized into two main sections:

1. **Navigation Bar**: Displays tabs appropriate for the user's role with notification badges showing counts
2. **Main Content Area**: Shows the selected tab's content with appropriate loading and error states

### Navigation Bar

```jsx

    
        
            {/* Tab items with notification badges */}
        
    

```

The navigation bar includes:
- Role-specific tabs (My Complaints/Pending, New Complaint/In Progress, etc.)
- Active tab highlighting with blue background
- Notification badges showing counts for each status (red for Pending, yellow for In Progress, green for Resolved)

### Main Content Area

```jsx

    {/* Loading and error states */}
    {/* Conditional rendering of tab components */}

```

The main content area:
- Shows loading spinner during data fetching
- Displays error message when data fetching fails
- Renders the appropriate tab component based on the active page
- Includes pagination controls for student/faculty views

## Tab Components Integration

The component conditionally renders different tab components based on the user's role and selected tab:

### Student/Faculty Views

```jsx
{isStudentOrFaculty && activePage === "My Complaints" && (
    <>
        
        {/* Pagination Controls */}
    
)}

{isStudentOrFaculty && activePage === "New Complaint" && (
    
)}
```

### Administrator Views

```jsx
{!isStudentOrFaculty && activePage === "Pending" && (
    
)}

{!isStudentOrFaculty && activePage === "In Progress" && (
    
)}

{!isStudentOrFaculty && activePage === "Resolved" && (
    
)}

{!isStudentOrFaculty && activePage === "Support Staff" && (
    
)}
```

Each tab component:
- Receives necessary props (complaint data, loading state, refetch function, user role)
- Manages its own specific functionality
- For administrator views, each tab handles its own data fetching and pagination

## Usage

This component serves as the main container for the complaint management system. It should be included in the main application layout for users who need access to the complaint system. It automatically adapts its interface based on the user's role as determined by the `RoleContext`.

The component integrates with the broader application by:
1. Providing role-based access to complaint management features
2. Displaying notification counts for different complaint statuses
3. Facilitating navigation between different views of the complaint system
4. Handling data fetching and state management for the overall complaint section

