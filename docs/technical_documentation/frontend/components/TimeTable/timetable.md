# TimeTable Component

## Overview

The `TimeTable` component is a React-based front-end module designed to display a weekly timetable in our  academic institution. It visualizes course schedules across days (Monday to Friday) and time slots (8:00 AM to 5:55 PM). The component uses a static dataset of courses with assigned slots and employs **Tailwind CSS** for styling to create a responsive and visually appealing table. The timetable supports both regular lecture slots (e.g., A, B, C) and lab slots (e.g., AL1, ML1) that span multiple time periods.

## Dependencies

- **React**: For building the UI and managing state.
- **Tailwind CSS**: For styling the timetable.

## Component Structure

The `TimeTable` component consists of:

1. **Header**: A centered title ("Time-Table").
2. **Table**: A responsive table displaying courses by day and time slot, with special handling for lab slots that span multiple columns.

## Code Explanation

### Imports

```jsx
import React, { useContext, useState } from 'react';
```

- **React**:
  - `useState`: Manages the static `activeCourses` data.
  - `useContext`: Imported but unused, suggesting potential future integration with a context (e.g., `RoleContext`).
- Note: The unused `useContext` import indicates possible plans for dynamic role-based course filtering.

### Data and State

```jsx
const timings = [
  "8:00 - 8:55", "9:00 - 9:55", "10:00 - 10:55", "11:00 - 11:55", "12:00 - 12:55",
  "1:00 - 1:55", "2:00 - 2:55", "3:00 - 3:55", "4:00 - 4:55", "5:00 - 5:55"
];

const [activeCourses] = useState([
  { id: "CS101", name: "Introduction to Computer Science", slot: "A" },
  { id: "MATH202", name: "Calculus II", slot: "B" },
  { id: "ENG105", name: "Academic Writing", slot: "C" },
  { id: "PHYS101", name: "Physics for Engineers", slot: "D" },
  { id: "PHYS102", name: "Physics for Engineers", slot: "E" },
  { id: "PHYS103", name: "Physics for Engineers", slot: "F" },
  { id: "PHYS104", name: "Physics for Engineers", slot: "G" },
  { id: "PHYS105", name: "Physics for Engineers", slot: "AL1" },
  { id: "PHYS106", name: "Physics for Engineers", slot: "AL2" },
  { id: "PHYS107", name: "Physics for Engineers", slot: "AL3" },
  { id: "PHYS108", name: "Physics for Engineers", slot: "AL4" },
  { id: "PHYS109", name: "Physics for Engineers", slot: "AL5" },
]);
```

- **Timings**:
  - An array of 10 hourly time slots from 8:00 AM to 5:55 PM, used as column headers.
- **Active Courses**:
  - A static state array of course objects, each with:
    - `id`: Unique course identifier (e.g., `"CS101"`).
    - `name`: Course name (e.g., `"Introduction to Computer Science"`).
    - `slot`: Timetable slot (e.g., `"A"`, `"AL1"`).
  - Contains 12 courses, with slots for regular lectures (A–G) and labs (AL1–AL5).
  - The commented-out alternative dataset uses different slot names (e.g., `A1`, `ML1`), suggesting flexibility in slot naming conventions.
- **State**:
  - `useState` is used but the data is static (never updated), indicating potential for dynamic data in the future.

### Slot Mapping

```jsx
const slotToCourseMap = activeCourses.reduce((map, course) => {
  map[course.slot] = course.id;
  return map;
}, {});
```

- Creates an object mapping slot names to course IDs (e.g., `{ "A": "CS101", "AL1": "PHYS105" }`).
- Used to quickly look up course IDs for each slot when rendering the table.
- Simplifies table cell population by avoiding repeated array searches.

### Rendering

```jsx
return (
  <>
    <div className="flex justify-center py-6">
      <h3 className="text-3xl font-bold text-gray-800">Time-Table</h3>
    </div>
    <div className="p-4">
      <div className="overflow-x-auto rounded-lg shadow-md bg-white">
        <table className="min-w-full text-center">
          <thead className="bg-gradient-to-r from-blue-500 to-green-500 text-white">
            <tr>
              <th className="px-6 py-4 text-lg font-semibold border-b border-gray-200">Day / Time</th>
              {timings.map((timing, index) => (
                <th key={index} className="px-6 py-4 text-md border-b border-gray-200">
                  {timing}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="text-gray-700">
            {/* Monday */}
            <tr className="hover:bg-gray-100 transition-all">
              <td className="bg-gradient-to-r from-blue-500 to-green-500 text-white font-bold px-6 py-4 border-b">
                Monday
              </td>
              <td className="px-6 py-4 border-b">{slotToCourseMap["A"]}</td>
              {slotToCourseMap["ML1"] === undefined ? (
                <>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["B"]}</td>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["C"]}</td>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["D"]}</td>
                </>
              ) : (
                <td colSpan="3" className="px-6 py-4 border-b">{slotToCourseMap["ML1"]}</td>
              )}
              <td className="px-6 py-4 border-b">{slotToCourseMap["F"]}</td>
              <td className="px-6 py-4 border-b">{slotToCourseMap["F1"]}</td>
              {slotToCourseMap["AL1"] === undefined ? (
                <>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["D1"]}</td>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["C1"]}</td>
                  <td className="px-6 py-4 border-b">{slotToCourseMap["B1"]}</td>
                </>
              ) : (
                <td colSpan="3" className="px-6 py-4 border-b">{slotToCourseMap["AL1"]}</td>
              )}
              <td className="px-6 py-4 border-b">{slotToCourseMap["A1"]}</td>
            </tr>
            {/* Similar structure for Tuesday to Friday */}
          </tbody>
        </table>
      </div>
    </div>
  </>
);
```

