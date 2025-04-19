# Authentication Controller Test

## Overview
This document provides comprehensive testing details for the authentication controller, covering the login, refresh, and logout functionalities. Each function is described in terms of its inputs, processing logic, and expected outputs, based on the Jest test suite implementation.
This test suite rigorously tests the authentication controller's core features, ensuring secure and robust handling of user authentication, token management, and session termination. The suite covers all major scenarios for various user roles (student, faculty, academic admin, hostel admin), including error handling for invalid credentials, missing fields, and database failures.


## Dependencies

**Controllers Tested**
- `login`
- `refresh`
- `logout`

**Models Mocked**
- `User`
- `Student`
- `Faculty`
- `AcadAdmin`
- `HostelAdmin`

**Middleware Mocked**
- `validateAccessToken`
- `validateRefreshToken`
- `findUserByEmail`
- `verifyRefreshTokenInDB`

**Libraries Used**
- `jest` for mocking and assertions
- `bcrypt` for password hashing and comparison
- `jsonwebtoken` for JWT token creation and verification[2][3]


## login

**Input**
- Expects a JSON body with the following fields:
  - `email`: String (required)
  - `password`: String (required)
  - `role`: String (required, must be one of: `student`, `faculty`, `acadAdmin`, `nonAcadAdmin`)[2][3]

**Process**
- Validates that all required fields are present; returns 400 if any are missing.
- Searches for a user by email in the User model; returns 401 if not found.
- Compares the provided password with the stored hash using bcrypt; returns 401 if incorrect.
- Depending on the specified role, checks for a corresponding record in the relevant model (Student, Faculty, AcadAdmin, HostelAdmin); returns 401 if not found.
- Returns 400 if the role is invalid.
- If all checks pass:
  - Generates an access token (expires in 1 hour) and a refresh token (expires in 1 day) using JWT.
  - Saves the refresh token to the user's record.
  - Sets three cookies: `user`, `refreshToken`, and `accessToken`, all with security options (`httpOnly: false`, `sameSite: 'none'`, `secure: true`, `maxAge: 86400000`).
  - Sets the `Authorization` header with the access token.
  - Returns a 200 response with the user's email and userId in the JSON body.
- If a database error occurs, returns 500 with a generic error message[2][3].

**Output**
- 400 Bad Request: If any required field is missing or the role is invalid.
- 401 Unauthorized: If credentials are invalid or the user does not have the specified role.
- 200 OK: On successful authentication, returns cookies and `{ user: { email, userId } }`.
- 500 Internal Server Error: On database or unexpected errors[2][3].


## refresh

**Input**
- Expects:
  - A valid `refreshToken` cookie.
  - A `foundUser` object (populated by middleware) containing user details (`email`, `role`)[2][3].

**Process**
- Uses the found user's details to generate a new access token with JWT (expires in 1 hour).
- Sets the new access token in a cookie and as an `Authorization` header.
- Returns 200 with the user's email and role.
- If token signing fails, returns 500 with an error message[2][3].

**Output**
- 200 OK: Returns a new access token and `{ user: { email, role } }`.
- 500 Internal Server Error: If token signing fails[2][3].


## logout

**Input**
- Expects authentication-related cookies to be present:
  - `refreshToken`
  - `accessToken`
  - `user`[2][3]

**Process**
- Clears all relevant authentication cookies from the response (`refreshToken`, `accessToken`, `user`), using `{ httpOnly: false, sameSite: 'strict' }` options.
- Returns 200 with a logout success message.
- If cookie clearing fails, returns 500 with an error message[2][3].

**Output**
- 200 OK: Returns `{ message: 'Logout successful' }`.
- 500 Internal Server Error: If an error occurs during cookie clearing[2][3].
