

# Technical Documentation: FeeReceiptPDF Component

## Overview

The `FeeReceiptPDF` component is a React-based module that uses the `@react-pdf/renderer` library to generate a PDF document for a student's fee receipt at an academic institution (e.g., IIT Guwahati). It displays student information, fee particulars, payment status, and institutional branding (logo and header). The component is designed to produce a professional, A4-sized PDF with structured formatting and styling defined using a custom stylesheet.

## Dependencies

- **React**: For building the component.
- **@react-pdf/renderer**: Provides components (`Page`, `Text`, `View`, `Document`, `Image`) for PDF generation.
- **iitglogo**: A static image file (`iitglogo.jpg`) used as the institutional logo.
- **StyleSheet**: A utility from `@react-pdf/renderer` to define CSS-like styles for PDF elements.

## Component Structure

The `FeeReceiptPDF` component generates a single-page PDF with the following sections:

1. **Payment Status**: Indicates whether the fees are paid or unpaid, with a due amount if applicable.
2. **Header**: Displays the IIT Guwahati logo and institutional details.
3. **Subheader**: Labels the document as a "FEE RECEIPT".
4. **Student Information**: Lists student details (name, roll number, semester, academic year, receipt number).
5. **Fees Table**: Presents a table of fee particulars with amounts, including a final payable amount.

## Code Explanation

### Imports

```jsx
import React from "react";
import { Page, Text, View, Document, Image } from "@react-pdf/renderer";
import iitglogo from '../../assets/iitglogo.jpg';
```

- **React**: Required for defining the component.
- **@react-pdf/renderer**: Imports core components:
  - `Document`: The root of the PDF.
  - `Page`: Defines a single page in the PDF.
  - `Text`: Renders text content.
  - `View`: A container for layout (similar to a `<div>`).
  - `Image`: Displays images (e.g., the logo).
- **iitglogo**: Imports the IIT Guwahati logo image from the assets directory.

### Styles

```jsx
const styles = StyleSheet.create({
  page: { padding: 20, fontSize: 12, backgroundColor: "#ffffff" },
  headerContainer: { flexDirection: "row", alignItems: "center", justifyContent: "center", marginBottom: 15 },
  headerText: { fontSize: 14, fontWeight: "bold", color: "#1a237e", marginLeft: 10, textAlign: "center" },
  subHeader: { fontSize: 14, fontWeight: "bold", marginBottom: 10, color: "#333", textAlign: "center" },
  logo: { width: 70, height: 70 },
  studentInfoContainer: { marginBottom: 15, borderBottom: "1px solid #333", paddingBottom: 10 },
  statusContainer: { textAlign: "center", fontSize: 12, fontWeight: "bold", marginBottom: 10, padding: 5, borderRadius: 5, color: "white" },
  paidStatus: { backgroundColor: "#4caf50" },
  unpaidStatus: { backgroundColor: "#f44336" },
  feesTable: { marginTop: 10, borderTop: "1px solid #333" },
  feesTableRow: { flexDirection: "row", borderBottom: "1px solid #333" },
  particularCell: { width: "70%", padding: 6, fontSize: 11, borderRight: "1px solid #333" },
  amountCell: { width: "30%", padding: 6, fontSize: 11, textAlign: "right" },
  totalRow: { flexDirection: "row", backgroundColor: "#e3f2fd", borderBottom: "1px solid #333" }
});
```

- **StyleSheet.create**: Defines styles for PDF elements using a CSS-like syntax tailored for `@react-pdf/renderer`.
- **Key Styles**:
  - `page`: Sets page padding, default font size, and white background.
  - `headerContainer`: Uses flexbox to align logo and text horizontally, centered.
  - `headerText`: Bold, blue text for the institution name and address.
  - `subHeader`: Bold, centered text for the "FEE RECEIPT" title.
  - `logo`: Fixed dimensions for the IIT Guwahati logo.
  - `studentInfoContainer`: Adds margin and a bottom border for student details.
  - `statusContainer`: Centered, bold text for payment status with rounded corners.
  - `paidStatus`/`unpaidStatus`: Green for paid, red for unpaid.
  - `feesTable`: Top border for the fee table.
  - `feesTableRow`: Flexbox row for table rows with bottom border.
  - `particularCell`/`amountCell`: Define table columns (70% and 30% width, respectively) with padding and borders.
  - `totalRow`: Light blue background for summary rows.

### Component Definition

```jsx
const FeeReceiptPDF = ({ student, semester, feeData, isPaid = true }) => {
```

- **Props**:
  - `student`: Object containing student details (e.g., `name`, `rollNo`).
  - `semester`: The semester for which the receipt is generated.
  - `feeData`: Array of fee particulars (e.g., `{ particular: "Tuition Fees", amount: "100000.00" }`).
  - `isPaid`: Boolean indicating payment status (defaults to `true`).

### Data Processing

```jsx
const currentDate = new Date().toLocaleDateString('en-GB');
const receiptNumber = `IITG/FEE/${student?.rollNo || ""}/${semester || ""}/${new Date().getFullYear()}`;
let payableAmount = parseFloat(feeData?.find(item => item.particular === "Payable Amount")?.amount || "0.00");
if (isPaid) {
    payableAmount = 0.00;
}
```

