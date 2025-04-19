# FeeReceiptPage Component

## Overview

The `FeeReceiptPage` component is a React-based front-end module designed to generate and preview fee receipt PDFs for students at an academic institution (e.g., IIT Guwahati). It allows users to select a semester, view student information, check fee payment status, generate a PDF receipt, and download it. The component integrates with **@react-pdf/renderer** for PDF generation, uses **Tailwind CSS** for styling, and is wrapped in a custom `DocumentLayout` component for consistent page structure.

## Dependencies

- **React**: For building the UI and managing state.
- **@react-pdf/renderer**: For generating PDF documents.
- **DocumentLayout**: A custom component for consistent page layout.
- **PDFPreview**: A custom component for previewing generated PDFs.
- **FeeReceiptPDF**: A custom component that defines the PDF receipt structure.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `FeeReceiptPage` component is organized into the following sections:

1. **Semester Selection**: A dropdown to select a semester (1–8).
2. **Student Information**: Displays static student details (name, roll number, programme, branch).
3. **Fee Payment Status**: Shows whether fees are paid for the selected semester.
4. **PDF Preview**: Displays the generated PDF receipt.
5. **Action Buttons**: Buttons to generate the PDF and download it.

## Code Explanation

### Imports

```jsx
import React, { useState } from "react";
import DocumentLayout from "../../components/documentSection/DocumentLayout";
import PDFPreview from "../../components/documentSection/PDFPreview";
import FeeReceiptPDF from "../../components/documentSection/FeeReceiptPDF";
import { pdf } from "@react-pdf/renderer";
```

- **React** and `useState`: For managing component state.
- **DocumentLayout**: Wraps the page content for consistent styling.
- **PDFPreview**: Renders the generated PDF in the browser.
- **FeeReceiptPDF**: A component that defines the structure of the fee receipt PDF.
- **pdf**: Utility from `@react-pdf/renderer` to generate PDF blobs.

### State Management

```jsx
const [isLoading, setIsLoading] = useState(false);
const [pdfUrl, setPdfUrl] = useState(null);
const [pdfBlob, setPdfBlob] = useState(null);
const [selectedSemester, setSelectedSemester] = useState("");
```

- `isLoading`: Tracks the PDF generation process to prevent multiple requests.
- `pdfUrl`: Stores the URL for the generated PDF (used in `PDFPreview`).
- `pdfBlob`: Stores the PDF blob for downloading.
- `selectedSemester`: Tracks the selected semester from the dropdown.

### Static Data

```jsx
const studentData = {
    name: "JOHN SMITH DOE",
    rollNo: "220103045",
    programme: "BTech",
    branch: "Computer Science and Engineering",
    department: "Computer Science and Engineering",
    feesPaid: {
        1: true,
        2: true,
        3: false,
        4: true,
        5: false,
        6: true,
        7: true,
        8: false,
    },
};

const feeData = [
    { particular: "Tuition Fees", amount: "100000.00" },
    { particular: "Examination Fee", amount: "500.00" },
    ...
    { particular: "Total Amount", amount: "134100.00" },
    { particular: "Adjustment Amount", amount: "0.00" },
    { particular: "Payable Amount", amount: "134100.00" },
    { particular: "Remarks", amount: "null" },
];
```

- **studentData**: Hardcoded student information, including:
  - Basic details (name, roll number, programme, branch, department).
  - `feesPaid`: An object mapping semesters (1–8) to payment status (`true` for paid, `false` for unpaid).
- **feeData**: An array of fee particulars with amounts, including summary rows (total, adjustment, payable amount, remarks).

### Payment Status

```jsx
const isPaid = selectedSemester ? studentData.feesPaid[selectedSemester] : false;
```

- Dynamically determines if fees are paid for the `selectedSemester`.
- Defaults to `false` if no semester is selected.

### PDF Generation Handler

```jsx
const handleGenerate = async () => {
    if (!selectedSemester) return;
    setIsLoading(true);
    try {
        const blob = await pdf(
            <FeeReceiptPDF 
                student={studentData} 
                semester={selectedSemester} 
                feeData={feeData}
                isPaid={isPaid} 
            />
        ).toBlob();
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
        setPdfBlob(blob);
    } finally {
        setIsLoading(false);
    }
};
```

- Triggered when the "Generate Receipt" button is clicked.
- Checks if a semester is selected; if not, exits early.
- Sets `isLoading` to `true` during generation.
- Uses `pdf` to generate a PDF blob from the `FeeReceiptPDF` component, passing:
  - `student`: Student data.
  - `semester`: Selected semester.
  - `feeData`: Fee particulars.
  - `isPaid`: Payment status.
- Creates a URL for the blob and updates `pdfUrl` and `pdfBlob`.
- Resets `isLoading` in the `finally` block.

### PDF Download Handler

```jsx
const handleDownload = () => {
    if (pdfBlob) {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(pdfBlob);
        link.download = `Fee_Receipt_Sem_${selectedSemester}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};
