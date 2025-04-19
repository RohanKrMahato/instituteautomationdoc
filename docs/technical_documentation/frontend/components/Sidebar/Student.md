# Student Component
## Overview
The `Student` component is a navigation sidebar specifically designed for student users in an educational management system. It provides an expandable/collapsible menu structure with multiple sections for accessing various student-related features.

## Component Structure

### Imports
```jsx
import React, { useState } from 'react';
import { IoMdArrowDropright } from "react-icons/io";
import { IoMdArrowDropdown } from "react-icons/io";
import { Link } from 'react-router-dom';
```

- React and useState for component creation and state management
- Arrow icons from React Icons library for visual indication of expanded/collapsed states
- Link from React Router for navigation without page reloads

### State Management
```jsx
const [expandedSections, setExpandedSections] = useState({
    course: false,
    activeCourses: false,
    feepayment: false,
    document: false,
    hostel: false,
    complaint: false,
    profile: false
});
```

A single state object tracks the expansion state of each navigation section, all initially collapsed.

### Toggle Function
```jsx
const toggleSection = (section) => {
    setExpandedSections(prev => ({
        ...prev,
        [section]: !prev[section]
    }));
};
```

This function toggles a specific section's expanded/collapsed state while preserving other sections' states.

### Key Features

1. **Nested Navigation Structure**:
   - Main sections: Course, Fee Payment, Document, Hostel, Complaint, Profile
   - Nested subsection: Active Courses (under Course) with its own expandable options

2. **Hierarchical Menu**:
   - Primary sections at the top level
   - Secondary options within expanded sections
   - Tertiary options within expanded subsections (e.g., within Active Courses)

3. **Visual Indicators**:
   - Arrow icons change direction based on expansion state
   - Consistent styling for all menu levels

## Navigation Sections

### Course Section
- Registration (/registration)
- Active Courses (/courses) - Expandable subsection with:
  - Assignment (/assignmentlanding)
  - Attendance (/attendancelanding)
  - Time Table (/timetable)
  - Drop Course (/dropcourse)
  - Feedback (/courseFeedback)

### Fee Payment Section
- Pay Fee (/feepayment)

### Document Section
- All Documents (/documents)
- Transcript (/documents/transcript)
- ID Card (/documents/idcard)
- Passport (/documents/passport)
- Bonafide (/documents/bonafide)
- Fee Receipt (/documents/feereceipt)
- Other Forms (/documents/othersform)

### Hostel Section
- Leave (/hostel/leave)
- Mess (/hostel/mess)
- Transfer (/hostel/transfer)

### Complaint Section
- Complaint Form (/complaint)

### Profile Section
- View Profile (/profile)

## Implementation Notes

- Uses conditional rendering with `&&` operator for showing/hiding expanded sections
- Applies consistent Tailwind CSS styling throughout
- Employs a unified toggle mechanism across all sections
- Handles both single-level and multi-level navigation hierarchies