# Title: SupportStaffManagement Component 

## Overview

The `SupportStaffManagement` component is a React-based interface for administrators to manage support staff within an educational institution's complaint management system. It provides comprehensive functionality for adding, viewing, searching, sorting, and deleting support staff members who handle various categories of complaints.

## Component Structure

The component is built using React with hooks for state management and React Query for data fetching. It implements a comprehensive management interface with form validation, search functionality, and sortable tabular data display.

## Dependencies

```jsx
import React, { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
```

The component relies on:
- React and its hooks for component structure and state management
- React Query for data fetching and state synchronization
- A nested `StaffComplaintsModal` component for viewing staff complaint details

## State Management

```jsx
// State for the new support staff form
const [newStaff, setNewStaff] = useState({
    name: "",
    phone: "",
    categories: [],
    subCategories: [],
});

// State for form validation and feedback
const [formError, setFormError] = useState("");
const [successMessage, setSuccessMessage] = useState("");

// Search state
const [searchQuery, setSearchQuery] = useState("");

// Sorting state
const [sortConfig, setSortConfig] = useState({
    key: "name",
    direction: "ascending",
});

// Filtered and sorted staff data
const [displayedStaff, setDisplayedStaff] = useState([]);

// Selected staff for viewing complaints
const [selectedStaff, setSelectedStaff] = useState(null);
```

The component maintains several state variables to control its behavior:
- `newStaff`: Object containing form data for adding a new staff member
- `formError` and `successMessage`: Feedback messages for user actions
- `searchQuery`: Controls the search functionality
- `sortConfig`: Tracks the current sorting configuration (field and direction)
- `displayedStaff`: Derived state containing filtered and sorted staff data
- `selectedStaff`: Tracks the currently selected staff member for viewing complaints

## Predefined Categories

The component includes a predefined structure of categories and subcategories:

```jsx
const categoriesOptions = {
    "Computer & Comm. Centre": ["Automation", "Email Services", "HPC Support", "Network", "PC & Peripherals", "Telephone", "Turnitin", "Web Services", "Other"],
    "Hostel/Resident Complaints": ["Plumbing", "Room Servicing", "Electricity Issues", "Furniture Repair", "Cleaning Services", "Other"],
    "Infrastructure Complaints": ["Gym", "Badminton Hall", "Table Tennis Court", "Ground", "Swimming Pool", "Food Court", "Other"],
};
```

This object maps each main department category to an array of specific issue subcategories, providing a structured approach to staff specialization.

## Data Fetching

The component uses React Query to fetch support staff data:

```jsx
const {
    data: supportStaffData = [],
    isLoading,
    isError,
    refetch,
} = useQuery({
    queryKey: ["supportStaff"],
    queryFn: async () => {
        const response = await fetch("http://localhost:8000/api/complaints/admin/supportStaff", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            credentials: "include",
        });

        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.message || "Failed to fetch support staff");
        }
        return result.supportStaff || [];
    },
});
```

This setup:
- Fetches support staff data from the API
- Handles authentication via Bearer token
- Provides loading and error states
- Offers a refetch function to refresh data after mutations

## Derived State

The component uses `useEffect` to derive the displayed staff list whenever the source data, sorting, or search criteria change:

```jsx
useEffect(() => {
    if (supportStaffData.length) {
        let sortedData = [...supportStaffData];
        
        // Apply sorting
        sortedData.sort((a, b) => {
            // Special case for assignedComplaints length sorting
            if (sortConfig.key === "assignedComplaints") {
                const aLength = a.assignedComplaints ? a.assignedComplaints.length : 0;
                const bLength = b.assignedComplaints ? b.assignedComplaints.length : 0;
                return sortConfig.direction === "ascending" 
                    ? aLength - bLength 
                    : bLength - aLength;
            }
            
            // Special case for resolvedComplaints length sorting
            if (sortConfig.key === "resolvedComplaints") {
                const aLength = a.resolvedComplaints ? a.resolvedComplaints.length : 0;
                const bLength = b.resolvedComplaints ? b.resolvedComplaints.length : 0;
                return sortConfig.direction === "ascending" 
                    ? aLength - bLength 
                    : bLength - aLength;
            }
            
            if (a[sortConfig.key]  b[sortConfig.key]) {
                return sortConfig.direction === "ascending" ? 1 : -1;
            }
            return 0;
        });
        
        // Apply search filter
        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase().trim();
            sortedData = sortedData.filter(staff =>
                staff.name.toLowerCase().includes(query) ||
                staff.phone.includes(query) ||
                (staff.categories && staff.categories.some(category => 
                    category.toLowerCase().includes(query)
                )) ||
                (staff.subCategories && staff.subCategories.some(subCategory => 
                    subCategory.toLowerCase().includes(query)
                ))
            );
        }
        
        setDisplayedStaff(sortedData);
    }
}, [supportStaffData, sortConfig, searchQuery]);
```

This effect:
- Creates a sorted copy of the support staff data
- Implements special handling for sorting by number of assigned or resolved complaints
- Filters the data based on the search query across multiple fields
- Updates the displayed staff list with the processed data

## Data Mutations

### Add Support Staff

```jsx
const handleAddStaff = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!newStaff.name || !newStaff.phone) {
        setFormError("Name and phone number are required.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/complaints/admin/supportStaff", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            credentials: "include",
            body: JSON.stringify(newStaff),
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || "Failed to add support staff");
        }
        
        // Reset form and show success message
        setNewStaff({
            name: "",
            phone: "",
            categories: [],
            subCategories: [],
        });
        setSuccessMessage("Support staff added successfully!");
        setFormError("");
        
        // Refetch the support staff list
        refetch();
        
        // Clear success message after a few seconds
        setTimeout(() => {
            setSuccessMessage("");
        }, 3000);
    } catch (error) {
        setFormError(error.message || "An error occurred while adding support staff");
    }
};
```

