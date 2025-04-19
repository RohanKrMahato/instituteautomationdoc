# HostelLeave & HostelTransfer Model 

This document provides a structured overview of the `HostelLeave` and `HostelTransfer` schemas used in the application for managing hostel-related requests submitted by students.

---

## HostelLeave Schema

```ts
import mongoose from "mongoose";

const hostelLeaveSchema = new mongoose.Schema({
  rollNo: { type: String, required: true, ref: 'Student' },
  startDate: { type: Date, required: true },
  endDate: { type: Date, required: true },
  reason: { type: String, required: true },
  status: { 
    type: String, 
    required: true, 
    enum: ['Pending', 'Approved', 'Rejected'], 
    default: 'Pending' 
  },
  remarks: { type: String },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

export const HostelLeave = mongoose.model('HostelLeave', hostelLeaveSchema);
```

### Fields

| Field         | Type         | Required | Default      | Description                                                         |
|---------------|--------------|----------|--------------|---------------------------------------------------------------------|
| `rollNo`      | `String`     | Yes      | -            | Reference to the student who applied for leave                     |
| `startDate`   | `Date`       | Yes      | -            | Start date of the leave                                             |
| `endDate`     | `Date`       | Yes      | -            | End date of the leave                                               |
| `reason`      | `String`     | Yes      | -            | Reason for the leave                                                |
| `status`      | `String`     | Yes      | `Pending`     | Status of the leave request (`Pending`, `Approved`, or `Rejected`) |
| `remarks`     | `String`     | No       | -            | Additional comments or remarks by admin                            |
| `createdAt`   | `Date`       | No       | `Date.now`   | Timestamp of request creation                                       |
| `updatedAt`   | `Date`       | No       | `Date.now`   | Timestamp of last update                                           |

### Relationships

- **Student (Many-to-One)**: Each leave record is associated with a student through their roll number.

---

## HostelTransfer Schema

```ts
import mongoose from "mongoose";

const hostelTransferSchema = new mongoose.Schema({
  rollNo: { type: String, required: true, ref: 'Student' },
  currentHostel: {
    type: String,
    enum: ['Brahmaputra', 'Lohit', 'Disang', 'Subansiri', 'Dhansiri', 'Kapili', 'Manas', 'Dihing', 'Barak', 'Siang', 'Kameng', 'Umiam', 'Married Scholar'],
    required: true
  },
  requestedHostel: {
    type: String,
    enum: ['Brahmaputra', 'Lohit', 'Disang', 'Subansiri', 'Dhansiri', 'Kapili', 'Manas', 'Dihing', 'Barak', 'Siang', 'Kameng', 'Umiam', 'Married Scholar'],
    required: true
  },
  reason: { type: String, required: true },
  status: { 
    type: String, 
    required: true, 
    enum: ['Pending', 'Approved', 'Rejected'], 
    default: 'Pending' 
  },
  remarks: { type: String },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

export const HostelTransfer = mongoose.model('HostelTransfer', hostelTransferSchema);
```

### Fields

| Field             | Type     | Required | Default     | Description                                                                 |
|-------------------|----------|----------|-------------|-----------------------------------------------------------------------------|
| `rollNo`          | `String` | Yes      | -           | Reference to the student requesting hostel transfer                         |
| `currentHostel`   | `String` | Yes      | -           | Student's current hostel                                                    |
| `requestedHostel` | `String` | Yes      | -           | Hostel the student wants to transfer to                                     |
| `reason`          | `String` | Yes      | -           | Justification for transfer                                                  |
| `status`          | `String` | Yes      | `Pending`   | Status of the transfer request (`Pending`, `Approved`, or `Rejected`)       |
| `remarks`         | `String` | No       | -           | Admin remarks on the request                                                |
| `createdAt`       | `Date`   | No       | `Date.now`  | Timestamp of request creation                                               |
| `updatedAt`       | `Date`   | No       | `Date.now`  | Timestamp of last update                                                    |

### Relationships

- **Student (Many-to-One)**: Each transfer record is linked to a student via their roll number.

---

## Model Registration

```ts
export const HostelLeave = mongoose.model('HostelLeave', hostelLeaveSchema);
export const HostelTransfer = mongoose.model('HostelTransfer', hostelTransferSchema);
```

## Usage

These models are used to:
- Allow students to apply for hostel leave or transfer
- Track application status and manage workflow (approve/reject)
- Provide hostel admins an interface to manage and respond to student requests

## Database Considerations

### Indexing
- `rollNo`: Should be indexed for fast lookup of student-related requests.

### Validation & Integrity
- Built-in validation ensures:
  - All required fields are filled
  - `status` values are restricted to allowed enums

### Performance Notes
- The schemas are lightweight and should scale well under moderate usage.
- Avoid excessive nesting or complex joins to keep operations efficient.

---