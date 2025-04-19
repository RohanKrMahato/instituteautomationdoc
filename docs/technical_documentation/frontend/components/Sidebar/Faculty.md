# Faculty Component 

## Overview
The `Faculty` component renders a sidebar navigation menu for faculty members in an educational application. The menu includes expandable sections for Course management, Complaints, and Profile, with various suboptions that link to different pages within the application.

## Component Structure

### Imports
```jsx
import React, { useState } from 'react';
import { IoMdArrowDropright } from "react-icons/io";
import { IoMdArrowDropdown } from "react-icons/io";
import { Link } from 'react-router-dom';
```

- **React, useState**: Core React library and state management hook
- **IoMdArrowDropright, IoMdArrowDropdown**: Icons from React Icons library for collapsed/expanded indicators
- **Link**: React Router component for navigation without page reloads

### State Management
```jsx
const [expandedSections, setExpandedSections] = useState({
    course: false,
    complaint: false,
    profile: false
});
```

The component uses a single state object to track which sections are expanded. Each key corresponds to a section name, with boolean values indicating expansion state:
- `course`: Controls visibility of course-related options
- `complaint`: Controls visibility of complaint-related options
- `profile`: Controls visibility of profile-related options

### Toggle Function
```jsx
const toggleSection = (section) => {
    setExpandedSections(prev => ({
        ...prev,
        [section]: !prev[section]
    }));
};
```

This function takes a section name and toggles its expansion state while preserving the state of other sections:
1. Uses functional state update pattern with previous state
2. Creates a new object with all existing properties via spread operator
3. Overrides the specific section's value with its opposite (true → false or false → true)

### JSX Structure
The component returns a hierarchical unordered list structure:
- Root `<ul>` contains three main sections
- Each section has:
  - A clickable header with toggle functionality
  - An icon that changes based on expansion state
  - A nested `<ul>` that renders conditionally when expanded
  - Various `<Link>` components pointing to different routes

### Navigation Options

#### Course Section
When expanded, displays:
- Registration (`/facultyregistration`)
- Feedback (`/feedbackReports`)
- Attendance Tracking (`/attendancelanding`)
- Grades Submission (no link provided)
- Assignment (`/assignmentlanding`)

#### Complaint Section
When expanded, displays:
- Complaint Form (`/complaint`)

#### Profile Section
When expanded, displays:
- View Profile (`/profile`)

## Implementation Details

### Conditional Rendering
```jsx
{expandedSections.course && (
    <ul className="pl-5">
        {/* List items */}
    </ul>
)}
```

The component uses the logical AND (`&&`) operator for conditional rendering of subsections. When `expandedSections.course` is `true`, the JSX after `&&` renders; otherwise, nothing renders.

### Icon Toggle
```jsx
{expandedSections.course ? <IoMdArrowDropdown /> : <IoMdArrowDropright />}
```

A ternary operator switches between dropdown and right-pointing arrow icons based on the section's expansion state.

### Styling
- The component uses Tailwind CSS classes for styling:
  - `list-none`: Removes default list bullets
  - `pl-5`: Adds left padding (5 units)
  - `mt-5`: Adds top margin (5 units)
  - `font-bold`: Makes text bold
  - `cursor-pointer`: Changes cursor to pointer on hover
  - `flex items-center`: Uses flexbox for alignment
  - `text-gray-700`, `hover:text-gray-900`: Text color management

## Usage
This component should be imported and placed within a layout that has React Router configured. It's typically used in a sidebar or navigation panel of the faculty portal.

