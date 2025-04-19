# Navbar Component

## Overview

The `Navbar` component is a React-based front-end module designed to provide a navigation bar for an academic institution's automation system (e.g., IIT Guwahati). It displays the institution's logo, a title ("Institute Automation"), and a logout button. The component integrates with a backend API for logout functionality, uses **React Router** for navigation, **Axios** for HTTP requests, and **Tailwind CSS** for styling. The logout action clears user data and redirects to the login page.

## Dependencies

- **React**: For building the UI.
- **React Router (react-router-dom)**: For navigation (`useNavigate`).
- **Axios**: For making HTTP requests to the backend.
- **Tailwind CSS**: For styling the component.
- **Assets**: An imported logo image (`iitglogo.jpg`).

## Component Structure

The `Navbar` component consists of:

1. **Logo and Title**: Displays the institution's logo and the system title on the left.
2. **Logout Button**: A button on the right to log out the user and redirect to the login page.

## Code Explanation

### Imports

```jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import iitglogo from '../assets/iitglogo.jpg';
import axios from 'axios';
```

- **React**: Core library for the component.
- **React Router**:
  - `useNavigate`: Enables programmatic navigation (e.g., redirecting to `/login` after logout).
- **Assets**:
  - `iitglogo`: Imported image file for the institution's logo.
- **Axios**: Used for making the logout API request.
- **Commented Imports**:
  - `FontAwesomeIcon` and `faPlane` are commented out, suggesting unused or planned icon integration.
  - `newRequest` (a custom utility) is commented out, indicating a shift to direct Axios usage.

### Logout Handler

```jsx
const navigate = useNavigate();

const handleLogout = async () => {
  try {
    const response = await axios.post("http://localhost:8000/api/auth/logout", {}, { withCredentials: true });
    localStorage.setItem("currentUser", null);
    if (response.status === 200) {
      console.log("Logout successful");
      navigate("/login");
    }
  } catch (err) {
    console.log(err);
  }
};
```

- **Navigation**:
  - `useNavigate` provides the `navigate` function for redirecting to `/login`.
- **Logout Logic**:
  - Sends a POST request to `/api/auth/logout` using Axios.
  - Includes `{ withCredentials: true }` to send cookies (likely for session-based authentication).
  - Clears `currentUser` in `localStorage` by setting it to `null` (stringified `null`).
  - On success (`status === 200`):
    - Logs "Logout successful" (for debugging).
    - Redirects to `/login`.
  - On error:
    - Logs the error to the console but provides no user feedback.
- **Notes**:
  - The commented `newRequest.post` suggests a previous custom HTTP utility was replaced with Axios.
  - Setting `localStorage.setItem("currentUser", null)` may cause issues since `null` is stored as a string; `localStorage.removeItem("currentUser")` or `localStorage.setItem("currentUser", JSON.stringify(null))` might be intended.
  - No user feedback (e.g., toast notification) on error.

### Rendering

```jsx
return (
  <nav className="bg-white py-4 shadow-lg">
    <div className="container mx-auto flex items-center justify-between px-8">
      {/* Logo + Title */}
      <div className="flex items-center space-x-4">
        <img src={iitglogo} alt="Logo" className="h-12 w-12 object-contain" />
        <h1 className="text-2xl font-bold text-gray-700 tracking-wide">Institute Automation</h1>
      </div>

      {/* Logout Button */}
      <div className="flex items-center space-x-4">
        <button
          type="button"
          onClick={handleLogout}
          className="bg-gradient-to-r from-green-400 to-green-600 text-white px-5 py-2 rounded-full font-semibold shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300"
        >
          Logout
        </button>
      </div>
    </div>
  </nav>
);
```

- **Nav Container**:
  - A `<nav>` element with white background (`bg-white`), vertical padding (`py-4`), and shadow (`shadow-lg`).
