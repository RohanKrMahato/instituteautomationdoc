
# Assignment Model

## Overview

This document describes the data model used for managing assignments and their submissions in the academic system. The `Assignment` model includes both assignment metadata and embedded student submissions.

## Model

### Assignment Model

The `Assignment` model represents course assignments and the submissions made by students.

#### Schema Definition

```javascript
// Embedded Submission Schema
const submissionSchema = new mongoose.Schema({
  studentRollNo: {
    type: String,
    required: true,
    ref: 'Student' // reference by rollNo
  },
  studentName: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  submittedAt: {
    type: Date,
    default: Date.now
  }
}, { _id: false });

// Main Assignment Schema
const assignmentSchema = new mongoose.Schema({
  assignmentNumber: {
    type: Number,
    required: true,
  },
  courseCode: {
    type: String,
    required: true,
    ref: 'Course'
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String
  },
  dueDate: {
    type: Date,
    required: true
  },
  submissions: [submissionSchema],
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

#### Fields (Assignment Schema)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| assignmentNumber | Number | Yes | - | Identifier for the assignment |
| courseCode | String | Yes | - | Code of the course the assignment belongs to, references the Course model |
| title | String | Yes | - | Title of the assignment |
| description | String | No | - | Detailed description of the assignment |
| dueDate | Date | Yes | - | Deadline for submitting the assignment |
| submissions | [submissionSchema] | No | [] | List of student submissions embedded in the assignment document |
| createdAt | Date | No | Date.now | Timestamp when the assignment was created |
| updatedAt | Date | No | Date.now | Timestamp when the assignment was last updated |

#### Fields (Submission Schema)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| studentRollNo | String | Yes | - | Roll number of the student submitting the assignment |
| studentName | String | Yes | - | Full name of the student |
| content | String | Yes | - | Content or answer submitted by the student |
| submittedAt | Date | No | Date.now | Timestamp when the student submitted the assignment |

#### Relationships

- **Course (Many-to-One)**: Each assignment belongs to one course.
- **Student (Embedded, One-to-Many)**: Each assignment may contain multiple student submissions.

#### Usage

The Assignment model is used to:
- Store assignment details for different courses
- Track and manage student submissions for each assignment
- Enforce submission deadlines and store submission timestamps

## Model Registration

```javascript
export const Assignment = mongoose.model('Assignment', assignmentSchema);
```

The `Assignment` model is registered with Mongoose and exported for use throughout the application.

## Database Considerations

### Indexing

Indexing may be beneficial on the following fields:
- `assignmentNumber` and `courseCode` for querying assignments by course and number
- `submissions.studentRollNo` for efficient lookups of specific student submissions

### Data Validation

The schema includes validation mechanisms:
- Required fields for both assignment and submission schemas
- Embedded submission schema for encapsulated submission data
- Default values for timestamps

### Performance Considerations

- Embedded submissions reduce the need for joins but could grow large for popular courses
- Updates to submission content require writing to the entire assignment document
- Embedded documents allow atomic updates to a student's submission for a given assignment
