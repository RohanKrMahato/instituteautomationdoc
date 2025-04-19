# Data Component

## Overview

This module exports two static data arrays, `courses` and `assignments`, which represent course and assignment information for an academic institution (e.g., IIT Guwahati). The data appears to serve as a mock dataset, likely used for development or testing purposes in a front-end application managing course assignments and student submissions. The structure supports course listings and detailed assignment management, including submission tracking.

## Data Structure

### Courses

```javascript
export const courses = [
  { id: "ME101", name: "Engineering Mechanics", assignments: ["A1", "A2"] },
  { id: "CS101", name: "Introduction to Computing", assignments: ["A3", "A4"] },
  { id: "BT101", name: "Introduction to Biology", assignments: ["A5", "A6"] },
  { id: "CS201", name: "Discrete Mathematics", assignments: ["A7", "A8"] },
  { id: "AI101", name: "Artificial Intelligence", assignments: ["A9", "A10"] }
];
```

- **Purpose**: Represents a list of courses offered.
- **Structure**: Array of objects, each with:
  - `id`: Unique course identifier (e.g., `"ME101"`).
  - `name`: Descriptive course name (e.g., `"Engineering Mechanics"`).
  - `assignments`: Array of assignment IDs linked to the course (e.g., `["A1", "A2"]`).
- **Details**:
  - Contains 5 courses, each with exactly 2 assignments.
  - Course IDs follow a department-based naming convention (e.g., `ME` for Mechanical, `CS` for Computer Science, `BT` for Biotechnology, `AI` for Artificial Intelligence).

### Assignments

```javascript
export const assignments = [
  {
    id: "A1",
    course_id: "ME101",
    title: "Mastering Newton's Laws of Motion",
    description: "...",
    due_date: "2025-04-10",
    submissions: [
      { student_id: "S101", student_name: "Alice Johnson", file_name: "alice_newton.pdf", submitted_at: "2025-04-08 14:30" },
      { student_id: "S102", student_name: "Bob Smith", file_name: "bob_newton.docx", submitted_at: "2025-04-09 16:45" }
    ]
  },
  // ... 9 more assignments
];
```

- **Purpose**: Represents a list of assignments with associated submissions.
- **Structure**: Array of objects, each with:
  - `id`: Unique assignment identifier (e.g., `"A1"`).
  - `course_id`: Links to a course’s `id` (e.g., `"ME101"`).
  - `title`: Assignment title (e.g., `"Mastering Newton's Laws of Motion"`).
  - `description`: Detailed instructions for the assignment.
  - `due_date`: Submission deadline in `YYYY-MM-DD` format (e.g., `"2025-04-10"`).
  - `submissions`: Array of submission objects, each with:
    - `student_id`: Unique student identifier (e.g., `"S101"`).
    - `student_name`: Student’s full name (e.g., `"Alice Johnson"`).
    - `file_name`: Name of the submitted file (e.g., `"alice_newton.pdf"`).
    - `submitted_at`: Submission timestamp in `YYYY-MM-DD HH:mm` format (e.g., `"2025-04-08 14:30"`).
- **Details**:
  - Contains 10 assignments, matching the `assignments` arrays in `courses`.
  - Descriptions are detailed and tailored to the course discipline.
  - 5 assignments have submissions (1–2 per assignment), and 5 have none.
  - Submission timestamps are before the respective due dates.

## Usage Context

- **Relation to Other Components**:
  - The data aligns with components like `AssignmentLanding`, `AssignmentList`, `AssignmentDetail`, `CreateAssignment`, `EditAssignment`, and `FacultyAssignmentSubmissions`.
  - `courses` matches the structure expected by `AssignmentLanding` (uses `courseCode` as `id`, `courseName` as `name`).
  - `assignments` matches the structure used in `AssignmentList`, `AssignmentDetail`, and `FacultyAssignmentSubmissions` (uses `assignmentNumber` as `id`, includes `submissions`).
- **Mock Data**:
  - Likely used as a placeholder before integrating with a backend API (e.g., `http://localhost:8000/api/assignment/...`).
  - Replicates the API response format seen in `AssignmentDetail` and `FacultyAssignmentSubmissions`.

## Assumptions

- **Data Consistency**:
  - Every assignment ID in `courses.assignments` has a corresponding entry in `assignments`.
  - `course_id` in `assignments` matches an `id` in `courses`.
- **Frontend Integration**:
  - The data is imported into components for rendering course lists and assignment details.
  - Used in development to simulate API responses.
- **Submission Format**:
  - File-based submissions (`file_name`) suggest support for document uploads (e.g., PDF, DOCX, Python scripts).
  - Timestamps are in a readable format but may need parsing for display (e.g., via `Date`).
- **No Authentication**:
  - The data doesn’t include user roles or permissions, assuming role-based logic is handled elsewhere (e.g., `RoleContext`).


## Integration with Components

- **AssignmentLanding**:
  - Uses `courses` to display course cards with `id` as `courseCode` and `name` as `courseName`.
  - Could filter assignments from `assignments` based on `course_id` if expanded.
- **AssignmentList**:
  - Expects assignments with `course_id`, `title`, `description`, `due_date`, and `submissions`.
  - Matches `id` to `assignmentNumber`.
- **AssignmentDetail**:
  - Expects text-based `content` in submissions, requiring adaptation for `file_name`.
  - Uses `due_date` for deadline checks.
- **FacultyAssignmentSubmissions**:
  - Fully compatible, expecting `title`, `description`, `due_date`, and `submissions` with `studentName`, `studentRollNo`, `submittedAt`, and `content` (map `file_name` to `content`).
- **CreateAssignment/EditAssignment**:
  - Output matches `assignments` structure (`title`, `description`, `due_date`).

## Example Usage

```jsx
import { courses, assignments } from "./data";

const CourseList = () => (
  <div>
    {courses.map((course) => (
      <div key={course.id}>
        <h2>{course.name}</h2>
        <ul>
          {assignments
            .filter((a) => a.course_id === course.id)
            .map((a) => (
              <li key={a.id}>
                {a.title} - Due: {a.due_date}
                ({a.submissions.length} submissions)
              </li>
            ))}
        </ul>
      </div>
    ))}
  </div>
);
```

## Notes

- **Static Nature**:
  - Hardcoded data lacks dynamic updates (e.g., adding new assignments or submissions).
  - Suitable for prototyping but should be replaced with API calls in production.
- **File Submissions**:
  - `file_name` suggests file uploads, but components like `AssignmentDetail` handle text submissions (`content`), indicating a possible mismatch or incomplete file support.
- **Due Dates**:
  - All due dates are in April 2025, suggesting a future-oriented test dataset.
  - No validation for past due dates (handled in components like `AssignmentDetail`).
- **Submissions**:
  - Empty `submissions` arrays for half the assignments simulate varied states (submitted vs. pending).
  - No grading or feedback data, which might be expected for faculty views.
- **Naming Conventions**:
  - `id` in `courses` and `assignments` aligns with `courseCode` and `assignmentNumber` in components, but naming could be standardized.

## Future Improvements

- **Dynamic Data**:
  - Replace with API calls to fetch courses and assignments.
- **Standardize Naming**:
  - Rename `id` to `courseCode` in `courses` and `assignmentNumber` in `assignments` for consistency with components.
- **Add Grading**:
  - Include fields for grades or feedback in `submissions`.
- **File Support**:
  - Align with `AssignmentDetail`’s text-based submissions or add file handling:
- **Validation**:
  - Add checks for data integrity (e.g., ensure `course_id` exists in `courses`):
