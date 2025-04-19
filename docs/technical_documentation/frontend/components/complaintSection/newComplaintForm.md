#  NewComplaintForm Component 

## Overview

The `NewComplaintForm` component is a React-based form interface for submitting new complaints within an educational institution's complaint management system. It provides a comprehensive form with validation, file uploads, and real-time feedback to users.

## Component Structure

The component is built using React with hooks for state management and side effects. It integrates with React Query for data mutations and includes features like drag-and-drop file uploads and form validation.

## Dependencies

```jsx
import React, { useState, useRef, useEffect } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import convertImageToBase64 from "../../utils/convertImageToBase64";
```

- React and its hooks for component structure and state management
- React Query for handling data mutations
- react-hot-toast for displaying notification messages
- A utility function to convert images to base64 format for submission

## Props

The component accepts the following props:

- `category`: The main category of the complaint
- `subCategory`: The specific subcategory of the complaint
- `onBack`: Callback function to return to the previous screen

## State Management

```jsx
const [title, setTitle] = useState("");
const [complaint, setComplaint] = useState("");
const [phoneNumber, setPhoneNumber] = useState("");
const [timeAvailability, setTimeAvailability] = useState("");
const [locality, setLocality] = useState("");
const [detailedAddress, setDetailedAddress] = useState("");
const [files, setFiles] = useState([]);
const [isSubmitting, setIsSubmitting] = useState(false);
const [characterCount, setCharacterCount] = useState(0);
const [isDragging, setIsDragging] = useState(false);
```

The component maintains several state variables to track form inputs, file uploads, and UI states:

- Form field states for each input
- Files array for tracking uploaded images
- Submission state for disabling controls during submission
- Character count for the description field
- Drag state for the file upload area

## Refs

```jsx
const fileInputRef = useRef(null);
const dropZoneRef = useRef(null);
const dragCounter = useRef(0);
```

- `fileInputRef`: References the hidden file input element
- `dropZoneRef`: References the drop zone area for drag-and-drop
- `dragCounter`: Tracks drag events to handle nested elements

## Data Mutation

The component uses React Query's mutation hook to handle form submission:

```jsx
const mutation = useMutation({
    mutationFn: submitComplaint,
    onSuccess: () => {
        toast.success("Complaint submitted successfully!");
        handleClear();
        queryClient.invalidateQueries(["complaints"]);
    },
    onError: (err) => {
        toast.error(`Error: ${err.message}`);
    },
    onSettled: () => {
        setIsSubmitting(false);
    }
});
```

This setup:
- Calls the `submitComplaint` function when triggered
- Shows success toast and clears the form on success
- Invalidates the complaints query to refresh the list
- Shows error toast on failure
- Resets the submitting state when completed

## Form Submission

```jsx
const submitComplaint = async (formData) => {
    const accessToken = localStorage.getItem("accessToken");
    const res = await fetch("http://localhost:8000/api/complaints/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            authorization: `${accessToken}`,
        },
        body: JSON.stringify(formData),
        credentials: "include",
    });

    const data = await res.json();
    if (!res.ok) {
        throw new Error(data?.message || "Failed to submit complaint");
    }
    onBack(); // Call the onBack function to navigate back to the previous page
    return data;
};
```

The submission function:
- Retrieves the authentication token
- Makes a POST request to the complaints creation endpoint
- Handles response validation
- Navigates back on success or throws an error

## Form Validation

The component implements several validation checks before submission:

```jsx
// Basic validation for required fields
if (!title || !complaint || !phoneNumber || !timeAvailability || !locality || !detailedAddress) {
    toast.error("All fields are required!");
    setIsSubmitting(false);
    return;
}

// Phone number validation
const phoneRegex = /^\+?\d{1,4}[\s-]?\d{10}$/;
if (!phoneRegex.test(phoneNumber)) {
    toast.error("Please enter a valid phone number (e.g., +91 9876543210)");
    setIsSubmitting(false);
    return;
}
```

These validations ensure:
- All required fields are filled
- Phone number follows the expected format
- Time availability is selected

## File Upload Handling

The component supports both traditional file input and drag-and-drop for image uploads:

```jsx
const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    processFiles(newFiles);
};

const processFiles = (newFiles) => {
    // Filter valid formats and size ( /\.(jpe?g)$/i.test(file.name) && file.size  !(/\.(jpe?g)$/i.test(file.name) && file.size  0) {
        toast.error("Some files were rejected. Make sure they are JPG format and under 200KB.");
    }
    
    if (files.length + validFiles.length > 5) {
        toast.error("You can only upload a maximum of 5 files.");
        return;
    }
    
    setFiles((prevFiles) => [...prevFiles, ...validFiles]);
};
```

This implementation:
- Accepts files from input or drop events
- Validates file format (JPG only) and size (max 200KB)
- Limits the total number of files to 5
- Provides error feedback for invalid files

## Drag and Drop Implementation

```jsx
const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current++;
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
        setIsDragging(true);
    }
};

const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current--;
    if (dragCounter.current === 0) {
        setIsDragging(false);
    }
};

const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragging) {
        setIsDragging(true);
    }
};

const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    dragCounter.current = 0;
    
    // Get the dropped files
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        const droppedFiles = Array.from(e.dataTransfer.files);
        processFiles(droppedFiles);
        e.dataTransfer.clearData();
    }
};
```

This implementation:
- Prevents default browser behavior for drag events
- Uses a counter to handle nested elements
- Updates the UI state to show active dragging
- Processes dropped files through the same validation as the file input

## UI Features

### Character Counter

```jsx
const handleDescriptionChange = (e) => {
    const text = e.target.value;
    setCharacterCount(text.length);
    setComplaint(text);
};
```

This feature:
- Tracks the number of characters in the description
- Changes color when approaching the limit (400 characters)
- Provides visual feedback to the user

### Image Preview

```jsx
{files.length > 0 && (
    
        Uploaded Images ({files.length}/5):
        
            {files.map((file, index) => (
                
                    
                        
                    
                     removeFile(index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 focus:outline-none"
                    >
                        
                            
                        
                    
                    
                        {file.name} ({(file.size / 1024).toFixed(1)} KB)
                    
                
            ))}
        
    
)}
```

This section:
- Displays previews of uploaded images in a grid
- Shows file name and size information
- Provides a remove button for each image
- Indicates the current count out of the maximum allowed

## Form Structure

The form is organized into several sections:

1. **Header**: Shows the form title and selected category/subcategory
2. **Title and Description**: Input fields for the complaint title and detailed description
3. **Contact Information**: Fields for phone number and preferred visit time
4. **Location**: Dropdown for locality and text area for detailed address
5. **Image Upload**: Drag-and-drop area and file input for image attachments
6. **Image Preview**: Grid display of uploaded images with remove functionality
7. **Action Buttons**: Submit and Clear buttons with appropriate states

## Usage

This component should be rendered when a user selects a category and subcategory for a new complaint. It handles the entire submission process, including form validation, file uploads, and API interaction.
