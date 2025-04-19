
# Academic Admin Model

## Overview

This document describes the data model used for managing Academic Administrators in the system. The `AcadAdmin` model defines the structure and relationships for storing information about academic administrators.

## Model

### AcadAdmin Model

The `AcadAdmin` model represents academic administrators within the system.

#### Schema Definition

```javascript
import mongoose from 'mongoose';

const acadAdminSchema = new mongoose.Schema({
  userId: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'User', 
    required: true 
  },
  designation: { 
    type: String, 
    required: true 
  },
  qualifications: [{ 
    type: String 
  }],    
  email: { 
    type: String, 
    required: true, 
    unique: true 
  },
  status: { 
    type: String, 
    enum: ['active', 'inactive', 'on-leave'], 
    default: 'active' 
  },
  createdAt: { 
    type: Date, 
    default: Date.now 
  },
  updatedAt: { 
    type: Date, 
    default: Date.now 
  }
});
```

#### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| userId | ObjectId | Yes | - | ID of the user who is the academic administrator, references the User model |
| designation | String | Yes | - | Designation or role of the academic administrator |
| qualifications | [String] | No | [] | List of qualifications or degrees held by the administrator |
| email | String | Yes | - | Email address of the academic administrator (must be unique) |
| status | String | No | 'active' | Current status of the administrator (active/inactive/on-leave) |
| createdAt | Date | No | Date.now | Timestamp when the administrator record was created |
| updatedAt | Date | No | Date.now | Timestamp when the administrator record was last updated |

#### Relationships

- **User (One-to-One)**: Each academic administrator is associated with one user in the system.

#### Usage

The AcadAdmin model is used to:
- Store details of academic administrators, including their role, qualifications, and contact information
- Track the status (active, inactive, on-leave) of administrators
- Maintain timestamps for creation and updates of administrator records

## Model Registration

```javascript
export const AcadAdmin = mongoose.model('AcadAdmin', acadAdminSchema);
```

The `AcadAdmin` model is registered with Mongoose and exported for use throughout the application.

## Database Considerations

### Indexing

Ensure indexing on the following fields for performance optimization:
- `AcadAdmin.userId`: Indexed for quick retrieval and association with user details
- `AcadAdmin.email`: Unique index to enforce email uniqueness constraint

### Data Validation

The schema includes validation to ensure data integrity:
- Required fields (`userId`, `designation`, `email`) to enforce mandatory data entry
- Default values (`status`) to ensure consistent initialization

### Performance Considerations

- Minimal denormalization to avoid redundancy
- Efficient querying through indexed fields
- Careful management of updates to maintain data integrity and consistency
