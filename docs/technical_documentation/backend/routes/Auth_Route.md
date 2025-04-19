# Auth Route

## Overview
This document provides comprehensive technical documentation for the Authentication API routes defined in `auth.route.js`. These routes handle user authentication flows including login, token refresh, logout, and password reset functionality.

## Base URL
All routes are prefixed with `/api/auth` (assumed based on typical Express configuration)

## Endpoints

### Authentication

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/login` | `login` | Authenticate a user and issue access tokens |
| POST | `/refresh` | `refresh` | Issue a new access token using a valid refresh token |
| POST | `/logout` | `logout` | Invalidate the current user session |

### Password Management

| Method | Endpoint | Controller Function | Description |
|--------|----------|---------------------|-------------|
| POST | `/forgot-password` | `forgotPassword` | Initiate the password reset process |
| POST | `/reset-password/:token` | `resetPassword` | Complete the password reset using a valid token |

## Usage Examples

### User Login
```javascript
// Example request
fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'user@example.com',
    password: 'securePassword123'
  })
})
  .then(response => response.json())
  .then(data => {
    // Store tokens securely
    localStorage.setItem('accessToken', data.accessToken);
    sessionStorage.setItem('refreshToken', data.refreshToken);
  });
```

### Token Refresh
```javascript
// Example request
fetch('/api/auth/refresh', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    refreshToken: sessionStorage.getItem('refreshToken')
  })
})
  .then(response => response.json())
  .then(data => {
    // Update stored access token
    localStorage.setItem('accessToken', data.accessToken);
  });
```

### User Logout
```javascript
// Example request
fetch('/api/auth/logout', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
})
  .then(() => {
    // Clear stored tokens
    localStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
  });
```

### Forgot Password
```javascript
// Example request
fetch('/api/auth/forgot-password', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com'
  })
})
  .then(response => response.json())
  .then(data => console.log(data.message));
```

### Reset Password
```javascript
// Example request
fetch('/api/auth/reset-password/a1b2c3d4e5f6', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    newPassword: 'newSecurePassword456',
    confirmPassword: 'newSecurePassword456'
  })
})
  .then(response => response.json())
  .then(data => console.log(data.message));
```

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 201: Resource created successfully
- 400: Bad request (invalid parameters)
- 401: Unauthorized (invalid credentials)
- 403: Forbidden
- 404: Resource not found
- 500: Server error

Common error scenarios:
- Invalid credentials during login
- Expired or invalid refresh token
- Invalid or expired password reset token
- Password reset token mismatch
- Invalid email format
- Non-existent user email

## Security Considerations
- Access tokens should have a short expiration time (e.g., 15-60 minutes)
- Refresh tokens should have a longer expiration time (e.g., 1-7 days)
- Password reset tokens should expire after a short period (e.g., 1 hour)
- All tokens should be transmitted and stored securely
- Implement rate limiting to prevent brute force attacks
- Use HTTPS for all API requests
- Consider implementing CSRF protection for cookie-based authentication
- Implement account lockout after multiple failed login attempts