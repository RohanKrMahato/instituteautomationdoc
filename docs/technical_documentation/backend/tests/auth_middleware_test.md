# Authentication Middleware Test Documentation

## Overview
This document provides detailed documentation for the Jest-based test suite of the authentication middleware, covering token validation and user verification logic.This test suite ensures that the authentication middleware functions are robust and reliable, correctly handling JWT refresh token validation, user lookup by email, and refresh token verification against the database. The suite simulates various scenarios, including missing or invalid tokens, expired tokens, user lookup failures, and successful authentication flows, to guarantee secure and predictable middleware behavior.


## Dependencies

- **Middleware Functions Tested**
  - `validateRefreshToken`
  - `findUserByEmail`
  - `verifyRefreshTokenInDB`

- **Libraries and Tools**
  - `jest` for mocking and assertions
  - `jsonwebtoken` for JWT verification (mocked)
  - `mongoose` for ObjectId and error handling (mocked)
  - `../models/user.model` for User data access (mocked)


## validateRefreshToken

**Input**
- Expects the incoming request (`req`) to have a `cookies` object.
  - The `cookies` object may contain a `refreshToken` property.

**Process**
- Checks if the `refreshToken` is present in `req.cookies`.
  - If not present, responds with a 401 status and a JSON message: `"Refresh token not provided"`.
- If a `refreshToken` is present:
  - Calls `jwt.verify()` with the token and the refresh secret.
  - If `jwt.verify` throws a syntax error (invalid token), responds with 403 and `"invalid token,login again"`.
  - If `jwt.verify` throws a `TokenExpiredError`, responds with 400 and `"expired refresh token,please login again"`.
  - If verification is successful, attaches the decoded user object to `req.user` and the token to `req.refreshToken`, then calls `next()` to proceed.
- Handles all error cases without calling `next()`.

**Output**
- 401 Unauthorized with `{ message: "Refresh token not provided" }` if token is missing.
- 403 Forbidden with `{ message: "invalid token,login again" }` if token is invalid.
- 400 Bad Request with `{ message: "expired refresh token,please login again" }` if token is expired.
- Calls `next()` and attaches user info to `req` if the token is valid.


## findUserByEmail

**Input**
- Expects `req.user` to be populated with an `email` property.

**Process**
- Uses the `User` model to find a user document by the given email.
- If a user is found:
  - Attaches the user document to `req.foundUser`.
  - Calls `next()` to proceed.
- If no user is found:
  - Responds with 404 status and `{ message: "User not found" }`.
- If a database error occurs:
  - Logs the error to the console.
  - Responds with 500 status and `"Internal server error"`.

**Output**
- Calls `next()` and attaches `foundUser` to `req` if user is found.
- 404 Not Found with `{ message: "User not found" }` if user does not exist.
- 500 Internal Server Error with `"Internal server error"` if a database error occurs.


## verifyRefreshTokenInDB

**Input**
- Expects `req.foundUser` to be populated with a `refreshToken` property.
- Expects `req.refreshToken` to be present.

**Process**
- Compares `req.foundUser.refreshToken` with `req.refreshToken`.
- If tokens match:
  - Calls `next()` to proceed.
- If tokens do not match:
  - Responds with 401 status and `{ message: "Invalid refresh token" }`.

**Output**
- Calls `next()` if tokens match.
- 401 Unauthorized with `{ message: "Invalid refresh token" }` if tokens do not match.
