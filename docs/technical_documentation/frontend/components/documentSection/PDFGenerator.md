# PDFGenerator Component Documentation

## Overview

The PDFGenerator component is a React component that generates PDF documents for different types of student documents including ID cards, transcripts, and fee receipts. It uses the `@react-pdf/renderer` library to render React components as PDFs.

## Props

| Prop        | Type          | Default                 | Description                                                            |
| ----------- | ------------- | ----------------------- | ---------------------------------------------------------------------- |
| `setPdfUrl` | Function      | Required                | Callback function to receive the generated PDF URL                     |
| `type`      | String        | Required                | Type of document to generate ('idCard', 'transcript', or 'feeReceipt') |
| `semester`  | String/Number | Required for feeReceipt | The semester for fee receipt                                           |
| `isPaid`    | Boolean       | `true`                  | Payment status for fee receipt                                         |

## Component Structure

```jsx
const PDFGenerator = ({ setPdfUrl, type, semester, isPaid = true }) => {
  // Component implementation
}
```

## Code Explanation

### Imports and Dependencies

```jsx
import React, { useState } from "react";
import { pdf } from "@react-pdf/renderer";
import IDCardPDF from "../../components/documentSection/IDCardPDF";
import TranscriptPDF from "../../components/documentSection/TranscriptPDF";
import FeeReceiptPDF from "../../components/documentSection/FeeReceiptPDF";
```

- `React, { useState }`: Core React library and the state management hook
- `pdf` from "@react-pdf/renderer": Used to convert React components into PDF blobs
- Custom PDF components that define the structure of different document types:
  - `IDCardPDF`: For student ID cards
  - `TranscriptPDF`: For academic transcripts
  - `FeeReceiptPDF`: For fee receipts

### State Management

```jsx
const [isLoading, setIsLoading] = useState(false);
```

The component uses a single state variable:
- `isLoading`: Boolean flag to track the PDF generation status
- Used to provide visual feedback through the button's appearance and text

### PDF Generation Function

```jsx
const handleGeneratePDF = async () => {
  setIsLoading(true);

  let documentComponent;
  let fileName;

  if (type === "idCard") {
    // ID Card generation logic
  } else if (type === "transcript") {
    // Transcript generation logic
  } else if (type === "feeReceipt") {
    // Fee Receipt generation logic
  }

  const blob = await pdf(documentComponent).toBlob();
  const url = URL.createObjectURL(blob);

  setPdfUrl(url);
  setIsLoading(false);
};
```

This function:
1. Sets the loading state to true to update the UI
2. Determines which document component to render based on the `type` prop
3. Creates sample data for the selected document type
4. Renders the appropriate PDF component with the provided data
5. Converts the React component to a PDF blob using the pdf() function
6. Creates an object URL from the blob using URL.createObjectURL()
7. Passes the URL back to the parent component via the setPdfUrl callback
8. Sets the loading state back to false when complete

### Document Type Handling

#### ID Card

```jsx
if (type === "idCard") {
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
  documentComponent = <IDCardPDF student={studentData} />;
  fileName = "Student_ID_Card.pdf";
}
```

- Creates sample student identification data
- Renders the IDCardPDF component with this data
- Sets the filename for the generated PDF

#### Transcript

```jsx
else if (type === "transcript") {
  const studentData = {
    name: "John Doe",
    rollNo: "220103045",
    programme: "BTech",
    department: "Computer Science and Engineering",
    dateOfAdmission: "2022-07-28",
    currentSemester: "4th",
    cgpa: "8.75",
  };
  documentComponent = <TranscriptPDF student={studentData} />;
  fileName = "Student_Transcript.pdf";
}
```

- Creates sample academic data for the student
- Renders the TranscriptPDF component with this data
- Sets the filename for the generated PDF

#### Fee Receipt

```jsx
else if (type === "feeReceipt") {
  const studentData = {
    name: "John Doe",
    rollNo: "220103045",
    programme: "BTech",
    department: "Computer Science and Engineering",
  };
  const feeData = [
    { particular: "Tuition Fees", amount: "100000.00" },
    // ...more fee items
    { particular: "Total Amount", amount: "134100.00" },
    // ...additional fee information
  ];
  documentComponent = (
    <FeeReceiptPDF
      student={studentData}
      semester={semester}
      feeData={feeData}
      isPaid={isPaid}
    />
  );
  fileName = `Fee_Receipt_Sem_${semester}.pdf`;
}
```

- Creates sample student data and detailed fee breakdown
- Includes total amount and payment status
- Renders the FeeReceiptPDF component with all required data
- Sets a dynamic filename that includes the semester

### UI Rendering

```jsx
return (
  <button
    onClick={handleGeneratePDF}
    disabled={isLoading}
    className={`px-6 py-3 rounded-lg font-semibold text-white transition-all duration-300 shadow-lg transform hover:scale-105 ${
      isLoading
        ? "bg-gray-400 cursor-not-allowed"
        : "bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-indigo-500 hover:to-blue-600"
    }`}
  >
    {isLoading
      ? `Generating ${
          type === "idCard"
            ? "ID Card"
            : type === "transcript"
            ? "Transcript"
            : "Fee Receipt"
        }...`
      : `Generate ${
          type === "idCard"
            ? "ID Card"
            : type === "transcript"
            ? "Transcript"
            : "Fee Receipt"
        }`}
  </button>
);
```

The button UI features:
- Click handler tied to the PDF generation function
- Disabled state when loading to prevent multiple clicks
- Tailwind CSS classes for styling:
  - Base styling: rounded corners, padding, shadow, text color
  - Gradient background that changes on hover
  - Scale transform effect on hover
  - Gray background when disabled
- Dynamic text that changes based on:
  - Loading state (e.g., "Generating..." vs "Generate")
  - Document type (ID Card, Transcript, or Fee Receipt)

## Example Usage

```jsx
import PDFGenerator from "./path/to/PDFGenerator";

function DocumentSection() {
  const [pdfUrl, setPdfUrl] = useState(null);
  
  return (
    <div>
      <PDFGenerator 
        setPdfUrl={setPdfUrl}
        type="idCard"
      />
      
      {pdfUrl && (
        <iframe 
          src={pdfUrl} 
          width="100%" 
          height="500px" 
          title="Generated PDF"
        />
      )}
    </div>
  );
}
```

## Key Implementation Notes

1. **PDF Generation Flow**:
   - React components are rendered with data
   - Components are converted to PDF using @react-pdf/renderer
   - PDFs are made available via object URLs

2. **Mock Data**:
   - The component uses hardcoded sample data
   - In a production environment, this would be replaced with real student data

3. **Error Handling**:
   - The current implementation lacks error handling
   - Consider adding try/catch blocks for production use

4. **Memory Management**:
   - Object URLs should be revoked when no longer needed
   - Parent component should handle URL.revokeObjectURL(pdfUrl) when appropriate