# IDCardPDF Component Documentation

## Overview

The `IDCardPDF` component is a React component that generates a PDF document for student ID cards using the `@react-pdf/renderer` library. It creates a professionally formatted student identity card with the student's photo, personal information, and a QR code for verification.

## Props

| Prop      | Type   | Description                                                  |
| --------- | ------ | ------------------------------------------------------------ |
| `student` | Object | Required student data object containing personal information |

The `student` object should include:
- `photo`: URL to student's photograph
- `name`: Student's full name
- `rollNo`: Student's roll number
- `branch`: Academic branch (e.g., CSE)
- `programme`: Degree programme (e.g., BTech)
- `dob`: Date of birth
- `bloodGroup`: Blood group
- `contact`: Emergency contact number

## Code Explanation

### Imports

```jsx
import React from "react";
import { Page, Text, View, Document, StyleSheet, Image } from "@react-pdf/renderer";
import iitglogo from '../../assets/iitglogo.jpg';
```

- `React`: Core React library
- `@react-pdf/renderer` components:
  - `Page`: Represents a single page in the PDF
  - `Text`: For rendering text content
  - `View`: Container component similar to div in HTML
  - `Document`: Root component that wraps all pages
  - `StyleSheet`: For defining styles
  - `Image`: For rendering images
- `iitglogo`: Imported institute logo image

### Styles Definition

```jsx
const styles = StyleSheet.create({
    page: { padding: 20, fontSize: 12, backgroundColor: "#ffffff", borderRadius: 10, border: "1 solid #333" },
    headerContainer: { textAlign: "center", marginBottom: 10, flexDirection: "row", alignItems: "center", justifyContent: "center" },
    headerText: { fontSize: 14, fontWeight: "bold", color: "#1a237e", marginLeft: 10 },
    subHeader: { fontSize: 10, fontWeight: "bold", marginBottom: 8, color: "#333", textAlign: "center" },
    topSection: { flexDirection: "row", alignItems: "center", marginBottom: 10 },
    logo: { width: 70, height: 70 },
    tableContainer: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 10 },
    table: { flex: 1, border: "2 solid #333", borderRadius: 5, overflow: "hidden", marginLeft: 10 },
    row: { flexDirection: "row", borderBottom: "2 solid #333", backgroundColor: "#f8f9fa", padding: 5 },
    cell: { flex: 1, padding: 6, fontSize: 11, borderRight: "2 solid #333" },
    label: { fontWeight: "bold", color: "#1a237e" },
    value: { textAlign: "right", color: "#333" },
    studentImage: { width: 100, height: 120, border: "2 solid #333", borderRadius: 5 },
    qrCode: { width: 60, height: 60, alignSelf: "center", marginTop: 10, border: "2 solid #333" }
});
```

The StyleSheet defines the appearance of all elements in the ID card:

- `page`: Sets the overall page appearance with padding, background color, and border
- `headerContainer`: Styles the header section with centered content and row layout
- `headerText`: Formats the institute name text with bold styling and blue color
- `subHeader`: Styles the "PROVISIONAL IDENTITY CARD" text
- `logo`: Sets dimensions for the institute logo
- `tableContainer`: Creates a flex container for the student photo and information table
- `table`: Styles the table containing student information with borders and rounded corners
- `row`: Formats each row in the table with bottom border and background color
- `cell`: Defines the appearance of individual cells within the table
- `label`: Styles the label text in the left column with bold and blue color
- `value`: Aligns and styles the student information in the right column
- `studentImage`: Sets dimensions and border for the student photo
- `qrCode`: Formats the QR code with borders and proper sizing

### Component Structure

