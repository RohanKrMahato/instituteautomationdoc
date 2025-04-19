# unauth Component

## Overview

The `Unauthorized` component is a React-based front-end module designed to display an access denial message for users attempting to access a restricted page at an academic institution (e.g., IIT Guwahati). It is used in role-based routing scenarios (e.g., within the `AnnouncementWrapper` component) to inform users they lack permission and display their current role. The component is styled with **Tailwind CSS** and uses **React Icons** for visual feedback, providing a clean and user-friendly interface.

## Dependencies

- **React**: For building the UI.
- **React Icons (react-icons/fa)**: For rendering the warning icon (`FaExclamationTriangle`).
- **Tailwind CSS**: For styling the component.

## Component Structure

The `Unauthorized` component is a simple, presentational component that:

1. Displays a centered error message with an icon.
2. Shows the user's current role (or "None" if undefined).
3. Provides a link to return to the homepage.

## Code Explanation

### Imports

```jsx
import React from 'react';
import { FaExclamationTriangle } from 'react-icons/fa';
```

- **React**: Required for defining the component.
- **FaExclamationTriangle**: A warning icon from `react-icons/fa` to visually indicate access denial.

### Component Definition

```jsx
const Unauthorized = ({ role }) => (
  <div className="flex items-center justify-center min-h-screen bg-gray-100">
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
      <div className="flex flex-col items-center text-center">
        <div className="bg-red-100 p-3 rounded-full mb-4">
          <FaExclamationTriangle className="text-red-500 text-2xl" />
        </div>
        
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Access Denied</h1>
        
        <p className="text-gray-600 mb-4">
          You don't have permission to access this page.
        </p>
        
        <div className="bg-gray-100 p-3 rounded-md w-full mb-4">
          <p className="text-sm text-gray-500 mb-1">Current role:</p>
          <p className="font-medium text-gray-700">{role || 'None'}</p>
        </div>
        
        <a 
          href="/" 
          className="bg-blue-500 text-white py-2 px-6 rounded-md font-medium hover:bg-blue-600 transition duration-300"
        >
          Return to Homepage
        </a>
      </div>
    </div>
  </div>
);
```

- **Props**:
  - `role`: A string (or `null`/undefined) indicating the user's current role (e.g., `"student"`, `"faculty"`, or invalid).
- **Structure**:
  - **Outer Container**: A full-screen flex container (`min-h-screen`, `bg-gray-100`) that centers the content.
  - **Card**: A white card (`bg-white`, `p-8`, `rounded-lg`, `shadow-lg`) with a maximum width (`max-w-md`).
  - **Icon**: A warning triangle (`FaExclamationTriangle`) in a red circle (`bg-red-100`, `text-red-500`).
  - **Heading**: A bold "Access Denied" title (`text-2xl`, `font-bold`).
  - **Message**: A brief explanation (`text-gray-600`).
  - **Role Display**: Shows the user’s role or "None" in a gray box (`bg-gray-100`, `rounded-md`).
  - **Link**: A button-like link (`<a href="/" ...>`) styled as a blue button (`bg-blue-500`, `hover:bg-blue-600`).
- **Role Fallback**: Uses the logical OR operator (`role || 'None'`) to display "None" if `role` is falsy.

### Export

```jsx
export default Unauthorized;
```

- Exports the `Unauthorized` component as the default export for use in other parts of the application.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Layout**: Flexbox for centering (`flex`, `items-center`, `justify-center`), full-screen height (`min-h-screen`).
  - **Card**: White background (`bg-white`), padding (`p-8`), rounded corners (`rounded-lg`), shadow (`shadow-lg`), constrained width (`max-w-md`, `w-full`).
  - **Icon**: Red background circle (`bg-red-100`, `rounded-full`), red icon (`text-red-500`, `text-2xl`).
  - **Typography**:
    - Heading: Large and bold (`text-2xl`, `font-bold`, `text-gray-800`).
    - Message: Subtle gray (`text-gray-600`).
    - Role labels: Small and light (`text-sm`, `text-gray-500`), with the role value in medium weight (`font-medium`, `text-gray-700`).
  - **Button**: Blue background (`bg-blue-500`), white text, rounded (`rounded-md`), hover effect (`hover:bg-blue-600`), smooth transition (`transition duration-300`).
  - **Role Box**: Light gray background (`bg-gray-100`), padding (`p-3`), rounded (`rounded-md`).

## Notes

- **Navigation**:
  - Uses a plain `<a href="/">` instead of React Router’s `Link`. This causes a full page reload, which may not align with a single-page application (SPA) architecture.
  - Consider replacing with `Link` from `react-router-dom` for client-side navigation.
- **Role Prop**:
  - The `role` prop is optional and defaults to `"None"` if falsy, making the component robust to undefined roles.
  - Useful for debugging or informing users of their current role status.
- **Static Content**:
  - The message and styling are fixed, with no dynamic customization beyond the `role` prop.
- **Context**:
  - Typically used within a role-based routing system (e.g., `AnnouncementWrapper`), where `role` is provided by a context like `RoleContext`.

## Assumptions

- **Routing**: The application uses a routing system where this component is rendered when a user attempts to access a restricted route.
- **Homepage**: The `/` route exists and is a valid destination for redirection.
- **Tailwind CSS**: Configured in the project to support the used classes.
- **RoleContext**: The `role` prop is passed from a parent component (e.g., `AnnouncementWrapper`) that accesses a context or authentication system.

## Usage Example

This component is likely used within a role-based routing setup, such as in `AnnouncementWrapper`:

```jsx
import Unauthorized from './Unauthorized';

const AnnouncementWrapper = () => {
  const { role } = useContext(RoleContext);
  
  switch (role) {
    case 'student':
      return <CourseAnnouncements />;
    case 'faculty':
      return <FacultyCourseAnnouncements />;
    default:
      return <Unauthorized role={role} />;
  }
};
```

When a user with an invalid role (e.g., `null` or `"admin"`) accesses a restricted route, the `Unauthorized` component renders with the provided `role` value displayed.

## Future Improvements

- **React Router Integration**:
  - Replace `<a href="/">` with `<Link to="/">` to maintain SPA behavior:
- **Dynamic Messaging**:
  - Accept a prop for a custom message or redirect URL to make the component reusable in different contexts.
- **Accessibility**:
  - Add ARIA attributes (e.g., `aria-live` for the error message, `aria-label` for the link).
  - Ensure keyboard navigation works (e.g., `tabindex` on the link).
- **Redirect Logic**:
  - Use `useNavigate` from `react-router-dom` to programmatically redirect after a delay or based on conditions:
- **Error Context**:
  - Display specific error details (e.g., “This page is for faculty only”) based on the expected role.
- **Testing**:
  - Write unit tests to verify rendering with different `role` values (e.g., `"student"`, `null`, undefined).
  - Test the link’s behavior and styling consistency.
- **Styling Variants**:
  - Allow theming or custom colors via props to align with different parts of the application.