- **Header**:
  - A centered title ("Time-Table") with large, bold, dark gray text (`text-3xl`, `font-bold`, `text-gray-800`).
- **Table**:
  - Wrapped in a container with padding (`p-4`), shadow (`shadow-md`), and rounded corners (`rounded-lg`).
  - Uses `overflow-x-auto` for horizontal scrolling on smaller screens.
  - **Header Row**:
    - Gradient background (`bg-gradient-to-r from-blue-500 to-green-500`), white text, with columns for days and time slots.
    - Time slots are dynamically rendered from `timings`.
  - **Body**:
    - Rows for Monday to Friday, each with:
      - A gradient-styled day column (`from-blue-500 to-green-500`).
      - Cells for each time slot, populated with course IDs from `slotToCourseMap`.
      - Conditional rendering for lab slots (e.g., `ML1`, `AL1`):
        - If a lab slot exists, it spans 3 columns (`colSpan="3"`).
        - Otherwise, individual lecture slots (e.g., `B`, `C`, `D`) are displayed.
    - Rows have a hover effect (`hover:bg-gray-100`, `transition-all`).
- **Slot Logic**:
  - Regular slots (A–G) occupy single cells.
  - Lab slots (AL1–AL5, ML1–ML5) span 3 time slots, replacing individual lecture slots.
  - The commented-out dataset uses `ML1–ML5` instead of `AL1–AL5`, indicating support for multiple lab slot formats.

## Styling

- **Tailwind CSS**: Used for a modern, responsive design.
  - **Header**: Centered (`flex justify-center`), padded (`py-6`), large bold text (`text-3xl`, `font-bold`, `text-gray-800`).
  - **Table Container**: Padded (`p-4`), white background (`bg-white`), rounded (`rounded-lg`), shadow (`shadow-md`), with horizontal scrolling (`overflow-x-auto`).
  - **Table**:
    - Full-width (`min-w-full`), centered text (`text-center`).
    - Header: Gradient background (`bg-gradient-to-r from-blue-500 to-green-500`), white text, padded (`px-6 py-4`), bordered (`border-b border-gray-200`).
    - Day Column: Gradient (`from-blue-500 to-green-500`), white text, bold (`font-bold`), padded, bordered.
    - Cells: Padded (`px-6 py-4`), bordered (`border-b`), gray text (`text-gray-700`).
    - Rows: Hover effect (`hover:bg-gray-100`, `transition-all`).
    - Lab Cells: Span 3 columns (`colSpan="3"`) for extended time slots.

## Assumptions

- **Static Data**:
  - `activeCourses` is hardcoded, suggesting a mock dataset for development.
  - Likely intended to be replaced with an API call (e.g., `/api/timetable`).
- **Slot System**:
  - Slots (A–G, AL1–AL5) are predefined and map to specific times and days.
  - Lab slots (AL1–AL5, ML1–ML5) span 3 time slots (e.g., 9:00–11:55 AM).
  - The commented dataset suggests alternative slot names (A1, ML1), indicating flexibility.
- **Timetable Structure**:
  - 5 days (Monday–Friday), 10 hourly slots (8:00 AM–5:55 PM).
  - Each day has a mix of lecture and lab slots, with fixed scheduling.
- **No Conflicts**:
  - Assumes no slot conflicts (e.g., multiple courses in the same slot/day).
- **Integration**:
  - Likely used alongside components like `AssignmentLanding` to provide a complete academic dashboard.
  - Courses (e.g., `CS101`) may link to `courses` data from other modules.

## Notes

- **Unused Context**:
  - `useContext` is imported but unused, suggesting plans for role-based timetable filtering (e.g., student vs. faculty).
- **Static Data**:
  - Hardcoded `activeCourses` limits flexibility; dynamic fetching would improve scalability.
- **Lab Slot Handling**:
  - Conditional rendering for `ML1–ML5` and `AL1–AL5` is repetitive and hardcoded, making maintenance harder.
- **Commented Code**:
  - The alternative `activeCourses` dataset (with `A1`, `ML1`) suggests testing or support for different slot formats.
- **No Navigation**:
  - Lacks links to course details (e.g., clicking `CS101` to view assignments).
- **Accessibility**:
  - Table lacks ARIA attributes for screen readers.
- **Debugging**:
  - No console logs or debugging artifacts, but the commented dataset indicates experimentation.

## Integration with Other Components

- **AssignmentLanding**:
  - Shares course IDs (e.g., `CS101`) with `courses` data, suggesting integration for course navigation.
  - Could link timetable slots to assignment views.
- **RoleContext**:
  - Unused `useContext` hints at future integration to show student-specific or faculty-specific timetables.
- **Courses Data**:
  - Aligns with `courses` dataset (e.g., `CS101`), but lacks assignments field, indicating a separate purpose (scheduling vs. assignment management).

## Future Improvements

- **Dynamic Data**:
  - Fetch courses from an API.
- **Navigation**:
  - Add links to course details.
- **Role-Based Filtering**:
  - Use `RoleContext` to filter courses by user role.
- **Refactor Lab Slots**:
  - Generalize lab slot rendering.
- **Course Details**:
  - Display course names instead of IDs, with tooltips for full details.
- **Testing**:
  - Write unit tests for slot mapping and rendering logic.
- **Error Handling**:
  - Add fallback for missing slots.

