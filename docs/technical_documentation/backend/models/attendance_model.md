
# Attendance Model

## Overview

This document outlines the structure and functionality of the `Attendance` model defined in the `attendance.model.js` file. The `Attendance` model tracks student attendance records for specific courses.

## Schema Definition

```javascript
const attendanceSchema = new mongoose.Schema({
  courseCode: { 
    type: String,
    required: true, 
    ref: 'Course' 
  },
  rollNo: { 
    type: String, 
    required: true, 
    ref: 'Student' 
  },
  date: {
    type: Date, 
    required: true, 
    default: Date.now 
  },
  isPresent: { 
    type: Boolean, 
    required: true, 
    default: false 
  },
  isApproved: { 
    type: Boolean, 
    required: true, 
    default: false 
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

## Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| courseCode | String | Yes | - | Code of the course, references the `Course` model |
| rollNo | String | Yes | - | Roll number of the student, references the `Student` model |
| date | Date | Yes | Date.now | Date of the attendance entry |
| isPresent | Boolean | Yes | false | Indicates whether the student was present on the given date |
| isApproved | Boolean | Yes | false | Indicates whether the attendance record has been approved by the instructor/admin |
| createdAt | Date | No | Date.now | Timestamp when the record was created |
| updatedAt | Date | No | Date.now | Timestamp when the record was last updated |

## Relationships

- **Course (Many-to-One)**: Each attendance record is associated with one course.
- **Student (Many-to-One)**: Each attendance record is associated with one student.

## Usage

The `Attendance` model is used to:

- Record student attendance for each course session.
- Track whether students were present or absent.
- Enable approval workflows for attendance validation by course instructors or administrators.

## Model Registration

```javascript
export const Attendance = mongoose.model('Attendance', attendanceSchema);
```

This statement registers the model with Mongoose for use across the application.

## Database Considerations

### Indexing

- Consider indexing `courseCode`, `rollNo`, and `date` fields for faster queries when checking attendance records by course, student, or session.

### Data Validation

The schema enforces:

- Required fields for key data like course, student, and attendance status.
- Default values for timestamp and boolean fields to ensure consistency and simplicity when inserting new records.

### Performance Considerations

- Frequent updates to `isApproved` or `isPresent` may require efficient write performance.
- Bulk attendance insertions can be optimized by batching requests.
