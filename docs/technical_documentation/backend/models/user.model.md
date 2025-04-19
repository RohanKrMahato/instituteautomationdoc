# User Model 

## Overview

This document describes the data model used to manage user information within the system. The `User` model is defined in the `user.model.js` file and is essential for authentication, profile management, and user-specific operations.

## Model

### User Model

The `User` model represents a registered individual in the system. It includes personal details, authentication credentials, and verification status.

#### Schema Definition

```javascript
import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  refreshToken: { type: String, required: true },
  contactNo: { type: String },
  profilePicture: { type: String },
  signature: { type: String },
  address: { type: String },
  dateOfBirth: { type: Date },
  bloodGroup: { type: String },
  isVerified: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

export const User = mongoose.model('User', userSchema);
```

#### Fields

| Field          | Type    | Required | Default    | Description                                     |
|----------------|---------|----------|------------|-------------------------------------------------|
| name           | String  | Yes      | -          | Full name of the user                           |
| email          | String  | Yes      | -          | User's email address, must be unique            |
| password       | String  | Yes      | -          | Hashed password for authentication              |
| refreshToken   | String  | Yes      | -          | Token used to refresh JWT sessions              |
| contactNo      | String  | No       | -          | User's contact number                           |
| profilePicture | String  | No       | -          | URL or filename of the user's profile picture   |
| signature      | String  | No       | -          | URL or filename of the user's digital signature |
| address        | String  | No       | -          | User's home or mailing address                  |
| dateOfBirth    | Date    | No       | -          | User's date of birth                            |
| bloodGroup     | String  | No       | -          | User's blood group                              |
| isVerified     | Boolean | No       | false      | Indicates if the user's email is verified       |
| createdAt      | Date    | No       | Date.now   | Timestamp when the user was created             |
| updatedAt      | Date    | No       | Date.now   | Timestamp when the user was last updated        |

#### Relationships

- **Authentication (One-to-One)**: Used in login systems to authenticate users.
- **Session Management**: The `refreshToken` field supports secure and scalable session handling.
- **Extended Models**: This model can be associated with other models like Complaints, Tickets, or Activity Logs.

#### Usage

The User model is used to:
- Register and authenticate users
- Manage and retrieve user profile data
- Store authentication tokens and verification state
- Track account creation and updates

## Model Registration

```javascript
export const User = mongoose.model('User', userSchema);
```

This registers the model with Mongoose and makes it available for import and use throughout the application.

## Database Considerations

### Indexing

The following fields should be indexed for performance:
- `email`: Ensures uniqueness and allows fast lookup during login
- `refreshToken`: Used for verifying and refreshing sessions securely

### Data Validation

- **Required fields**: Ensure completeness of core user data
- **Unique constraints**: Prevent duplicate accounts via email
- **Defaults**: Ensure fields like verification and timestamps are initialized correctly

### Performance Considerations

- Passwords should always be hashed before storage (use middleware for hashing)
- Refresh tokens must be securely stored and rotated frequently
- Avoid overloading user profiles with large image/signature files; consider storing URLs or cloud references