# TranscriptPDF Component Technical Documentation

## Overview

The `TranscriptPDF` component is a React component that generates a PDF document containing a student's academic transcript for the Indian Institute of Technology Guwahati. The component uses `@react-pdf/renderer` to create a structured PDF with student information, course details, and academic performance metrics.

## Dependencies

- React
- @react-pdf/renderer (for PDF generation)
- IIT Guwahati logo image asset (`iitglogo.jpg`)

## Component Structure

### Styles

The component defines a comprehensive set of styles using `StyleSheet.create()` from the `@react-pdf/renderer` library. These styles control the appearance of the PDF document, including:

- Page layout and background
- Header formatting
- Student information section
- Course table formatting
- SPI/CPI (academic performance metrics) table formatting

### Main Component

`TranscriptPDF` is a functional React component that accepts a `student` object as a prop. The component renders a PDF document with the following sections:

1. **Header**: Contains the IIT Guwahati logo and title
2. **Student Information**: Displays personal details alongside student photo and QR code
3. **Course List**: Table of all courses taken by the student
4. **SPI & CPI**: Table of semester-wise academic performance metrics

## Props

### `student` (Object)

Required student data with the following structure:

```javascript
{
  name: String,          // Student's full name
  rollNo: String,        // Student's roll number
  branch: String,        // Academic branch/department
  programme: String,     // Academic program (e.g., B.Tech, M.Tech)
  photo: String,         // URL or data URI of student's photo
  courses: [             // Array of course objects
    {
      code: String,      // Course code
      name: String,      // Course name
      credit: String,    // Credit value or "Audit"
      year: String,      // Academic year
      session: String,   // Academic session
      grade: String      // Achieved grade
    }
  ],
  spiCpi: [              // Array of semester performance objects
    {
      semester: String,  // Semester number
      spi: String,       // Semester Performance Index
      cpi: String        // Cumulative Performance Index
    }
  ]
}
```

## Component Features

### Error Handling

If no student data is provided, the component renders a PDF with an error message.

### Student Information Section

The component displays key student information in a structured format, including:
- Name
- Roll Number
- Branch
- Programme

### Student Photo and QR Code

The component includes:
- The student's photo (if available)
- A QR code generated from the student's roll number (using an external QR code generation API)

### Course List Table

A comprehensive table listing all courses taken by the student, including:
- Course Code
- Course Name
- Credit/Audit status
- Year
- Session
- Grade

### SPI & CPI Table

A table showing the student's academic performance metrics by semester:
- Semester number
- SPI (Semester Performance Index)
- CPI (Cumulative Performance Index)

## Implementation Details

### Document Structure

The component uses the `Document` and `Page` components from `@react-pdf/renderer` to create the PDF structure.

### Styling Approach

- Uses flexbox-based layouts for responsive positioning
- Implements consistent color scheme using institute colors
- Applies borders and formatting consistent with official document standards

### Conditional Rendering

The component handles missing data gracefully:
- Displays "N/A" for missing field values
- Shows appropriate messages when arrays are empty
- Provides fallback content when images are unavailable

## Usage Example

```jsx
import React from 'react';
import { PDFViewer } from '@react-pdf/renderer';
import TranscriptPDF from './TranscriptPDF';

const studentData = {
  name: "John Doe",
  rollNo: "12345678",
  branch: "Computer Science and Engineering",
  programme: "B.Tech",
  photo: "https://example.com/student-photo.jpg",
  courses: [
    {
      code: "CS101",
      name: "Introduction to Programming",
      credit: "4",
      year: "2022",
      session: "Autumn",
      grade: "A"
    },
    // More courses...
  ],
  spiCpi: [
    {
      semester: "1",
      spi: "9.2",
      cpi: "9.2"
    },
    // More semester data...
  ]
};

const TranscriptViewer = () => (
  <PDFViewer width="100%" height="800px">
    <TranscriptPDF student={studentData} />
  </PDFViewer>
);

export default TranscriptViewer;
```

## Notes

- The QR code is generated using an external API (`https://api.qrserver.com`)
- The component is designed for academic transcript formatting specific to IIT Guwahati
- PDF styling uses the institute's color scheme with primary color `#1a237e`