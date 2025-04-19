# Feedback Models 

This document provides a detailed description of the `Feedback` and `GlobalFeedbackConfig` schemas used to manage the feedback process between students and faculty in a course.

---

## Feedback Model

### Schema Definition

```ts
import mongoose from 'mongoose';

const feedbackSchema = new mongoose.Schema({
  student: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
    ref: 'Student',
  },
  faculty: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
    ref: 'Faculty',
  },
  course: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
    ref: 'Course',
  },
  isActive: {
    type: Boolean,
    default: true,
  },
  ratings: [
    {
      questionId: {
        type: String,
        required: true,
      },
      rating: {
        type: Number,
        required: true,
        min: 1,
        max: 5,
      },
    },
  ],
  comments: {
    type: String,
    trim: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

feedbackSchema.index(
  { student: 1, course: 1, faculty: 1 },
  { unique: true }
);

export const Feedback = mongoose.model('Feedback', feedbackSchema);
```

### Fields

| Field         | Type                          | Required | Default      | Description                                     |
|---------------|-------------------------------|----------|--------------|-------------------------------------------------|
| `student`     | `ObjectId` (ref: `Student`)   | Yes      | -            | ID of the student submitting the feedback       |
| `faculty`     | `ObjectId` (ref: `Faculty`)   | Yes      | -            | ID of the faculty receiving the feedback        |
| `course`      | `ObjectId` (ref: `Course`)    | Yes      | -            | ID of the course associated with the feedback   |
| `isActive`    | `Boolean`                     | No       | `true`       | Indicates if the feedback is active             |
| `ratings`     | `Array<Object>`               | Yes      | -            | Array of question-wise ratings                  |
| `questionId`  | `String`                      | Yes      | -            | Unique identifier for a feedback question       |
| `rating`      | `Number` (1-5)                | Yes      | -            | Rating given to the question                    |
| `comments`    | `String`                      | No       | -            | Additional comments from the student            |
| `createdAt`   | `Date`                        | No       | `Date.now`   | When feedback was created                       |
| `updatedAt`   | `Date`                        | No       | `Date.now`   | When feedback was last updated                  |

### Indexing
- Compound index on `(student, course, faculty)` to ensure uniqueness per feedback submission.

### Relationships
- `student` references the `Student` model.
- `faculty` references the `Faculty` model.
- `course` references the `Course` model.

### Use Cases
- Allows students to submit feedback for a specific course and faculty.
- Ensures one feedback submission per student per course-faculty combination.
- Can be toggled with `isActive` to enable/disable feedback collection dynamically.

### Database Considerations
- Compound index enhances lookup performance and enforces logical constraints.
- Feedback records are time-stamped to support analytics and audit trails.

---

## GlobalFeedbackConfig Model

### Schema Definition

```ts
const globalFeedbackConfigSchema = new mongoose.Schema({
  isActive: {
    type: Boolean,
    default: true,
    required: true
  },
  lastUpdated: {
    type: Date,
    default: Date.now
  }
});

globalFeedbackConfigSchema.statics.getConfig = async function() {
  let config = await this.findOne();
  if (!config) config = await this.create({});
  return config;
};

export const GlobalFeedbackConfig = mongoose.model(
  'GlobalFeedbackConfig', 
  globalFeedbackConfigSchema
);
```

### Fields

| Field         | Type      | Required | Default    | Description                                 |
|---------------|-----------|----------|------------|---------------------------------------------|
| `isActive`    | `Boolean` | Yes      | `true`     | Indicates whether global feedback is open   |
| `lastUpdated` | `Date`    | No       | `Date.now` | Timestamp when config was last updated      |

### Use Cases
- Toggle feedback collection system-wide using a single document.
- Useful for administrators to open/close the feedback period.

### Database Considerations
- `getConfig` ensures a singleton config document by creating one if none exists.
- Time-stamping helps admins track changes to global settings.

---

## Model Registration

```ts
const Feedback = mongoose.model("Feedback", feedbackSchema);
const GlobalFeedbackConfig = mongoose.model("GlobalFeedbackConfig", globalFeedbackConfigSchema);
```

---