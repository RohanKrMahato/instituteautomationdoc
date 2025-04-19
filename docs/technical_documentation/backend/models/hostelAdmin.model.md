# HostelAdmin Model 

This document provides a structured overview of the `HostelAdmin` schema used in the application for managing hostel administration staff.

---

## Schema Definition

```ts
import mongoose from "mongoose";

const hostelTypeEnum = [
  "kameng",
  "subansiri",
  "lohit",
  "disang",
  "brahmaputra",
  "dihing",
  "kapili",
  "manas",
  "dhansiri",
  "barak"
];

// Hostel Admin Model
const hostelAdminSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  // hostel: {
  //   type: String,
  //   required: true,
  //   enum: hostelTypeEnum,
  //   default: "Not Assigned"
  // },
  // designation: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  status: { 
    type: String, 
    enum: ['active', 'inactive', 'on-leave'], 
    default: 'active' 
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

export const HostelAdmin = mongoose.model
```
## Fields

| Field                                 | Type                           | Required | Default          | Description                                                      |
|---------------------------------------|--------------------------------|----------|------------------|------------------------------------------------------------------|
| `userId`                              | `ObjectId` (ref: `User`)       | Yes      | -                | Reference to the `User` model                                    |
| `email`                               | `String`                       | Yes      | -                | Hostel Admin's email (must be unique)                            |
| `status`                              | `String`                       | No       | 'active'         | Current status of the hostel admin (active, inactive, on-leave)  |
| `createdAt`                           | `Date`                         | No       | `Date.now`       | Timestamp of hostel admin record creation                        |
| `updatedAt`                           | `Date`                         | No       | `Date.now`       | Timestamp of last update                                         |


## Relationships

- **User (One-to-One)**: Each hostel admin is associated with one user profile via the `userId` reference.

## Usage

The HostelAdmin model is used to:
- Maintain information about the admin assigned to a student hostel
- Track the status (active, inactive, or on leave) of each admin
- Allow the hostel admin to manage tasks related to the hostel operations

## Model Registration

```javascript
export const HostelAdmin = mongoose.model('HostelAdmin', hostelAdminSchema);
```

## Database Considerations
### Indexing
Consider indexing the following fields:

- `email`: For fast lookups and ensuring uniqueness of email addresses

- `userId`: For associating and querying hostel admin data with the User model

### Validation & Integrity
- The schema uses built-in validation:

- Required userId and email fields for data integrity

- Enum validation on status to ensure valid values (active, inactive, on-leave)

### Performance Considerations
- `userId` should be indexed to speed up queries when joining with the User model.

- The schema is simple, but performance may degrade if more nested fields or complex queries are added.

