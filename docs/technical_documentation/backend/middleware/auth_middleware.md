# Auth Middleware

## Overview

The `auth.middleware.js` module provides middleware functions for validating access and refresh tokens using JWT. It also includes utilities to retrieve the authenticated user from the database and ensure the integrity of the refresh token stored in the system.

## Dependencies

```javascript
import jwt from 'jsonwebtoken';
import { User } from '../models/user.model.js';`
```

## Middleware Functions

### `validateAccessToken`
Validates the JWT access token stored in cookies.

**Input:**
-   Cookie: `accessToken`
-   Cookie: `user` (JSON string)

**Process:**
1.  Extracts `accessToken` and `user` from cookies.
2.  Parses `user` JSON to retrieve user data.
3.  Verifies token using `ACCESS_TOKEN_SECRET`.
4.  Handles token expiration and invalid signatures.

**Key Code Snippet**
```javascript
const accessToken = req?.cookies?.accessToken;
const user = req?.cookies?.user;
const parsedUser = JSON.parse(user);
jwt.verify(accessToken, process.env.ACCESS_TOKEN_SECRET, (err, decoded) => {
    if (err) {
        if (err instanceof jwt.TokenExpiredError) {
            return res.status(401).json({ message: "expired access token,please refresh" });
        }
        return res.status(403).json({ message: "invalid token" });
    }
    req.user = parsedUser;
    next();
});
```

**Output:**
-   Proceeds to next middleware if valid.
-   Returns `401` if expired.
-   Returns `403` if invalid.

**Attaches to `req`:**
-   `req.user` → Parsed user info from cookie.

### `validateRefreshToken`
Validates the JWT refresh token from cookies.

**Input:**
-   Cookie: `refreshToken`

**Process:**
1.  Extracts refresh token from cookies.
2.  Verifies it using `REFRESH_TOKEN_SECRET`.
3.  Decodes and attaches user payload and refresh token to the request.

**Key Code Snippet**
```javascript
const refreshToken = req.cookies['refreshToken'];
if (!refreshToken) {
    return res.status(401).json({ message: "Refresh token not provided" });
}
jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET, (err, decoded) => {
    if (err) {
        if (err instanceof jwt.TokenExpiredError) {
            return res.status(400).json({ message: "expired refresh token,please login again" });
        }
        return res.status(403).json({ message: "invalid token,login again" });
    }
    req.user = decoded.user;
    req.refreshToken = refreshToken;
    next();
});
```

**Output:**
-   Proceeds to next middleware if valid.
-   Returns `400` if token is expired.
-   Returns `403` if token is invalid.

**Attaches to `req`:**
-   `req.user` → Decoded user object from token.
-   `req.refreshToken` → Raw refresh token.

### `findUserByEmail`
Fetches the user document from the database using email.

**Input:**
-   `req.user.email` → Populated by previous middleware

**Process:**
1.  Finds user by lowercase, trimmed email.
2.  Returns `404` if not found.

**Key Code Snippet**
```javascript
const email = req.user.email;
const user = await User.findOne({ email: email.toLowerCase().trim() });
if (!user) {
    return res.status(404).json({ message: "User not found" });
}
req.foundUser = user;
```

**Output:**
-   Proceeds if user exists.
-   Returns error if not found or on DB failure.

**Attaches to `req`:**
-   `req.foundUser` → Full user document.

### `verifyRefreshTokenInDB`
Compares the provided refresh token with the one stored in DB.

**Input:**
-   `req.foundUser.refreshToken` (from DB)
-   `req.refreshToken` (from client cookie)

**Process:**
1.  Compares the two tokens for equality.

**Key Code Snippet**
```javascript
if (req.foundUser.refreshToken !== req.refreshToken) {
    return res.status(401).json({ message: "Invalid refresh token" });
}
```

**Output:**
-   Proceeds if tokens match.
-   Returns `401` if tokens differ.

* * * * *

## Error Handling Strategy
-   Uses status codes `401`, `403`, `404`, and `500` with detailed messages.
-   All async operations wrapped in `try-catch` blocks.
-   Includes fallback for expired tokens and invalid token formats.

## Security Considerations
-   All JWTs are verified using environment-defined secrets.
-   Refresh tokens are stored securely in the database.
-   Access tokens are short-lived (as per controller config).