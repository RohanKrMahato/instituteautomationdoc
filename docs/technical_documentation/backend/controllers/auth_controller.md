# Auth Controller
===============

## Overview
--------

The `auth.controller.js` module handles user authentication, including login, token refresh, and logout. It supports multiple roles (`student`, `faculty`, `acadAdmin`, `nonAcadAdmin`) and uses JWT-based authentication with cookies to manage session security.

## Dependencies
------------

```javascript

import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { User } from '../models/user.model.js';
import { Faculty } from '../models/faculty.model.js';
import { Student } from '../models/student.model.js';
import { AcadAdmin } from '../models/acadAdmin.model.js';
import { HostelAdmin } from '../models/hostelAdmin.model.js';
import { validateAccessToken, validateRefreshToken } from '../middleware/auth.middleware.js';
import { findUserByEmail, verifyRefreshTokenInDB } from '../middleware/auth.middleware.js';`
```

## Controller Methods

### `login`
Authenticates user and generates JWT access & refresh tokens.

**Input:**
-   `req.body`: `email`, `password`, `role`

**Process:**
1.  Validates input fields.
2.  Looks up the user by email.
3.  Compares hashed password using bcrypt.
4.  Checks for existence in respective role collection.
5.  Generates JWT access and refresh tokens.
6.  Stores refresh token in DB.
7.  Sends tokens via cookies.

**Output:**
-   Success (200): Returns `user` object and sets cookies.
-   Error (400/401/500): Input validation failure or internal error.

**Cookies Set:**
-   `user`
-   `accessToken`
-   `refreshToken`

**Token Expiry:**
-   Access Token: 1 hour
-   Refresh Token: 1 day

### `refresh`
Middleware-based route to refresh access token using a valid refresh token.

**Input:**
-   Valid `refreshToken` cookie and headers

**Process:**
1.  `validateRefreshToken`: Validates JWT structure.
2.  `findUserByEmail`: Finds user from the token payload.
3.  `verifyRefreshTokenInDB`: Confirms token match in database.
4.  Generates new access token.

**Output:**
-   Success (200): Returns new access token.
-   Error (500): Token invalid or internal error.

### `logout`
Clears authentication cookies and ends user session.

**Input:**
-   Requires valid access token in headers

**Process:**
1.  Validates access token via `validateAccessToken`.
2.  Clears all cookies (`refreshToken`, `accessToken`, `user`).

**Output:**
-   Success (200): Logout confirmation.
-   Error (500): Internal server error.

## Error Handling Strategy

-   All methods are wrapped in try-catch blocks.
-   Input validations for essential fields.
-   Proper use of status codes: `400` for bad input, `401` for auth failure, `500` for server errors.
-   Server logs for all critical failures.

## Security Considerations

-   JWT access and refresh tokens signed using secrets from environment variables.
-   Refresh token stored in DB and validated on refresh.
-   All cookies are:
    -   `httpOnly: false` *(can be toggled to true for production)*
    -   `sameSite: 'none'`
    -   `secure: true` *(for HTTPS support)*