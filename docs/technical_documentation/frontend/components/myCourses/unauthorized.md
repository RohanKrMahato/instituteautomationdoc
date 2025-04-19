
# Unauthorized Component Documentation

## Overview
The `Unauthorized` component displays an access denied message when a user’s role does not permit viewing a page. It shows the current role (if any) and provides a link back to the homepage.

## File Location
**File Name**: `Unauthorized.js` (or `.jsx`)

## Dependencies
- **React**: Core UI library.
- **React Icons** (`react-icons/fa`): Icon for the warning symbol (`FaExclamationTriangle`).

## Props
- `role` (string | undefined): The current user role to display. Defaults to `'None'` if not provided.

## Component Structure
1. **Wrapper**  
   ```jsx
   <div className="flex items-center justify-center min-h-screen bg-gray-100">
   ```
   Centers content vertically and horizontally on a full-screen gray background.
2. **Card**  
   ```jsx
   <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
   ```
   White card with padding, rounded corners, and shadow.
3. **Icon**  
   ```jsx
   <FaExclamationTriangle className="text-red-500 text-2xl" />
   ```
   Displays a red warning icon inside a circular background.
4. **Heading & Message**  
   - **Heading**: `<h1>` with "Access Denied"  
   - **Message**: `<p>` explaining lack of permission.
5. **Role Display**  
   ```jsx
   <div className="bg-gray-100 p-3 rounded-md w-full">
     <p className="text-sm text-gray-500">Current role:</p>
     <p className="font-medium text-gray-700">{role || 'None'}</p>
   </div>
   ```
6. **Return Link**  
   ```jsx
   <a href="/" className="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600">Return to Homepage</a>
   ```

## Usage Example
```jsx
import Unauthorized from './Unauthorized';

function ProtectedRoute({ role }) {
  return role === 'admin'
    ? <AdminDashboard />
    : <Unauthorized role={role} />;
}
```

## Notes
- Tailwind CSS classes are used for layout and styling.
- Ensure `react-icons` is installed to render the warning icon.