```

- Triggered when the "Download PDF" button is clicked.
- Checks if `pdfBlob` exists.
- Creates a temporary `<a>` element to trigger the download.
- Sets the filename to `Fee_Receipt_Sem_${selectedSemester}.pdf`.
- Cleans up by removing the element.

### Rendering

```jsx
return (
    <DocumentLayout title="Fee Receipt">
        <div className="max-w-3xl mx-auto space-y-6 p-6 bg-gradient-to-b from-blue-50 to-gray-100 rounded-lg shadow-lg">
            <h1 className="text-3xl font-bold text-center text-blue-900 mb-6">Fee Receipt</h1>
            ...
        </div>
    </DocumentLayout>
);
```

- Wraps the content in `DocumentLayout` with the title "Fee Receipt".
- Uses a centered container with Tailwind styling (gradient background, shadow, rounded corners).

#### Semester Selection

```jsx
<select
    value={selectedSemester}
    onChange={(e) => setSelectedSemester(e.target.value)}
    className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
>
    <option value="">Select Semester</option>
    {[1, 2, 3, 4, 5, 6, 7, 8].map(num => (
        <option key={num} value={num}>Semester {num}</option>
    ))}
</select>
```

- A dropdown for selecting semesters (1–8).
- Updates `selectedSemester` on change.
- Styled with Tailwind (border, padding, focus ring).

#### Student Information

```jsx
<div className="bg-white p-4 rounded-lg shadow-inner mt-6">
    <h2 className="text-lg font-semibold text-gray-800 mb-3">Student Information</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <p className="text-sm text-gray-600">Name</p>
            <p className="font-medium">{studentData.name}</p>
        </div>
        ...
    </div>
</div>
```

- Displays student details in a responsive grid (1 column on mobile, 2 on medium screens).
- Styled with Tailwind (white background, shadow, padding).

#### Fee Payment Status

```jsx
{selectedSemester && (
    <div className={`p-3 text-center rounded-lg text-lg font-semibold ${
        isPaid ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
    }`}>
        {isPaid ? "Fees Paid" : "Fees Not Paid"}
    </div>
)}
```

- Conditionally renders when a semester is selected.
- Displays "Fees Paid" (green) or "Fees Not Paid" (red) based on `isPaid`.
- Styled with Tailwind (colored backgrounds, rounded corners).

#### PDF Preview

```jsx
<PDFPreview pdfUrl={pdfUrl} isLoading={isLoading} />
```

- Renders the generated PDF using the `PDFPreview` component.
- Passes `pdfUrl` and `isLoading` as props.

#### Action Buttons

```jsx
<div className="flex justify-center gap-4 pt-4">
    <button
        onClick={handleGenerate}
        disabled={isLoading || !selectedSemester}
        className={`... ${
            isLoading || !selectedSemester
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-gradient-to-r from-blue-600 to-indigo-700 ..."
        }`}
    >
        {isLoading ? "Generating..." : "Generate Receipt"}
    </button>
    {pdfUrl && (
        <button
            onClick={handleDownload}
            className="... bg-gradient-to-r from-green-600 to-teal-700 ..."
        >
            Download PDF
        </button>
    )}
</div>
```

- **Generate Button**:
  - Triggers `handleGenerate`.
  - Disabled if `isLoading` or no semester is selected.
  - Shows "Generating..." during loading.
  - Styled with a blue/indigo gradient and hover effects.
- **Download Button**:
  - Appears only when `pdfUrl` exists.
  - Triggers `handleDownload`.
  - Styled with a green/teal gradient and hover effects.

## Styling

- **Tailwind CSS**: Used for responsive, modern styling.
  - Container: `max-w-3xl`, gradient background (`from-blue-50 to-gray-100`), shadow, rounded corners.
  - Inputs: Border, focus ring, full-width.
  - Cards: White background, shadow, padding.
  - Buttons: Gradients, hover scaling, shadows.
  - Status: Color-coded (green for paid, red for unpaid).
- **Responsive Design**: Uses Tailwind's responsive classes (e.g., `md:grid-cols-2`).

## Assumptions

- **FeeReceiptPDF**: A component that accepts `student`, `semester`, `feeData`, and `isPaid` props to render the PDF content.
- **PDFPreview**: A component that handles PDF rendering in the browser, accepting `pdfUrl` and `isLoading`.
- **DocumentLayout**: A wrapper component that accepts a `title` prop for consistent page structure.
- **Static Data**: `studentData` and `feeData` are hardcoded; in production, these would likely be fetched from an API.

## Notes

- **Hardcoded Data**: The component uses static data for demonstration. Replace with API calls for real-world use.
- **Error Handling**: Limited to `try`/`catch` in `handleGenerate`. Add error messages for failed PDF generation.
- **Performance**: PDF generation is client-side; large datasets may impact performance.
- **Security**: No sensitive data is exposed, but ensure `studentData` is securely fetched in production.

## Future Improvements

- **API Integration**: Fetch `studentData` and `feeData` from a backend API.
- **Error UI**: Display user-friendly error messages for PDF generation failures.
- **Validation**: Add validation for semester selection (e.g., toast notification if not selected).
- **Accessibility**: Add ARIA attributes and keyboard navigation support.
- **Testing**: Write unit tests for PDF generation, download, and semester selection.
- **Dynamic Fee Data**: Allow `feeData` to vary by semester or student.
- **Cleanup**: Revoke `pdfUrl` when the component unmounts to prevent memory leaks:

```jsx
useEffect(() => {
    return () => {
        if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    };
}, [pdfUrl]);
```