
# Student Model

## Overview

This document describes the data model used for storing student information in the application. The `Student` model extends the base user functionality with academic, residential, and document access information, and is defined in the `student.model.js` file.

## Model

### Student Model

The `Student` model represents a student enrolled at the institution and includes both personal and academic attributes.

#### Schema Definition

```javascript
const studentSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  email: { type: String, required: true, unique: true },
  rollNo: { type: String, unique: true, required: true },
  fatherName: { type: String, required: true },
  motherName: { type: String, required: true },
  department: { type: String, required: true },
  semester: { type: Number, required: true, default: 1 },
  batch: { type: String, required: true },
  program: { type: String, enum: ['BTech', 'MTech', 'PhD', 'BDes', 'MDes'], required: true },
  status: { 
    type: String, 
    enum: ['active', 'inactive', 'graduated', 'suspended'], 
    default: 'active' 
  },
  hostel: {
    type: String,
    enum: ['Brahmaputra', 'Lohit', 'Disang', 'Subansiri', 'Dhansiri', 'Kapili', 'Manas', 'Dihing', 'Barak', 'Siang', 'Kameng', 'Umiam', 'Married Scholar'],
    required: true
  },
  documentAccess: {
    transcript: { type: Boolean, default: true },
    idCard: { type: Boolean, default: true },
    feeReceipt: { type: Boolean, default: true }
  },
  roomNo: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});
```

#### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| userId | ObjectId | Yes | - | Reference to the User model |
| email | String | Yes | - | Student's email (must be unique) |
| rollNo | String | Yes | - | Unique roll number assigned to the student |
| fatherName | String | Yes | - | Father's name |
| motherName | String | Yes | - | Mother's name |
| department | String | Yes | - | Department of the student |
| semester | Number | Yes | 1 | Current semester of the student |
| batch | String | Yes | - | Batch year or code |
| program | String | Yes | - | Academic program (BTech, MTech, etc.) |
| status | String | No | 'active' | Current academic status of the student |
| hostel | String | Yes | - | Name of the hostel student resides in |
| documentAccess.transcript | Boolean | No | true | Access to transcript document |
| documentAccess.idCard | Boolean | No | true | Access to ID card |
| documentAccess.feeReceipt | Boolean | No | true | Access to fee receipt |
| roomNo | String | Yes | - | Room number in the hostel |
| createdAt | Date | No | Date.now | Timestamp of student record creation |
| updatedAt | Date | No | Date.now | Timestamp of last update |

#### Relationships

- **User (One-to-One)**: Each student is associated with one user profile via the `userId` reference.

#### Usage

The Student model is used to:
- Extend user information with academic and hostel details
- Track student semester, batch, and program information
- Control access to documents like transcripts and ID cards
- Manage room assignments within hostels

## Model Registration

```javascript
export const Student = mongoose.model('Student', studentSchema);
```

The model is registered with Mongoose and exported for use throughout the application.

## Database Considerations

### Indexing

Consider indexing the following fields:
- `email`: For fast lookups and uniqueness validation
- `rollNo`: For efficient queries using student roll numbers
- `userId`: For joining with user-related data

### Validation & Integrity

The schema uses built-in validation:
- Required fields for data integrity
- Enums for program, hostel, and status values
- Unique constraints on `email` and `rollNo`

### Performance Considerations

- Keep an eye on nested document structures (`documentAccess`) as complexity grows
- Ensure `userId` reference integrity when creating or deleting related `User` records