This function:
- Validates the form data
- Sends a POST request to create a new support staff member
- Handles success with feedback and form reset
- Triggers a refetch of the staff list
- Provides error handling with user feedback

### Delete Support Staff

```jsx
const handleDeleteStaff = async (staffId) => {
    try {
        const response = await fetch("http://localhost:8000/api/complaints/admin/supportStaff", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            credentials: "include",
            body: JSON.stringify({ supportStaffId: staffId }),
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || "Failed to delete support staff");
        }
        
        // Show success message
        setSuccessMessage("Support staff deleted successfully!");
        
        // Refetch the support staff list
        refetch();
        
        // Clear success message after a few seconds
        setTimeout(() => {
            setSuccessMessage("");
        }, 3000);
    } catch (error) {
        setFormError(error.message || "An error occurred while deleting support staff");
    }
};
```

This function:
- Sends a DELETE request to remove the staff member
- Handles success with feedback
- Triggers a refetch of the staff list
- Provides error handling with user feedback

## Form Handling

### Category Selection

```jsx
const handleCategoryChange = (category) => {
    const updatedCategories = [...newStaff.categories];
    
    // Toggle category selection
    if (updatedCategories.includes(category)) {
        const index = updatedCategories.indexOf(category);
        updatedCategories.splice(index, 1);
    } else {
        updatedCategories.push(category);
    }
    
    setNewStaff({
        ...newStaff,
        categories: updatedCategories,
        // Clear subcategories when categories change
        subCategories: []
    });
};
```

This function:
- Toggles the selection of a category
- Clears subcategories when categories change to maintain data consistency

### Subcategory Selection

```jsx
const handleSubcategoryChange = (subcategory) => {
    const updatedSubcategories = [...newStaff.subCategories];
    
    // Toggle subcategory selection
    if (updatedSubcategories.includes(subcategory)) {
        const index = updatedSubcategories.indexOf(subcategory);
        updatedSubcategories.splice(index, 1);
    } else {
        updatedSubcategories.push(subcategory);
    }
    
    setNewStaff({
        ...newStaff,
        subCategories: updatedSubcategories
    });
};
```

This function toggles the selection of a subcategory in the form.

### Available Subcategories

```jsx
const getAvailableSubcategories = () => {
    let subcategories = [];
    newStaff.categories.forEach(category => {
        if (categoriesOptions[category]) {
            subcategories = [...subcategories, ...categoriesOptions[category]];
        }
    });
    return [...new Set(subcategories)]; // Remove duplicates
};
```

This helper function:
- Collects all subcategories from the selected categories
- Removes duplicates to create a clean list for the form

## Sorting Implementation

```jsx
const requestSort = (key) => {
    let direction = "ascending";
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
        direction = "descending";
    }
    setSortConfig({ key, direction });
};

const getSortDirectionIndicator = (key) => {
    if (sortConfig.key !== key) return null;
    return sortConfig.direction === "ascending" ? "↑" : "↓";
};
```

These functions:
- Toggle sort direction when clicking the same column header
- Provide visual indicators for the current sort direction
- Update the sort configuration which triggers the derived state effect

## Staff Complaints Modal Integration

```jsx
const handleStaffRowClick = (staff) => {
    // Show complaints if the staff has assigned or resolved complaints
    if ((staff.assignedComplaints && staff.assignedComplaints.length > 0) || 
        (staff.resolvedComplaints && staff.resolvedComplaints.length > 0)) {
        setSelectedStaff(staff);
    }
};

// In the render section:
{selectedStaff && (
     setSelectedStaff(null)}
    />
)}
```

This integration:
- Shows the complaints modal when clicking on a staff row with complaints
- Passes the selected staff data to the modal
- Provides a way to close the modal

## UI Structure

The component's UI is organized into several sections:

1. **Header**: Component title
2. **Feedback Messages**: Success and error notifications
3. **Add Staff Form**: Form for adding new support staff
4. **Staff List**: Searchable and sortable table of staff members

### Add Staff Form

The form includes:
- Name and phone number inputs (required)
- Category selection checkboxes
- Dynamic subcategory selection based on chosen categories
- Submit button with validation

### Staff List

The staff list includes:
- Search functionality across multiple fields
- Column sorting with direction indicators
- Staff details including name, phone, categories, and subcategories
- Visual indicators for staff at capacity (5+ assigned complaints)
- Delete action with appropriate disabling for staff with active complaints
- Row click functionality to view staff complaints

## StaffComplaintsModal Component

The component includes a nested `StaffComplaintsModal` component that:
- Fetches and displays complaints assigned to a specific staff member
- Provides tabs to switch between active and resolved complaints
- Shows detailed complaint information including images
- Implements loading and error states
- Provides a close button to return to the staff list

## Usage

This component should be included in the administrative section of the complaint management system, accessible only to users with appropriate permissions. It provides a complete interface for managing the support staff who will be assigned to handle complaints.

The component integrates with the broader complaint system by:
1. Allowing administrators to add staff with specific specializations
2. Showing the current workload of each staff member
3. Preventing deletion of staff with active assignments
4. Providing search and sort capabilities for efficient management
5. Allowing detailed viewing of complaints assigned to each staff member

