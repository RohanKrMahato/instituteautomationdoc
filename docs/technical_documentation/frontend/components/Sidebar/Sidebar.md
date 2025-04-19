# Sidebar Component 

## Overview
The `Sidebar` component is a responsive navigation sidebar that dynamically renders different navigation options based on the user's role. It supports collapsing and expanding functionality and integrates with a context-based role management system.

## Component Structure

### Imports
```jsx
import React, { useContext, useState } from 'react';
import { IoMenuOutline } from "react-icons/io5";
import Student from './Student';
import Faculty from './Faculty';
import AcadAdmin from './AcadAdmin';
import HostelAdmin from './HostelAdmin';
import { RoleContext } from '../../context/Rolecontext';
```

- **React, useContext, useState**: Core React library and hooks for state and context management
- **IoMenuOutline**: Icon component from React Icons library for the hamburger menu
- **Student, Faculty, AcadAdmin, HostelAdmin**: Role-specific navigation components
- **RoleContext**: Custom context for accessing the user's role

### State Management
```jsx
const [isOpen, setIsOpen] = useState(true);
```

The component uses a boolean state to track whether the sidebar is expanded or collapsed:
- `isOpen: true` → Sidebar is expanded and visible
- `isOpen: false` → Sidebar is collapsed, showing only a hamburger icon

### Context Usage
```jsx
const { role } = useContext(RoleContext);
```

The component consumes the `RoleContext` to access the current user's role, which determines which navigation component to render.

### JSX Structure
The component's JSX is divided into two main conditional sections:

1. **Collapsed State** (when `isOpen` is `false`):
   - Renders only a hamburger menu button
   - Clicking this button expands the sidebar

2. **Expanded State** (when `isOpen` is `true`):
   - Renders a full width sidebar with close button
   - Dynamically renders the appropriate role-based navigation component

### Role-Based Rendering
```jsx
{role === "student" && <Student />}
{role === "faculty" && <Faculty />}
{role === "acadAdmin" && <AcadAdmin />}
{role === "nonAcadAdmin" && <HostelAdmin />}
```

Using conditional rendering with the logical AND operator, the component displays:
- `<Student />` component for users with "student" role
- `<Faculty />` component for users with "faculty" role
- `<AcadAdmin />` component for users with "acadAdmin" role
- `<HostelAdmin />` component for users with "nonAcadAdmin" role

## Implementation Details

### Toggle Functionality
```jsx
<button
    onClick={() => setIsOpen(true)}
    className="text-3xl text-gray-700 hover:text-green-600 transition-colors duration-300"
>
    <IoMenuOutline />
</button>
```

```jsx
<button
    onClick={() => setIsOpen(false)}
    className="text-3xl text-gray-700 hover:text-green-600 transition-colors duration-300"
>
    <IoMenuOutline />
</button>
```

The same `IoMenuOutline` icon is used for both opening and closing the sidebar, with different click handlers that:
- Set `isOpen` to `true` to expand the sidebar
- Set `isOpen` to `false` to collapse the sidebar

### Styling
The component uses Tailwind CSS utility classes for styling:

#### Collapsed State:
- `relative p-2`: Positions the hamburger menu with padding

#### Expanded State:
- `relative top-0 left-0`: Positions the sidebar at the top-left
- `w-[250px]`: Sets a fixed width of 250px
- `min-h-screen`: Makes the sidebar at least as tall as the viewport
- `bg-white shadow-2xl`: Sets a white background with a strong shadow effect
- `p-6`: Adds padding inside the sidebar
- `transition-transform duration-300`: Adds a smooth transition effect
- `mr-2`: Adds a small right margin

#### Button Styling:
- `text-3xl`: Sets icon size
- `text-gray-700 hover:text-green-600`: Sets color and hover color
- `transition-colors duration-300`: Adds a smooth color transition

### Layout Structure
```jsx
<div className="flex justify-end mb-6">
    {/* Close button */}
</div>

<div className="space-y-6">
    {/* Role-based components */}
</div>
```

The expanded sidebar has two main sections:
1. A top section with the close button aligned to the right
2. A content section with appropriate spacing between elements

## Usage
This component should be placed in a layout where it can respond to the user's role. The `RoleContext` must be properly set up and provided higher in the component tree.

## Dependencies
- Requires the `RoleContext` to be properly set up
- Depends on role-specific navigation components (Student, Faculty, AcadAdmin, HostelAdmin)
- Uses React Icons for the menu icon