- **Inner Container**:
  - A centered container (`container mx-auto`) with horizontal padding (`px-8`).
  - Uses flexbox (`flex items-center justify-between`) to align logo/title on the left and logout button on the right.
- **Logo and Title**:
  - A flex container (`flex items-center space-x-4`) with:
    - An `<img>` for the logo (`h-12 w-12 object-contain`).
    - A `<h1>` title ("Institute Automation") with large, bold, gray text (`text-2xl font-bold text-gray-700 tracking-wide`).
- **Logout Button**:
  - A `<button>` with a gradient background (`bg-gradient-to-r from-green-400 to-green-600`), white text, padding (`px-5 py-2`), rounded corners (`rounded-full`), and bold font (`font-semibold`).
  - Includes hover effects: increased shadow (`hover:shadow-lg`), scale transform (`hover:scale-105`), and smooth transition (`transition-all duration-300`).
  - Triggers `handleLogout` on click.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Nav**:
    - White background (`bg-white`), vertical padding (`py-4`), shadow (`shadow-lg`).
  - **Container**:
    - Centered (`mx-auto`), padded (`px-8`), flexbox (`flex items-center justify-between`).
  - **Logo and Title**:
    - Logo: Fixed size (`h-12 w-12`), object containment (`object-contain`).
    - Title: Large, bold, gray (`text-2xl font-bold text-gray-700`), wide tracking (`tracking-wide`).
    - Spaced via flex (`space-x-4`).
  - **Logout Button**:
    - Gradient (`bg-gradient-to-r from-green-400 to-green-600`), white text, padded (`px-5 py-2`), fully rounded (`rounded-full`), bold (`font-semibold`).
    - Shadow (`shadow-md`), with hover effects: larger shadow (`hover:shadow-lg`), scale (`hover:scale-105`), smooth transition (`transition-all duration-300`).

## Assumptions

- **Backend API**:
  - `POST /api/auth/logout`: Logs out the user, invalidates the session, and expects `{ withCredentials: true }` for cookie-based authentication.
  - Returns a 200 status on success.
- **Authentication**:
  - `currentUser` in `localStorage` stores user data (e.g., from login).
  - Logout clears the session and user data.
- **Routing**:
  - `/login` exists as a valid route for redirection.
- **Static Assets**:
  - `iitglogo.jpg` is available in `../assets/`.
- **Context**:
  - No integration with `RoleContext` or other contexts, suggesting a generic navbar for all users.

## Notes

- **Commented Imports**:
  - `FontAwesomeIcon` and `newRequest` suggest prior or planned features (e.g., icons, custom HTTP utilities).
- **Logout Feedback**:
  - Errors are logged but not displayed to the user, reducing UX quality.
- **LocalStorage**:
  - Setting `currentUser` to `null` may not fully clear user data; `removeItem` or proper serialization is preferred.
- **Static Navbar**:
  - Only includes a logout button; no links to other pages (e.g., dashboard, timetable).
- **Accessibility**:
  - Lacks ARIA attributes for the button and image.
- **Debugging**:
  - Console logs for success and error states (should be removed in production).

## Integration with Other Components

- **AssignmentLanding**:
  - Could include a link to the course list or assignments page.
- **TimeTable**:
  - A timetable link would enhance navigation.
- **CourseRegistration**:
  - A registration link could be added for students.
- **RoleContext**:
  - Integrating with `RoleContext` would allow role-specific navigation (e.g., faculty vs. student links).
- **Login**:
  - The `/login` route is the target post-logout, confirming its role in the authentication flow.

## Future Improvements

- **Clear LocalStorage Properly**:
  - Use `removeItem` or serialize `null`.
- **Add Navigation Links**:
  - Include links to dashboard, timetable, or assignments.
- **Role-Based Rendering**:
  - Use `RoleContext` to show relevant links.
- **Loading State**:
  - Add a loading indicator for logout.
- **Testing**:
  - Write unit tests for logout functionality and navigation.