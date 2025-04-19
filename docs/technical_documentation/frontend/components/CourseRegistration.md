# CourseRegistration Component

## Overview

The `CourseRegistration` component is a React-based front-end module designed to facilitate course registration for students at an academic institution (e.g., IIT Guwahati). It allows users to view and register for core courses, select and register for elective courses, and choose audit courses. The component uses static course data and manages selections with **React state**, styled with **Tailwind CSS** for a clean and responsive interface. The registration functionality is currently a placeholder (buttons are non-functional), indicating a prototype or partial implementation.

## Dependencies

- **React**: For building the UI and managing state.
  - `useState`: Manages selected elective and audit courses.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `CourseRegistration` component is divided into three sections:

1. **Core Courses**: Displays a list of mandatory courses with placeholder "Register" buttons.
2. **Elective Courses**: Allows selection of two elective courses via dropdowns with conditional "Register" buttons.
3. **Audit Courses**: Allows selection of three audit courses via dropdowns with conditional "Register" buttons.

## Code Explanation

### Imports

```jsx
import { useState } from "react";
```

- **React**:
  - `useState`: Used to manage the state of selected elective and audit courses.
- No other dependencies (e.g., React Router, Context) are imported, indicating a standalone component.

### Data and State

```jsx
const coreCourses = ["Data Structures", "Operating Systems", "Computer Networks"];
const electiveCourses = ["AI", "Cyber Security", "Cloud Computing", "Blockchain", "Data Science"];
const auditCourses = ["Ethics in AI", "Financial Management", "Psychology", "Machine Learning", "Leadership", "Philosophy", "Environmental Science", "Digital Marketing", "Robotics", "Astronomy"];

const [selectedElectives, setSelectedElectives] = useState(["", ""]);
const [selectedAudits, setSelectedAudits] = useState(["", "", ""]);
```

- **Course Lists**:
  - `coreCourses`: Array of 3 mandatory courses.
  - `electiveCourses`: Array of 5 elective courses.
  - `auditCourses`: Array of 10 audit courses.
  - All are static arrays, suggesting mock data for development.
- **State**:
  - `selectedElectives`: Array of 2 strings (initially empty `["", ""]`), tracking selected elective courses.
  - `selectedAudits`: Array of 3 strings (initially empty `["", "", ""]`), tracking selected audit courses.
  - Fixed lengths (2 for electives, 3 for audits) enforce a maximum number of selections.

### Handlers

```jsx
const handleElectiveChange = (index, course) => {
  let updatedElectives = [...selectedElectives];
  updatedElectives[index] = course;
  setSelectedElectives(updatedElectives);
};

const handleAuditChange = (index, course) => {
  let updatedAudits = [...selectedAudits];
  updatedAudits[index] = course;
  setSelectedAudits(updatedAudits);
};
```

- **handleElectiveChange**:
  - Updates the `selectedElectives` array at the specified `index` with the selected `course`.
  - Uses spread operator (`[...selectedElectives]`) to create a new array, ensuring immutability.
- **handleAuditChange**:
  - Similar to `handleElectiveChange`, updates `selectedAudits` at the specified `index`.
- Both functions are triggered by `<select>` element changes and maintain the fixed-length arrays.

### Rendering

```jsx
return (
  <div className="p-5">
    <h2 className="text-xl font-bold mb-4">Course Registration</h2>

    {/* Core Courses Section */}
    <h3 className="text-lg font-semibold mb-2">Core Courses</h3>
    <ul className="mb-4">
      {coreCourses.map((course) => (
        <li key={course} className="flex justify-between p-2 border-b">
          {course}
          <button className="bg-blue-500 text-white px-3 py-1 rounded">Register</button>
        </li>
      ))}
    </ul>

    {/* Elective Courses Section */}
    <h3 className="text-lg font-semibold mb-2">Elective Courses</h3>
    {selectedElectives.map((selected, index) => (
      <div key={index} className="flex justify-between p-2 border-b">
        <select
          className="border p-2 w-1/4"
          onChange={(e) => handleElectiveChange(index, e.target.value)}
          value={selected}
        >
          <option value="">Select Elective Course</option>
          {electiveCourses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>
        <button
          className={`px-3 py-1 rounded ${
            selected ? "bg-blue-500 text-white" : "bg-gray-300"
          }`}
          disabled={!selected}
        >
          Register
        </button>
      </div>
    ))}

    {/* Audit Courses Section */}
    <h3 className="text-lg font-semibold mt-4 mb-2">Audit Courses</h3>
    {selectedAudits.map((selected, index) => (
      <div key={index} className="flex justify-between p-2 border-b">
        <select
          className="border p-2 w-1/4"
          onChange={(e) => handleAuditChange(index, e.target.value)}
          value={selected}
        >
          <option value="">Select Audit Course</option>
          {auditCourses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>
        <button
          className={`px-3 py-1 rounded ${
            selected ? "bg-blue-500 text-white" : "bg-gray-300"
          }`}
          disabled={!selected}
        >
          Register
        </button>
      </div>
    ))}
  </div>
);
```

