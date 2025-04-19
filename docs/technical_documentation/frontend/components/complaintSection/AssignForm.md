# AssignForm Component

## Overview

The `AssignForm` component is a React modal interface used within the complaint management system to assign complaints to support staff members. It provides administrators with a filtered list of support staff based on the complaint's category and subcategory, allowing for appropriate assignment of complaints to qualified personnel.

## Component Structure

The component is built using React with hooks for state management and side effects. It implements a modal dialog that overlays the main application, focusing the user's attention on the assignment task.

## Dependencies

```jsx
import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";
```

- React and its hooks (useState, useEffect) for component structure and lifecycle management
- react-hot-toast for displaying notification messages

## Props

The component accepts the following props:

- `onClose`: Callback function to close the modal
- `onAssign`: Callback function to handle the assignment action
- `complaint`: Object containing complaint details, including category and subcategory

## State Management

```jsx
const [selectedStaffId, setSelectedStaffId] = useState("");
const [supportStaff, setSupportStaff] = useState([]);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
```

- `selectedStaffId`: Tracks the ID of the selected support staff member
- `supportStaff`: Stores the list of available support staff members
- `isLoading`: Indicates when data is being fetched
- `error`: Stores any error messages during data fetching

## Data Fetching

The component uses the `useEffect` hook to fetch support staff data when the component mounts or when the complaint's category or subcategory changes:

```jsx
useEffect(() => {
    const fetchSupportStaff = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem("accessToken");
            const response = await fetch(`http://localhost:8000/api/complaints/admin/filteredSupportStaff?category=${complaint.category}&subCategory=${complaint.subCategory}`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error("Failed to fetch support staff");
            }

            const data = await response.json();
            setSupportStaff(data.supportStaff || []);
            setSelectedStaffId("");
        } catch (error) {
            console.error("Error fetching support staff:", error);
            setError("Failed to load support staff. Please try again.");
            toast.error("Failed to load support staff");
        } finally {
            setIsLoading(false);
        }
    };

    if (complaint?.category && complaint?.subCategory) {
        fetchSupportStaff();
    }
}, [complaint?.category, complaint?.subCategory]);
```

This function:
- Sets loading state and clears any previous errors
- Retrieves the authentication token from localStorage
- Makes an API request to fetch support staff filtered by the complaint's category and subcategory
- Updates the component state with the fetched data or error information
- Displays toast notifications for errors

## Event Handlers

```jsx
const handleStaffSelect = (staff) => {
    setSelectedStaffId(staff._id);
};

const handleAssign = async (e) => {
    e.preventDefault();
    if (!selectedStaffId) {
        toast.error("Please select a staff member to assign!");
        return;
    }

    const selectedStaff = supportStaff.find((staff) => staff._id === selectedStaffId);

    if (!selectedStaff) {
        toast.error("Selected staff not found. Please try again.");
        return;
    }

    const assignData = {
        complaintId: complaint._id,
        name: selectedStaff.name,
        phoneNo: selectedStaff.phone,
        supportStaffId: selectedStaffId,
    };

    console.log("Assigning to:", assignData);
    onAssign(assignData);
};
```

These functions handle:
- Selecting a staff member from the list
- Form submission validation
- Creating the assignment data object
- Calling the parent component's `onAssign` callback with the prepared data

## UI Structure

The component's UI is organized into several sections:

1. **Modal Container**: A fixed-position overlay that covers the entire screen
2. **Modal Content**: A white card containing the assignment interface
3. **Complaint Details**: Displays the category and subcategory of the complaint
4. **Staff Selection**: Lists available support staff with their current workload
5. **Action Buttons**: Cancel and Assign buttons to complete or abort the operation

## Loading and Error States

The component handles three main states:

1. **Loading**: Displays a spinning animation while fetching data
2. **Error**: Shows an error message if staff data couldn't be loaded
3. **Empty Results**: Displays a message when no matching staff are found

## Staff Selection Interface

```jsx

    {supportStaff.map((staff) => {
        const assignedCount = staff.assignedComplaints?.length || 0;
        return (
             handleStaffSelect(staff)}
            >
                
                    {staff.name}
                    
                        {assignedCount} {assignedCount === 1 ? "complaint" : "complaints"}
                    
                
                {staff.phone}
            
        );
    })}

```

This section:
- Creates a scrollable list of staff members
- Shows each staff member's name and phone number
- Displays the number of complaints currently assigned to each staff member
- Highlights the selected staff member with a blue background
- Provides visual feedback on hover

## Form Submission

```jsx

    
        
            Cancel
        
        
            {isLoading ? "Assigning..." : "Assign"}
        
    

```

The form:
- Calls `handleAssign` on submission
- Provides a Cancel button to close the modal
- Includes an Assign button that is disabled when loading or when no staff is selected
- Shows dynamic button text based on the loading state

## Integration with Parent Component

This component is designed to work with the `ComplaintDetails` component, which renders it as a modal when the "Assign" button is clicked. The parent component passes the necessary props:

```jsx
{showAssignModal && (
     setShowAssignModal(false)}
        onAssign={handleAssign}
        complaint={complaint}
    />
)}
```

When a staff member is selected and the form is submitted, the `onAssign` callback is triggered, which in turn calls the `assignMutation.mutate()` function in the parent component to perform the actual API request.

## Usage

This component should be rendered conditionally when an administrator needs to assign a complaint to a support staff member. It requires the complaint object, a callback function to handle the assignment, and a callback function to close the modal.