- **currentDate**: Formats the current date in `DD/MM/YYYY` format (e.g., 16/04/2025).
- **receiptNumber**: Generates a unique receipt number using the format `IITG/FEE/rollNo/semester/year` (e.g., `IITG/FEE/220101125/5/2025`).
  - Uses optional chaining (`?.`) to handle missing `student.rollNo` or `semester`.
- **payableAmount**: Extracts the "Payable Amount" from `feeData` or defaults to `0.00`.
  - If `isPaid` is `true`, sets `payableAmount` to `0.00` to reflect no dues.

### PDF Structure

```jsx
return (
    <Document>
        <Page size="A4" style={styles.page}>
            <View style={[styles.statusContainer, isPaid ? styles.paidStatus : styles.unpaidStatus]}>
                <Text>{isPaid ? "Paid - No Due" : `Unpaid - Due Amount: ₹ ${payableAmount.toFixed(2)}`}</Text>
            </View>
            <View style={styles.headerContainer}>
                <Image src={iitglogo} style={styles.logo} />
                <Text style={styles.headerText}>Indian Institute of Technology Guwahati{"\n"}Guwahati - 781039</Text>
            </View>
            <Text style={styles.subHeader}>FEE RECEIPT</Text>
            <View style={styles.studentInfoContainer}>
                <Text>Student Name: {student?.name || ""}</Text>
                <Text>Roll No: {student?.rollNo || ""}</Text>
                <Text>Semester: {semester}</Text>
                <Text>Academic Year: {new Date().getFullYear()}</Text>
                <Text>Receipt No: {receiptNumber}</Text>
            </View>
            <View style={styles.feesTable}>
                {feeData.map((item, index) => (
                    <View key={index} style={styles.feesTableRow}>
                        <Text style={styles.particularCell}>{item.particular}</Text>
                        <Text style={styles.amountCell}>{`₹ ${parseFloat(item.amount.replace(/[^\d.]/g, '')).toFixed(2)}`}</Text>
                    </View>
                ))}
                <View style={styles.feesTableRow}>
                    <Text style={styles.particularCell}>Payable Amount</Text>
                    <Text style={styles.amountCell}>{`₹ ${payableAmount.toFixed(2)}`}</Text>
                </View>
            </View>
        </Page>
    </Document>
);
```

- **Document**: The root component for the PDF.
- **Page**: Defines an A4-sized page with `styles.page` (padding, font size, white background).
- **Status Container**:
  - Displays "Paid - No Due" or "Unpaid - Due Amount: ₹ X.XX" based on `isPaid`.
  - Applies `paidStatus` (green) or `unpaidStatus` (red) styles.
- **Header**:
  - Uses a flexbox `View` to align the logo and institution text.
  - `Image` renders the `iitglogo` with fixed dimensions.
  - `Text` displays "Indian Institute of Technology Guwahati" and the address, with a newline (`\n`).
- **Subheader**:
  - A centered "FEE RECEIPT" title with bold styling.
- **Student Info**:
  - Lists student details (name, roll number, semester, academic year, receipt number).
  - Uses optional chaining for safe access to `student` properties.
  - Separated by a bottom border.
- **Fees Table**:
  - Maps `feeData` to table rows, each with a `particular` and `amount`.
  - Amounts are cleaned (removing non-numeric characters) and formatted to two decimal places.
  - Adds a final row for "Payable Amount" with the computed `payableAmount`.
  - Uses flexbox rows with borders for a tabular layout.

### Amount Formatting

```jsx
parseFloat(item.amount.replace(/[^\d.]/g, '')).toFixed(2)
```

- Strips non-numeric characters (e.g., currency symbols) from `item.amount` using a regex.
- Converts to a float and formats to two decimal places (e.g., `100000.00`).

### Export

```jsx
export default FeeReceiptPDF;
```

- Exports the component for use in other parts of the application.

## Assumptions

- **iitglogo**: The logo file (`iitglogo.jpg`) is available in the specified path and compatible with `@react-pdf/renderer`.
- **feeData**: Contains a "Payable Amount" entry; otherwise, defaults to `0.00`.
- **student**: Provides `name` and `rollNo`; handled gracefully if missing.
- **IDCardPDF**: Not referenced here but assumed to be a separate component (possible documentation error in context).
- **API**: Not used in this component, but parent components may fetch `student` and `feeData`.

## Notes

- **Hardcoded Data**: `validUntil` and some fields are static; consider making them dynamic via props or API.
- **Error Handling**: Limited to optional chaining; missing props could still cause rendering issues.
- **Styling**: Tailored for A4 PDF output, with no responsiveness needed (unlike web UI).
- **Amount Parsing**: The regex-based parsing assumes amounts are numeric or contain removable symbols; validate inputs to avoid errors.
- **Title Inconsistency**: The parent context mentions "Bonafide Certificate" in some cases, but this component is for a fee receipt.

## Future Improvements

- **Dynamic Data**: Fetch `validUntil` and other fields dynamically (e.g., via API or props).
- **Error Handling**: Add validation for `feeData` and `student` props, with fallback UI for missing data.
- **Enhanced Styling**: Add more visual elements (e.g., watermarks, signatures) for authenticity.
- **Accessibility**: Not applicable for PDFs, but ensure parent components are accessible.
- **Testing**: Write unit tests for PDF rendering, amount parsing, and edge cases (e.g., missing props).
- **Amount Validation**: Validate `feeData` amounts to ensure they are numeric and properly formatted.
- **Cleanup**: Ensure parent components revoke blob URLs to prevent memory leaks.