- **Container**:
  - A padded container (`p-5`) wrapping all sections.
- **Header**:
  - A bold title ("Course Registration") with large text (`text-xl`, `font-bold`).
- **Core Courses Section**:
  - Displays a list (`<ul>`) of core courses.
  - Each course is a list item (`<li>`) with the course name and a "Register" button.
  - Buttons are styled blue (`bg-blue-500`) but lack functionality (no `onClick` handler).
- **Elective Courses Section**:
  - Renders two dropdowns (`<select>`) based on `selectedElectives` length.
  - Each dropdown:
    - Lists all `electiveCourses` with a placeholder option ("Select Elective Course").
    - Updates `selectedElectives` via `handleElectiveChange`.
    - Has a fixed width (`w-1/4`).
  - Each dropdown is paired with a "Register" button:
    - Enabled (blue, `bg-blue-500`) if a course is selected (`selected` is non-empty).
    - Disabled (gray, `bg-gray-300`) if no course is selected.
    - Lacks functionality (no `onClick`).
- **Audit Courses Section**:
  - Similar to the elective section but renders three dropdowns based on `selectedAudits`.
  - Uses `handleAuditChange` for updates.
  - Same button logic and styling as electives.
- **Key Usage**:
  - `key={course}` for core courses and `key={index}` for electives/audits ensure unique React keys.
  - `value={selected}` ensures dropdowns reflect the current state.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Container**: Padded (`p-5`) for spacing.
  - **Headers**:
    - Main: Large, bold (`text-xl`, `font-bold`, `mb-4`).
    - Section: Slightly smaller, bold (`text-lg`, `font-semibold`, `mb-2`).
  - **Core Courses**:
    - List items: Flexbox (`flex justify-between`), padded (`p-2`), with bottom border (`border-b`).
    - Buttons: Blue (`bg-blue-500`), white text, padded (`px-3 py-1`), rounded (`rounded`).
  - **Elective/Audit Sections**:
    - Rows: Flexbox (`flex justify-between`), padded (`p-2`), with bottom border (`border-b`).
    - Dropdowns: Bordered (`border`), padded (`p-2`), 25% width (`w-1/4`).
    - Buttons: Conditional styling (`bg-blue-500` or `bg-gray-300`), padded, rounded.
  - **Spacing**: Margins (`mb-4`, `mt-4`) ensure clear section separation.

## Assumptions

- **Static Data**:
  - `coreCourses`, `electiveCourses`, and `auditCourses` are hardcoded, likely for prototyping.
  - Expected to be replaced with API data (e.g., `/api/courses`).
- **Course Limits**:
  - Exactly 2 electives and 3 audit courses are allowed, enforced by `selectedElectives` and `selectedAudits` lengths.
- **Registration**:
  - "Register" buttons are placeholders; actual registration requires backend integration.
- **No Validation**:
  - No checks for duplicate course selections (e.g., selecting "AI" twice).
  - No integration with a timetable (e.g., checking for slot conflicts).
- **Integration**:
  - Likely part of a larger system with components like `TimeTable` and `AssignmentLanding`.
  - Courses (e.g., "Data Structures") may align with `courses` data (`CS101`).

## Notes

- **Placeholder Functionality**:
  - "Register" buttons lack `onClick` handlers, indicating incomplete implementation.
- **Duplicate Selections**:
  - Users can select the same course multiple times in electives or audits, which may be undesirable.
- **No Submission**:
  - No mechanism to submit the selected courses to a backend.
- **Static Data**:
  - Hardcoded course lists limit flexibility; dynamic data would improve scalability.
- **No Feedback**:
  - No user feedback (e.g., toast notifications) for registration actions.
- **Accessibility**:
  - Lacks ARIA attributes for dropdowns and buttons.
- **Integration with TimeTable**:
  - Courses don’t reference slots (e.g., A, B from `TimeTable`), suggesting a need for timetable validation.

## Integration with Other Components

- **TimeTable**:
  - Courses should map to `activeCourses` (e.g., `Data Structures` to `CS101`) with slot information for conflict checking.
- **AssignmentLanding**:
  - Registered courses could link to `courses` data (e.g., `CS101` for assignments).
- **RoleContext**:
  - Could restrict registration to students and validate eligibility.

## Future Improvements

- **Dynamic Data**:
  - Fetch courses from an API.
- **Prevent Duplicates**:
  - Validate selections to avoid duplicate courses.
- **Timetable Integration**:
  - Check for slot conflicts using `TimeTable` data.
- **Submit All Selections**:
  - Add a "Submit Registration" button to send all selections.
- **Dynamic Course Limits**:
  - Allow configurable numbers of electives and audits.
- **Testing**:
  - Write unit tests for selection handling and registration logic.

