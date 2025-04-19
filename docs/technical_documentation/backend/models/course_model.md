
# Course Management Models

## Overview

This document outlines the Mongoose schemas used in the course management system. It includes models for courses, student course enrollments, faculty assignments, course registrations, program-course mappings, and approval requests.

## Models

### Course Model

Represents the details of a course offered by a department.

#### Schema Definition

```javascript
const courseSchema = new mongoose.Schema({
    courseCode: { type: String, required: true, unique: true },
    courseName: { type: String, required: true },
    department: { type: String, required: true },
    slot: { type: String, required: true },
    announcements: [{
        id: { type: mongoose.Schema.Types.ObjectId, auto: true },
        title: { type: String, required: true },
        content: { type: String, required: true },
        importance: { type: String, enum: ['Low', 'Medium', 'High', 'Critical'], default: 'Medium' },
        date: { type: Date, default: Date.now },
        postedBy: { type: String, ref: 'Faculty' },
        attachments: [{ name: String, url: String }]
    }],
    students: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Student' }],
    credits: { type: Number, required: true, default: 6 },
    maxIntake: { type: Number, required: true, default: 100 },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
});
```

#### Key Fields

- `courseCode`: Unique identifier for the course.
- `announcements`: Embedded array of announcements with importance, title, content, and attachments.
- `students`: References to enrolled student IDs.

---

### StudentCourse Model

Represents the mapping between a student and a course enrollment.

```javascript
const studentCourseSchema = new mongoose.Schema({
    rollNo: { type: String, required: true, ref: 'Student' },
    courseId: { type: String, required: true, ref: 'Course' },
    creditOrAudit: { type: String, enum: ['Credit', 'Audit'], required: true },
    semester: { type: String, required: true },
    status: { type: String, enum: ['Approved', 'Pending'], default: 'Pending' },
    grade: { type: String, default: null },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
    isCompleted: { type: Boolean, default: false },
});
```

- Maps a course enrollment for a student.
- Tracks status, completion, and grade.

---

### FacultyCourse Model

Defines which faculty teaches which course during which session.

```javascript
export const facultyCourseSchema = new mongoose.Schema({
    facultyId: { 
        type: String, 
        required: true, 
        ref: 'Faculty' 
    },
    courseCode: { 
        type: String, 
        required: true, 
        ref: 'Course' 
    },
    year: { 
        type: Number, 
        required: true 
    },
    session: { 
        type: String, 
        enum: ['Winter Semester', 'Spring Semester', 'Summer Course'], 
        required: true 
    },
    status: { 
        type: String, 
        enum: ['Ongoing', 'Completed'], 
        default: 'Ongoing' 
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

- Helps track faculty-course allocation and teaching status.

---

### CourseRegistration Model

Temporary model representing a student's course registration submission.

```javascript
const courseRegistrationSchema = new mongoose.Schema({
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
    creditOrAudit: { 
        type: String, 
        enum: ['Credit', 'Audit'], 
        required: true 
    },
    semester: { 
        type: String, 
        required: true 
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

- Used during the registration phase before approval.

---

### ProgramCourseMapping Model

Specifies which course is mapped to which program and academic term.

```javascript
const programCourseMappingSchema = new mongoose.Schema({
    courseCode: { 
        type: String, 
        required: true, 
        ref: 'Course' 
    },
    program: { 
        type: String, 
        required: true 
    },
    department: { 
        type: String, 
        required: true 
    },
    year: { 
        type: Number, 
        required: true 
    },
    semester: { 
        type: String, 
        required: true 
    },
    type: { 
        type: String, 
        enum: ['Core', 'Elective'], 
        required: true 
    }
});
```

- Useful for filtering courses relevant to a student’s curriculum.

---

### CourseApprovalRequest Model

Stores approval requests for students registering to courses.

```javascript
const courseApprovalRequestSchema = new mongoose.Schema({
    studentId: { 
        type: mongoose.Schema.Types.ObjectId, 
        ref: 'Student', 
        required: true 
    },
    courseCode: { 
        type: String, 
        required: true, 
        ref: 'Course' 
    },
    courseType: { 
        type: String, 
        enum: ['Core', 'Elective', 'Audit'], 
        required: true 
    },
    status: { 
        type: String, 
        enum: ['Pending', 'Approved', 'Rejected'], 
        default: 'Pending' 
    },
    createdAt: { 
        type: Date,
        default: Date.now
    },
});
```

- Tracks course approval requests with their status.

## Model Registration

```javascript
export const Course = mongoose.model('Course', courseSchema);

export const StudentCourse = mongoose.model('StudentCourse', studentCourseSchema);

export const FacultyCourse = mongoose.model('FacultyCourse', facultyCourseSchema);

export const CourseRegistration = mongoose.model('CourseRegistration', courseRegistrationSchema);

export const ProgramCourseMapping = mongoose.model('ProgramCourseMapping', programCourseMappingSchema);

export const CourseApprovalRequest = mongoose.model('CourseApprovalRequest', courseApprovalRequestSchema);
```

Each model is registered with Mongoose and exported for use in the rest of the application.

## Database Considerations

### Indexing

- Ensure `courseCode`, `rollNo`, `facultyId`, and other references are indexed for performance.
- Embedded documents like announcements should be monitored for size.
- Schema defaults and enums ensure consistent and valid data.

### Data Validation

The models incorporate several built-in validation strategies:

- Use of `required` flags ensures critical fields are always provided.
- `enum` values restrict fields like status or course type to valid entries, improving data consistency.
- Defaults (e.g., for timestamps and status) ensure predictable initial values.
- Unique constraints like on `courseCode` help prevent data duplication.

### Performance Considerations

- Arrays such as `Course.students` and `Course.announcements` can grow large; pagination or limit mechanisms should be used in production scenarios.
- Virtual population of announcements or related student info can improve performance when large documents are not always necessary.
- Keeping track of timestamps (`createdAt`, `updatedAt`) can help with audit logging and optimization.