```jsx
const IDCardPDF = ({ student }) => (
    <Document>
        <Page style={styles.page}>
            {/* Header */}
            <View style={styles.headerContainer}>
                <Image src={iitglogo} style={styles.logo} />
                <Text style={styles.headerText}>Indian Institute of Technology Guwahati{"\n"}Guwahati - 781039</Text>
            </View>
            <Text style={styles.subHeader}>PROVISIONAL IDENTITY CARD</Text>
            
            {/* Image and Table Container */}
            <View style={styles.tableContainer}>
                <Image src={student.photo} style={styles.studentImage} />
                <View style={styles.table}>
                    {[
                        { label: "NAME", value: student.name },
                        { label: "ROLL NO", value: student.rollNo },
                        { label: "BRANCH", value: student.branch },
                        { label: "PROGRAMME", value: student.programme },
                        { label: "DATE OF BIRTH", value: student.dob },
                        { label: "BLOOD GROUP", value: student.bloodGroup },
                        { label: "EMERGENCY CONTACT NO", value: student.contact }
                    ].map((item, index) => (
                        <View key={index} style={styles.row}>
                            <Text style={[styles.cell, styles.label]}>{item.label}</Text>
                            <Text style={[styles.cell, styles.value]}>{item.value}</Text>
                        </View>
                    ))}
                </View>
            </View>
            
            {/* QR Code for Verification */}
            <Image 
                src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${student.rollNo}`} 
                style={styles.qrCode} 
            />
        </Page>
    </Document>
);
```

The component creates a PDF document with the following structure:

1. **Header Section**:
   - Displays the institute logo and name
   - Shows "PROVISIONAL IDENTITY CARD" as a subtitle

2. **Main Content Section**:
   - A flex container with two main elements:
     - Student photo on the left
     - Information table on the right

3. **Information Table**:
   - Created dynamically using an array of label-value pairs
   - Each row contains a label and corresponding student information
   - Includes all essential student details (name, roll number, branch, etc.)

4. **QR Code Section**:
   - Generates a QR code containing the student's roll number
   - Uses an external API (api.qrserver.com) to create the QR code
   - The QR code can be used for verification purposes

### Dynamic Data Rendering

The component uses the JavaScript `map()` function to dynamically generate table rows based on the student data:

```jsx
{[
    { label: "NAME", value: student.name },
    { label: "ROLL NO", value: student.rollNo },
    { label: "BRANCH", value: student.branch },
    { label: "PROGRAMME", value: student.programme },
    { label: "DATE OF BIRTH", value: student.dob },
    { label: "BLOOD GROUP", value: student.bloodGroup },
    { label: "EMERGENCY CONTACT NO", value: student.contact }
].map((item, index) => (
    <View key={index} style={styles.row}>
        <Text style={[styles.cell, styles.label]}>{item.label}</Text>
        <Text style={[styles.cell, styles.value]}>{item.value}</Text>
    </View>
))}
```

This approach makes the component more maintainable as it centralizes the data structure and avoids repetitive code.

## Example Usage

```jsx
import React from 'react';
import { pdf } from '@react-pdf/renderer';
import IDCardPDF from './path/to/IDCardPDF';

const GenerateIDCard = () => {
  const studentData = {
    photo: "https://via.placeholder.com/80",
    name: "John Doe",
    rollNo: "220103045",
    branch: "CSE",
    programme: "BTech",
    dob: "15-Aug-2003",
    bloodGroup: "B+",
    contact: "+91 9876543210",
  };

  const handleGenerate = async () => {
    const blob = await pdf(<IDCardPDF student={studentData} />).toBlob();
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
  };

  return (
    <button onClick={handleGenerate}>
      Generate ID Card
    </button>
  );
};
```

## Implementation Notes

1. **External QR Code Generation**:
   - The component uses an external API for QR code generation
   - For a production environment, consider implementing a local QR code generator

2. **Image Handling**:
   - Student photos and the institute logo are rendered using the Image component
   - Ensure proper image dimensions and formats for optimal PDF generation

3. **Styling Approach**:
   - The component uses a detailed StyleSheet object for consistent styling
   - Note that @react-pdf/renderer uses a subset of CSS properties

4. **Layout Considerations**:
   - The component uses flexbox layout extensively for positioning elements
   - The table of information uses a responsive approach to fit various content lengths