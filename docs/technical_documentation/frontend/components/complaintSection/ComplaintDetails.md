# Title: ComplaintDetails Component 

## Overview

The `ComplaintDetails` component is a React-based interface for displaying comprehensive information about a specific complaint within an educational institution's complaint management system. It provides role-based actions and a detailed view of complaint information including status, contact details, assignment information, and attached images.

## Component Structure

The component is built using React with hooks for state management and React Query for data mutations. It implements a responsive layout with conditional rendering based on the user's role and the complaint's current status.

## Dependencies

```jsx
import React, { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import AssignForm from "./AssignForm";
```

The component relies on:
- React and useState hook for component structure and state management
- React Query's useMutation and useQueryClient for server state mutations
- react-hot-toast for displaying notification messages
- AssignForm component for assigning complaints to support staff

## Props

The component accepts three props:
- `complaint`: Object containing all complaint details
- `onBack`: Callback function to return to the previous screen
- `role`: String representing the user's role in the system

## State Management

```jsx
const [showAssignModal, setShowAssignModal] = useState(false);
const queryClient = useQueryClient();
const [activeImageIndex, setActiveImageIndex] = useState(0);
```

The component maintains several state variables:
- `showAssignModal`: Controls the visibility of the assignment modal
- `queryClient`: Used to invalidate and refetch queries after mutations
- `activeImageIndex`: Tracks the currently displayed image when multiple images are attached

## Data Mutations

The component implements three main mutations:

### Delete Mutation

```jsx
const deleteMutation = useMutation({
    mutationFn: async () => {
        const res = await fetch("http://localhost:8000/api/complaints/delete", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ _id: complaint._id }),
            credentials: "include",
        });

        if (!res.ok) throw new Error("Failed to delete complaint");
    },
    onSuccess: () => {
        toast.success("Complaint deleted");
        onBack(true);
        queryClient.invalidateQueries(["complaints"]);
    },
    onError: (err) => {
        toast.error(err.message);
    },
});
```

This mutation allows students to delete their complaints with appropriate success/error handling.

### Mark as Done Mutation

```jsx
const markAsDoneMutation = useMutation({
    mutationFn: async () => {
        const res = await fetch("http://localhost:8000/api/complaints/admin/updateStatus", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ complaintId: complaint._id, updatedStatus: "Resolved" }),
            credentials: "include",
        });
        if (!res.ok) throw new Error("Failed to mark as done");
    },
    onSuccess: () => {
        toast.success("Marked as resolved");
        onBack(true);
        queryClient.invalidateQueries(["complaints"]);
    },
    onError: (err) => {
        toast.error(err.message);
    },
});
```

This mutation allows administrators to mark complaints as resolved when they're completed.

### Assign Mutation

```jsx
const assignMutation = useMutation({
    mutationFn: async (assignData) => {
        // Create the request body
        const body = {
            complaintId: complaint._id,
            supportStaffId: assignData.supportStaffId || null,
            assignedName: assignData.name,
            assignedContact: assignData.phoneNo,
        };
        
        const res = await fetch("http://localhost:8000/api/complaints/admin/assign", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(body),
            credentials: "include",
        });

        if (!res.ok) {
            const errorData = await res.text();
            throw new Error(`Failed to assign complaint: ${errorData}`);
        }
        
        return await res.json();
    },
    onSuccess: () => {
        toast.success("Complaint assigned successfully");
        onBack(true);
        queryClient.invalidateQueries(["complaints"]);
    },
    onError: (err) => {
        console.error("Assignment error:", err);
        toast.error(err.message);
    },
});
```

This mutation allows administrators to assign complaints to support staff members.

## Event Handlers

```jsx
const handleDelete = (e) => {
    e.preventDefault();
    deleteMutation.mutate();
};

const handleMarkAsDone = (e) => {
    e.preventDefault();
    markAsDoneMutation.mutate();
};

const handleAssign = (assignData) => {
    assignMutation.mutate(assignData);
    setShowAssignModal(false);
};
```

These functions handle user interactions with appropriate mutation calls.

## UI Features

### Status Visualization

The component dynamically generates status indicators with appropriate colors and icons:

```jsx
let statusColor, statusBgColor, statusIcon;
switch (complaint.status) {
    case "Pending":
        statusColor = "text-red-600";
        statusBgColor = "bg-red-50";
        statusIcon = (
            
                
            
        );
        break;
    // Other cases...
}
```

This creates visually distinct indicators for each status:
- **Pending**: Red with a clock icon
- **In Progress**: Yellow with an information icon
- **Resolved**: Green with a checkmark icon

### Image Gallery

For complaints with attached images, the component provides:

```jsx
{complaint.imageUrls && complaint.imageUrls.length > 0 && (
    
        Uploaded Images

        {/* Main image display */}
        
             {
                    e.target.onerror = null;
                    e.target.src = "/complaint_placeholder.jpeg";
                }}
                className="max-h-80 object-contain"
            />
        

        {/* Image thumbnails */}
        {complaint.imageUrls.length > 1 && (
            
                {complaint.imageUrls.map((url, index) => (
                     setActiveImageIndex(index)}
                        className={`cursor-pointer rounded-md overflow-hidden border-2 ${index === activeImageIndex ? "border-blue-500" : "border-transparent"}`}
                    >
                         {
                                e.target.onerror = null;
                                e.target.src = "/complaint_placeholder.jpeg";
                            }}
                            className="h-16 w-16 object-cover"
                        />
                    
                ))}
            
        )}
    
)}
```

This implementation provides:
- A main image display area
- Thumbnail navigation for multiple images
- Active image highlighting
- Fallback handling for missing images

### Role-Based Actions

Different actions are available based on user role and complaint status:

```jsx
{role === "student" && complaint.status !== "Resolved" && (
    
        ...
        Delete
    
)}
{role === "nonAcadAdmin" && complaint.status === "Pending" && (
     setShowAssignModal(true)}
    >
        ...
        Assign
    
)}
{role === "nonAcadAdmin" && complaint.status === "In Progress" && (
    
        ...
        Mark as Resolved
    
)}
```

This conditional rendering ensures:
- Students can delete their complaints (if not resolved)
- Non-Academic Admins can assign pending complaints
- Non-Academic Admins can mark in-progress complaints as resolved

## UI Structure

The component's UI is organized into several sections:

1. **Header**: Contains back button and action buttons
2. **Title and Status**: Displays complaint title and current status
3. **Information Grid**:
   - Complaint details (date, category, subcategory)
   - Contact information (phone, address, availability)
   - Assigned staff information (when applicable)
   - Complaint description
4. **Image Gallery**: Displays attached images with navigation (when applicable)

## Modal Integration

The component integrates with the `AssignForm` component through a modal interface:

```jsx
{showAssignModal && (
     setShowAssignModal(false)}
        onAssign={handleAssign}
        complaint={complaint}
    />
)}
```

This allows administrators to assign complaints to support staff members through a dedicated form interface.

## Usage

This component should be rendered when a user selects a specific complaint to view its details. It requires the complaint object, a callback function to return to the previous screen, and the user's role for proper rendering of role-specific actions.

The component integrates with the broader complaint system by:
1. Displaying comprehensive information about a specific complaint
2. Providing role-based actions for complaint management
3. Supporting image viewing for visual evidence
4. Facilitating the assignment of complaints to support staff
5. Allowing administrators to mark complaints as resolved
