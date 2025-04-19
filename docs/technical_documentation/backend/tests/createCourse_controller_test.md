# Authentication Controller Test

## Overview
The authentication controller test suite validates the core authentication flows for users in a multi-role academic system. It covers the login, token refresh, and logout endpoints, ensuring correct handling of credentials, roles, tokens, and session management. All models and middleware are mocked to focus on the controller logic.


## Dependencies

- **Controllers Tested**
  - `login`
  - `refresh`
  - `logout`

- **Models Mocked**
  - `User`
  - `Student`
  - `Faculty`
  - `AcadAdmin`
  - `HostelAdmin`

- **Middleware Mocked**
  - `validateAccessToken`
  - `validateRefreshToken`
  - `findUserByEmail`
  - `verifyRefreshTokenInDB`

- **Libraries Used**
  - `jest` for mocking and assertions
  - `bcrypt` for password hashing and comparison
  - `jsonwebtoken` for JWT token creation and verification


## login

**Input**
- Receives a JSON body with:
  - `email`: User’s email (required)
  - `password`: User’s password (required)
  - `role`: User’s role (`student`, `faculty`, `acadAdmin`, `nonAcadAdmin`; required)

**Process**
- Checks that all required fields (`email`, `password`, `role`) are present. If not, responds with 400 and an error message.
- Looks up the user by email in the `User` model. If the user is not found, responds with 401 and "Invalid credentials".
- Uses `bcrypt.compare` to verify the password. If incorrect, responds with 401 and "Invalid credentials".
- Depending on the specified role, checks if the user exists in the corresponding role model (`Student`, `Faculty`, `AcadAdmin`, `HostelAdmin`). If not, responds with 401 and "Invalid role".
- If the role is not recognized, responds with 400 and "Invalid role".
- If all checks pass:
  - Generates an access token (expires in 1 hour) and a refresh token (expires in 1 day) using `jsonwebtoken`.
  - Saves the refresh token to the user’s record.
  - Sets three cookies: `user`, `refreshToken`, and `accessToken`, all with secure and cross-site options.
  - Sets the `Authorization` header with the access token.
  - Responds with a 200 status and the user's email and userId in JSON.

**Output**
- 400 Bad Request: If any required field is missing or the role is invalid.
- 401 Unauthorized: If credentials are invalid or the user does not have the specified role.
- 200 OK: On success, sets cookies and returns `{ user: { email, userId } }` in JSON.
- 500 Internal Server Error: If a database or unexpected error occurs, responds with a generic error message.


## refresh

**Input**
- Expects:
  - A valid `refreshToken` cookie.
  - A `foundUser` object (populated by middleware) with user details.

**Process**
- Uses the found user's details to generate a new access token with JWT (expires in 1 hour).
- Sets the new access token in a cookie and as an `Authorization` header.
- Responds with the user's email and role in JSON.
- If token signing fails, responds with 500 and an error message.

**Output**
- 200 OK: Returns a new access token (in header and cookie) and `{ user: { email, role } }` in JSON.
- 500 Internal Server Error: If token signing fails, responds with "Internal server error".


## logout

**Input**
- Expects authentication-related cookies to be present:
  - `refreshToken`
  - `accessToken`
  - `user`

**Process**
- Clears all authentication cookies (`refreshToken`, `accessToken`, `user`) from the response using secure options.
- Responds with a logout success message.
- If cookie clearing fails, responds with 500 and an error message.

**Output**
- 200 OK: Returns `{ message: 'Logout successful' }` in JSON when cookies are cleared.
- 500 Internal Server Error: If an error occurs during cookie clearing, responds with "Something went wrong!".

