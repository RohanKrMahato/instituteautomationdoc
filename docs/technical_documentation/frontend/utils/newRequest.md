# newRequest Utility

## Overview

The `newRequest` utility is a pre-configured **Axios** instance designed to simplify HTTP requests to a backend API in an academic institution's automation system (e.g., IIT Guwahati). It sets a base URL and enables credential inclusion for authenticated requests, providing a reusable client for API interactions across the application. This utility is likely used in components like `Navbar`, `AssignmentDetail`, or `CourseRegistration` to communicate with the backend.

## Dependencies

- **Axios**: A promise-based HTTP client for making API requests.

## Utility Structure

The utility is a single exported Axios instance with predefined configuration.

## Code Explanation

### Imports

```javascript
import axios from "axios";
```

- **Axios**: Imported to create a custom HTTP client instance.

### Axios Instance Creation

```javascript
const newRequest = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true,
});
```

- **axios.create**:
  - Creates a new Axios instance with custom configuration.
- **Configuration**:
  - `baseURL`: Sets the base URL for all requests to `http://localhost:8000/api/`.
    - All requests using `newRequest` will prepend this URL (e.g., `newRequest.get('/auth/logout')` becomes `http://localhost:8000/api/auth/logout`).
  - `withCredentials: true`:
    - Ensures cookies and authentication credentials (e.g., session tokens) are sent with requests.
    - Critical for session-based authentication, allowing the backend to identify authenticated users.
- **Instance**:
  - Stored in `newRequest`, a reusable client for API calls.

### Export

```javascript
export default newRequest;
```

- Exports the configured Axios instance as the default export.
- Importable in other modules as `newRequest` (e.g., `import newRequest from './utils/newRequest';`).

## Assumptions

- **Backend API**:
  - The backend runs on `http://localhost:8000/api/` during development.
  - Supports session-based authentication, requiring credentials (cookies) for protected routes.
- **Usage Context**:
  - Used in a React application to handle API requests for authentication, assignments, courses, or timetables.
- **Environment**:
  - The `baseURL` is hardcoded for local development; production likely requires a different URL.
- **Authentication**:
  - The backend expects credentials for routes like `/auth/logout` or `/assignment/submit`.

## Notes

- **Hardcoded baseURL**:
  - `http://localhost:8000/api/` is suitable for development but needs environment-based configuration for production.
- **Minimal Configuration**:
  - Only `baseURL` and `withCredentials` are set, which is sufficient for basic use but lacks advanced features like interceptors or default headers.
- **No Error Handling**:
  - The instance does not include global error handling or request/response interceptors.


## Integration with Other Components

- **Navbar**:
  - Intended for logout (`/auth/logout`), but currently uses direct Axios.
- **AssignmentDetail**:
  - Likely uses `newRequest` to fetch assignment data (`/assignment/:courseId/:assignmentId`).
- **FacultyAssignmentSubmissions**:
  - Could use `newRequest` for fetching submissions (same endpoint as `AssignmentDetail`).
- **CourseRegistration**:
  - May use `newRequest` to submit course registrations (`/register`).
- **RoleContext**:
  - No direct integration, but `newRequest` supports authenticated requests tied to `currentUser` roles.
- **convertImageToBase64**:
  - Complements `newRequest` by preparing image data for upload via API calls.

## Future Improvements

- **Environment-Based baseURL**:
  - Use environment variables for the `baseURL`.
- **Request/Response Interceptors**:
  - Add interceptors for global error handling or token refresh.
- **Default Headers**:
  - Set common headers like `Content-Type`.
- **Timeout Configuration**:
  - Add a timeout to prevent hanging requests.
- **Testing**:
  - Write unit tests for API requests.
