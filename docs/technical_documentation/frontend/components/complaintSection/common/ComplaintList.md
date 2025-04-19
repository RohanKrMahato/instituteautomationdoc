# ComplaintList Component 

## Overview

The `ComplaintList` component is a React-based interface for displaying and filtering complaints within an educational institution's complaint management system. It provides a searchable list of complaints with detailed cards and integrates with the `ComplaintDetails` component for viewing individual complaints.

## Component Structure

The component is built using React with functional components and props for data and event handling. It implements a responsive design with search functionality and conditional rendering based on the selected complaint state.

## Props

```jsx
/**
 * @param {Object} props Component props
 * @param {Array} props.complaints - Array of complaints to display
 * @param {boolean} props.isLoading - Loading state
 * @param {string} props.searchQuery - Current search query
 * @param {function} props.setSearchQuery - Function to update search query
 * @param {Object|null} props.selectedComplaint - Currently selected complaint for details view
 * @param {function} props.setSelectedComplaint - Function to set selected complaint
 * @param {function} props.refetch - Function to refetch complaints data
 * @param {string} props.role - User role
 */
```

The component accepts several props to control its behavior:
- `complaints`: The array of complaint objects to display
- `isLoading`: Boolean indicating if data is being loaded
- `searchQuery` and `setSearchQuery`: State and setter for the search functionality
- `selectedComplaint` and `setSelectedComplaint`: State and setter for the currently viewed complaint
- `refetch`: Function to reload complaint data after changes
- `role`: User role for permission-based rendering

## Event Handlers

```jsx
/**
 * Sets the selected complaint for viewing details.
 * @param {object} complaint - The complaint to view.
 */
const handleViewDetails = (complaint) => {
  setSelectedComplaint(complaint);
};

/**
 * Handles the back action from the complaint details view.
 * @param {boolean} wasDeleted - Indicates if the complaint was deleted.
 */
const handleBackFromDetails = (wasDeleted) => {
  setSelectedComplaint(null);
  if (wasDeleted) {
    refetch();
  }
};
```

These functions manage:
- Selecting a complaint to view its details
- Returning from the details view to the list view
- Refreshing data if a complaint was deleted

## Conditional Rendering

The component implements conditional rendering based on the selected complaint state:

```jsx
// If a complaint is selected, show its details
if (selectedComplaint) {
  return (
    
  );
}
```

When a complaint is selected, the component renders the `ComplaintDetails` component instead of the list view, passing the necessary props for displaying the complaint details and handling the back action.

## Search Implementation

The component includes a search input with real-time filtering:

```jsx
 setSearchQuery(e.target.value)}
/>
```

The search input:
- Updates the `searchQuery` state as the user types
- Includes a clear button when text is entered
- Shows the number of results found for the current query

The actual filtering logic is implemented in the parent component, which passes the filtered complaints array to this component.

## Complaint Cards

Each complaint is displayed as a card with key information:

```jsx

  {complaints.map((complaint) => {
    // Determine status color based on status
    let statusColor = "gray";
    if (complaint.status === "Pending") statusColor = "red";
    else if (complaint.status === "In Progress") statusColor = "yellow";
    else if (complaint.status === "Resolved") statusColor = "green";

    return (
      
        {/* Card content */}
      
    );
  })}

```

Each card includes:
- Complaint title and status with appropriate color coding
- Date, category, and subcategory information
- Assignment details when applicable
- A truncated description with a 2-line limit
- A "View Details" button to see the full complaint

## Empty State Handling

The component handles the case when no complaints match the search criteria:

```jsx
!isLoading && (
  
    
      
    
    No complaints found.
    Try adjusting your search criteria.
  
)
```

This provides a user-friendly message when no results are found, with a suggestion to adjust the search criteria.

## Integration with Parent Components

This component is designed to work within a larger complaint management system:
- It receives filtered complaints from the parent component
- It communicates with the parent when a complaint is selected or when returning from details view
- It triggers data refetching when necessary (e.g., after deletion)

## Styling

The component uses Tailwind CSS for styling:
- Responsive grid layout for complaint cards
- Shadow effects with hover transitions
- Color-coded status indicators
- Line clamping for description text
- Icon integration for search and view details

## Usage

This component should be used within a parent component that:
1. Fetches and manages complaint data
2. Implements the filtering logic based on search queries
3. Provides the necessary state management for selected complaints
4. Handles data refetching when needed

The component handles the presentation and user interaction aspects of the complaint list, while delegating data management to its parent.

