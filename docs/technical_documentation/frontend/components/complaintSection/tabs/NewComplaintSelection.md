#  NewComplaintSelection Component 

## Overview

The `NewComplaintSelection` component is a React-based interface that serves as the first step in the complaint submission process within an educational institution's complaint management system. It provides a user-friendly interface for selecting the department and issue category before proceeding to the detailed complaint form.

## Component Structure

The component is built using React with hooks for state management and conditional rendering. It acts as a gateway to the `NewComplaintForm` component, ensuring that users properly categorize their complaints before submission.

## Dependencies

```jsx
import React, { useState } from "react";
import NewComplaintForm from "../newComplaintForm";
```

- React and useState hook for component structure and state management
- `NewComplaintForm` component for rendering the detailed complaint form after category selection

## Props

```jsx
/**
 * @param {Object} props Component props
 * @param {function} props.refetch - Function to refetch complaints data after creation
 */
```

The component accepts a single prop:
- `refetch`: Function to reload complaint data after a new complaint is successfully submitted

## State Management

```jsx
const [category, setCategory] = useState("Computer & Comm. Centre");
const [subCategory, setSubCategory] = useState("");
const [showNewComplaintForm, setShowNewComplaintForm] = useState(false);
```

The component maintains three state variables:
- `category`: Stores the selected department (main category)
- `subCategory`: Stores the selected issue category (subcategory)
- `showNewComplaintForm`: Controls whether to show the category selection or the detailed complaint form

## Predefined Categories

The component includes a predefined structure of categories and subcategories:

```jsx
const categories = {
  "Computer & Comm. Centre": ["Automation", "Email Services", "HPC Support", "Network", "PC & Peripherals", "Telephone", "Turnitin", "Web Services", "Other"],
  "Hostel/Resident Complaints": ["Plumbing", "Room Servicing", "Electricity Issues", "Furniture Repair", "Cleaning Services", "Other"],
  "Infrastructure Complaints": ["Gym", "Badminton Hall", "Table Tennis Court", "Ground", "Swimming Pool", "Food Court", "Other"],
};
```

This object maps each main department category to an array of specific issue subcategories, providing a structured approach to complaint categorization.

## Event Handlers

```jsx
/**
 * Handles the continue button click to show the complaint form
 */
const handleGoClick = () => {
  setShowNewComplaintForm(true);
};

/**
 * Handles the back action from the complaint form
 * @param {boolean} wasNewAdded - Whether a new complaint was added
 */
const handleBackClick = (wasNewAdded) => {
  setShowNewComplaintForm(false);
  if (wasNewAdded) {
    refetch();
  }
};
```

These functions manage:
- Transitioning from category selection to the detailed complaint form
- Returning from the complaint form to the category selection
- Triggering data refetch when a new complaint has been successfully added

## Conditional Rendering

The component implements conditional rendering based on the `showNewComplaintForm` state:

```jsx
if (showNewComplaintForm) {
  return (
    
       handleBackClick(false)}
      >
        
          
        
        Back
      
       handleBackClick(true)}
      />
    
  );
}
```

When a user has selected categories and clicked "Continue":
- The component renders the `NewComplaintForm` component
- It passes the selected category and subcategory as props
- It provides a back button to return to the selection screen
- It passes an onBack handler that indicates successful submission

## Selection Interface

When `showNewComplaintForm` is false, the component renders a selection interface:

```jsx
return (
  
    Register New Complaint
    
    
      {/* Department selection dropdown */}
      
        Department
        
           {
              setCategory(e.target.value);
              setSubCategory("");
            }}
          >
            {Object.keys(categories).map((cat) => (
              {cat}
            ))}
          
          {/* Custom dropdown arrow */}
        
      
      
      {/* Issue category selection dropdown */}
      
        Issue Category
        
           setSubCategory(e.target.value)}
          >
            --Select Category--
            {categories[category]?.map((cat) => (
              {cat}
            ))}
          
          {/* Custom dropdown arrow */}
        
      
      
      {/* Continue button */}
      
        
          Continue
          
            
          
        
      
    
  
);
```

This interface includes:
- A department (main category) dropdown that automatically resets the subcategory when changed
- A subcategory dropdown that dynamically updates based on the selected department
- A Continue button that is disabled until a subcategory is selected
- Visual feedback through button styling to indicate when the form is ready to proceed

## User Experience Features

The component implements several UX enhancements:

1. **Default Selection**: Pre-selects "Computer & Comm. Centre" as the default department
2. **Cascading Dropdowns**: Updates subcategory options based on the selected department
3. **Validation**: Disables the Continue button until a subcategory is selected
4. **Visual Feedback**: Changes button styling based on form completeness
5. **Back Navigation**: Provides a clear way to return to the selection screen from the form
6. **Custom Dropdown Styling**: Includes custom dropdown arrows for a consistent look

## Integration with NewComplaintForm

When a user proceeds to the complaint form, this component:
1. Passes the selected category and subcategory to `NewComplaintForm`
2. Provides a callback for the form to indicate successful submission
3. Handles refetching data when a new complaint is added

## Usage

This component should be included in the student and faculty views of the complaint management system as the entry point for creating new complaints. It ensures that complaints are properly categorized before submission, which helps in:

1. Routing complaints to the appropriate department
2. Assigning complaints to qualified support staff
3. Generating meaningful statistics about complaint categories
4. Providing a structured approach to complaint management

