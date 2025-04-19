# Meal Middleware

## Overview

The `meal.middleware.js` module provides middleware functions for authenticating and authorizing users for meal-related functionality. It verifies user authentication, confirms student status, and validates administrative access for meal management operations.

## Dependencies

```javascript
import { User } from "../models/user.model.js";
import { Student } from "../models/student.model.js";
```

## Middleware Functions

### `validateMealAccess`
Authenticates users for accessing meal-related endpoints.

**Input:**
-   Cookie: `user` or `userData` (JSON string or object)

**Process:**
1.  Extracts user data from cookies.
2.  Parses cookie data if needed.
3.  Validates presence of email and userId.
4.  Retrieves user from database to confirm existence.

**Output:**
-   Proceeds to next middleware if valid.
-   Returns `401` if authentication is missing or invalid.
-   Returns `500` for server errors.

**Attaches to `req`:**
-   `req.user` → Object with user ID, email, and role.

### `isStudent`
Verifies the authenticated user has a student role and record.

**Input:**
-   `req.user` → Populated by previous middleware

**Process:**
1.  Checks if user exists and has a valid ID.
2.  Validates that user role is 'student'.
3.  Finds corresponding student record in database.

**Output:**
-   Proceeds if user is a valid student.
-   Returns `401` if not authenticated.
-   Returns `403` if not a student or no student record.

**Attaches to `req`:**
-   `req.student` → Full student document.

### `isMealAdmin`
Confirms the authenticated user has meal administration privileges.

**Input:**
-   `req.user` → Populated by previous middleware

**Process:**
1.  Checks user authentication.
2.  Verifies that user role is 'nonAcadAdmin'.

**Output:**
-   Proceeds if user is a meal admin.
-   Returns `401` if not authenticated.
-   Returns `403` if not authorized as admin.

* * * * *

## Error Handling Strategy
-   Uses status codes `401`, `403`, and `500` with descriptive messages.
-   All database operations wrapped in `try-catch` blocks.
-   Handles JSON parsing errors from cookies.

## Security Considerations
-   Validates user existence in database for each request.
-   Omits sensitive fields when retrieving user data.
-   Role-based access control for specialized operations.