# Faculty Model

## Overview

This document outlines the schema structure for the `Faculty` model defined in the system. The model manages data pertaining to faculty members, including their profile information, academic contributions, and associated courses.

## Schema Definition

```javascript
const facultySchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  email: { type: String, required: true, unique: true },
  department: { type: String, required: true },
  designation: { type: String, required: true },
  yearOfJoining: { type: Number },
  courses:  [facultyCourseSchema],
  specialization: { type: String },
  qualifications: [{ type: String }],
  experience: [{ type: String }],
  publications: [{ type: String }],
  researchStudents:[{ type: String }],
  achievements: [{ type: String }],
  conferences: [
    {
      name: { type: String },
      year: { type: String },
      role: { type: String },
    }
  ],
  status: { 
    type: String, 
    enum: ['active', 'inactive', 'on-leave'], 
    default: 'active' 
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});
```

## Fields

| Field            | Type                         | Required | Default      | Description |
|------------------|------------------------------|----------|--------------|-------------|
| userId           | ObjectId (ref: 'User')       | Yes      | -            | Reference to the associated user account |
| email            | String                       | Yes      | -            | Unique email ID of the faculty member |
| department       | String                       | Yes      | -            | Department the faculty belongs to |
| designation      | String                       | Yes      | -            | Official designation/title of the faculty |
| yearOfJoining    | Number                       | No       | -            | Year the faculty joined the institution |
| courses          | [facultyCourseSchema]        | No       | []           | List of courses handled, uses external schema |
| specialization   | String                       | No       | -            | Area of academic/research specialization |
| qualifications   | [String]                     | No       | []           | Academic qualifications held |
| experience       | [String]                     | No       | []           | Experience descriptions or entries |
| publications     | [String]                     | No       | []           | List of publications |
| researchStudents | [String]                     | No       | []           | Research students mentored |
| achievements     | [String]                     | No       | []           | List of academic or professional achievements |
| conferences      | [Object]                     | No       | []           | Conference participation details |
| ├─ name          | String                       | No       | -            | Name of the conference |
| ├─ year          | String                       | No       | -            | Year of participation |
| └─ role          | String                       | No       | -            | Role played in the conference (e.g., Speaker) |
| status           | String                       | No       | 'active'     | Employment status: active, inactive, or on-leave |
| createdAt        | Date                         | No       | Date.now     | Record creation timestamp |
| updatedAt        | Date                         | No       | Date.now     | Last updated timestamp |

## Relationships

- **User (One-to-One)**: Each faculty is linked to a single `User` object, enabling authentication and access control.
- **Courses (Embedded Subdocument)**: The `courses` field references an external schema `facultyCourseSchema` and holds data about the courses taught by the faculty.

## Usage

The `Faculty` model is used to:
- Maintain detailed faculty profiles
- Track teaching and research activities
- Record participation in conferences and other professional events

## Schema Considerations

### Indexing

- `email`: Unique index for quick lookups and to enforce uniqueness

### Data Validation

- Required fields ensure basic profile integrity
- Enum types restrict status values to allowed categories

### Performance Notes

- Embedded arrays like `courses`, `qualifications`, and `publications` should be monitored for excessive growth in high-volume systems
- Denormalization is avoided by using references where appropriate (e.g., `userId`)

## Model Registration

```javascript
export const Faculty = mongoose.model('Faculty', facultySchema);
```

## Database Considerations

### Indexing
- `email`: Indexed and unique to prevent duplicate entries and to speed up email-based lookups.
- `userId`: Indexed to allow faster joins and lookups in authentication contexts.

### Data Validation
- The schema enforces validation via `required`, `enum`, and `unique` constraints to ensure data consistency.

## Performance
- Integrate soft deletion using a `isDeleted` or `deletedAt` field.
- Introduce a `profilePicture` field for enhanced faculty profile visibility.
- Add `officeHours` or `availability` for student interaction scheduling.
- Define virtuals for computed data like `totalExperience` based on `experience[]` entries.



