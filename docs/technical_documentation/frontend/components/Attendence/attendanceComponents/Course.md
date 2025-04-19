# Course

## Overview

The `Course` component is a React component that renders a grid of course cards. It displays different content based on the user's role and makes the cards clickable links for navigation (except for academic administrators).

## Dependencies

- **react-router-dom**: Used for navigation links
- **React Context API**: Used to access user role information

## Props

| Prop | Type | Description |
|------|------|-------------|
| `courses` | Array | An array of course objects containing course details |

## Course Object Structure

Each course object in the `courses` array is expected to have the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `courseId` | String | The unique identifier for the course |
| `courseName` | String | The name of the course |
| `attendance` | Number | For students and academic admins: Student's attendance percentage in the course |
| `averageAttendance` | Number | For faculty: The average attendance percentage across all students in the course |

## Role-Based Logic

The component uses React Context to access the user's role (`student`, `faculty`, or `acadAdmin`) and displays different attendance data based on this role:

- **Faculty**: Shows average attendance across all students in the course
- **Student**: Shows the student's personal attendance percentage
- **Academic Admin**: Shows attendance data but cards are not clickable

## Navigation

For `student` and `faculty` roles, each course card is wrapped in a `<Link>` component that navigates to `/attendancelanding/{courseId}` when clicked. For the `acadAdmin` role, cards are rendered without links.

## Component Structure

```jsx
function Course(courses) {
    const { role } = useContext(RoleContext);

    return (
        <div className="my-courses">
            {
                courses.courses.map((course) => {
                    // Card rendering logic
                    // ...
                })
            }
        </div>
    );
}
```

The component:
1. Gets the user's role from context
2. Maps through the courses array to render individual course cards
3. Conditionally wraps cards in navigation links based on role

## Code Breakdown

### Context and Role Access

```jsx
import { RoleContext } from '../../../context/Rolecontext';
import { useContext } from 'react';

function Course(courses) {
    const { role } = useContext(RoleContext);
    
    // Rest of component...
}
```

This section:
- Imports the necessary React hooks and context
- Accesses the user's role from the `RoleContext`

### Card Content Rendering

```jsx
const cardContent = (
    <div className="course-card">
        <div className="overlap-7">
            <div className="overlap-8">
                <div className="text-wrapper-5">{course.courseId}</div>
                <div className="pie-chart-5">
                    <div className="overlap-group-2">
                        <div className="ellipse"></div>
                        <div className="text-wrapper-4-attendance">{role === "faculty" && course.averageAttendance}</div>
                        <div className="text-wrapper-4-attendance">{role === "student" && course.attendance}</div>
                        <div className="text-wrapper-4-attendance">{role === "acadAdmin" && course.attendance}</div>
                    </div>
                </div>
            </div>
            <div className="text-wrapper-8">{course.courseName}</div>
        </div>
    </div>
);
```

This section:
- Creates the visual structure for each course card
- Displays the course ID and name
- Uses conditional rendering to show different attendance data based on user role
- Includes styling classes for layout and appearance

### Conditional Rendering Based on Role

```jsx
return role === "acadAdmin" ? (
    <div key={course.courseId}>{cardContent}</div>
) : (
    <Link key={course.courseId} to={`/attendancelanding/${course.courseId}`}>
        {cardContent}
    </Link>
);
```

This ternary operation:
- Renders plain div containers for academic administrators
- Renders clickable links for students and faculty members
- Uses the course ID as the React key for efficient list rendering
- Sets the navigation path to include the course ID

## CSS Classes

The component uses several CSS classes for styling:

- `my-courses`: Container for the entire course list
- `course-card`: Styling for individual course cards
- `overlap-7`, `overlap-8`, `overlap-group-2`: Layout classes for nested elements
- `text-wrapper-5`: Styling for course ID text
- `text-wrapper-8`: Styling for course name text
- `text-wrapper-4-attendance`: Styling for attendance percentage display
- `pie-chart-5`: Container for attendance visualization
- `ellipse`: Visual element for attendance display

## Usage Notes

1. The component expects to receive an array of course objects via the `courses` prop
2. The `RoleContext` must be properly set up higher in the component tree
3. The component assumes the role will be one of: "student", "faculty", or "acadAdmin"
4. CSS classes should be properly defined in an external stylesheet
5. The React Router setup must include routes that handle the `/attendancelanding/{courseId}` path pattern