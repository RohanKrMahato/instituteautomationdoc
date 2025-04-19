# IDCardPage Component

## Overview

The `IDCardPage` component is a React-based front-end module designed to generate and preview a student ID card in PDF format for an academic institution (e.g., IIT Guwahati). It fetches student data from an API, displays student information, generates a PDF ID card using `@react-pdf/renderer`, and allows users to download the PDF. The component is styled with **Tailwind CSS**, uses **Tanstack Query** for data fetching, and is wrapped in a custom `DocumentLayout` component for consistent page structure.

## Dependencies

- **React**: For building the UI and managing state.
- **@react-pdf/renderer**: For generating PDF documents.
- **Tanstack Query (@tanstack/react-query)**: For fetching student data.
- **newRequest**: A custom utility for making HTTP requests (assumed to be an Axios wrapper).
- **React Icons**: For rendering icons from the `react-icons/fa` library.
- **DocumentLayout**: A custom component for consistent page layout.
- **PDFPreview**: A custom component for previewing generated PDFs.
- **IDCardPDF**: A custom component that defines the PDF ID card structure.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `IDCardPage` component is organized into the following sections:

1. **Student Information**: Displays fetched student details (e.g., name, roll number, programme).
2. **PDF Preview**: Shows the generated ID card PDF.
3. **Action Buttons**: Buttons to generate and download the PDF.

## Code Explanation

### Imports

```jsx
import React, { useState } from "react";
import DocumentLayout from "../../components/documentSection/DocumentLayout";
import PDFPreview from "../../components/documentSection/PDFPreview";
import IDCardPDF from "../../components/documentSection/IDCardPDF";
import { pdf } from "@react-pdf/renderer";
import { FaUser, FaIdBadge, FaGraduationCap, ... } from "react-icons/fa";
import { useQuery } from "@tanstack/react-query";
import newRequest from "../../utils/newRequest";
```

- **React** and `useState`: For managing component state.
- **DocumentLayout**: Wraps the page content for consistent styling.
- **PDFPreview**: Renders the generated PDF in the browser.
- **IDCardPDF**: Defines the structure of the ID card PDF.
- **pdf**: Utility from `@react-pdf/renderer` for PDF generation.
- **React Icons**: Provides icons for visual enhancement (e.g., `FaUser`, `FaFilePdf`).
- **useQuery**: For fetching student data.
- **newRequest**: A utility for API requests (likely Axios-based).

### State Management

```jsx
const [isGenerating, setIsGenerating] = useState(false);
const [pdfUrl, setPdfUrl] = useState(null);
const [pdfBlob, setPdfBlob] = useState(null);
```

- `isGenerating`: Tracks the PDF generation process to prevent multiple requests.
- `pdfUrl`: Stores the URL for the generated PDF (used in `PDFPreview`).
- `pdfBlob`: Stores the PDF blob for downloading (though not used directly in this version).

### User Data

```jsx
const { data: userData } = JSON.parse(localStorage.getItem("currentUser"));
const { userId } = userData.user;
```

- Retrieves user data from `localStorage` and extracts `userId` for API requests.
- Assumes `currentUser` is stored as a JSON string with a `user` object containing `userId`.

### Data Fetching with Tanstack Query

```jsx
const { isLoading, error, data: studentData } = useQuery({
    queryKey: [`idcard-${userId}`],
    queryFn: () => newRequest.get(`/student/${userId}`).then((res) => res.data),
});
```

- Uses `useQuery` to fetch student data for the given `userId`.
- `queryKey`: Unique key (`idcard-${userId}`) for caching.
- `queryFn`: Makes a GET request to `/student/${userId}` and returns the response data.
- Returns `isLoading`, `error`, and `studentData` (renamed from `data`).

### Loading and Error States

```jsx
if (isLoading) {
    return (
        <DocumentLayout title="Bonafide Certificate">
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading student information...</p>
                </div>
            </div>
        </DocumentLayout>
    );
}
if (error) {
    return (
        <DocumentLayout title="Bonafide Certificate">
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <FaExclamationCircle className="h-5 w-5 text-red-500" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-red-700">
                            Error loading student information. Please try again later.
                        </p>
                    </div>
                </div>
            </div>
        </DocumentLayout>
    );
}
```

- **Loading**: Displays a spinner and message while `studentData` is being fetched.
- **Error**: Shows an error alert with an icon if the data fetch fails.
- Both use `DocumentLayout` with the title "Bonafide Certificate" (likely a typo; should be "Student ID Card").

### Student Data Processing

```jsx
const fullStudent = {
    photo: studentData?.userId?.profilePicture || "https://via.placeholder.com/80",
    name: studentData?.userId?.name || "N/A",
    rollNo: studentData?.rollNo || "N/A",
    programme: studentData?.program || "N/A",
    branch: studentData?.department || "N/A",
    validUntil: "2024-05-31", // optionally fetch this if it's dynamic
    bloodGroup: studentData?.userId?.bloodGroup || "N/A",
    contact: studentData?.userId?.contactNo || "N/A"
};

const studentInfo = [
    { label: "Name", value: fullStudent.name, icon: <FaUser /> },
    { label: "Roll No", value: fullStudent.rollNo, icon: <FaIdCard /> },
    ...
];
```

- **fullStudent**: Normalizes fetched `studentData` with fallback values:
  - Uses optional chaining to handle nested properties (e.g., `userId.profilePicture`).
  - Defaults to placeholders (e.g., a placeholder image URL, "N/A").
  - Hardcodes `validUntil` (should ideally be dynamic).
- **studentInfo**: An array of display items for student details, each with a label, value, and icon.

### PDF Generation Handler

```jsx
const handleGenerate = async () => {
    setIsGenerating(true);
    setPdfUrl(null); // Clear previous PDF
    setPdfBlob(null);
    try {
        const blob = await pdf(<IDCardPDF student={fullStudent} />).toBlob();
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
    } catch (error) {
        console.error("Error generating PDF:", error);
    } finally {
        setIsGenerating(false);
    }
};
```

- Triggered when the "Generate ID Card" button is clicked.
- Clears previous PDF state (`pdfUrl`, `pdfBlob`).
- Sets `isGenerating` to `true` during generation.
- Uses `pdf` to generate a PDF blob from the `IDCardPDF` component, passing `fullStudent` as a prop.
- Creates a URL for the blob and updates `pdfUrl`.
- Logs errors to the console (no user-facing error message).
- Resets `isGenerating` in the `finally` block.

### Rendering

```jsx
return (
    <DocumentLayout title="Student ID Card">
        <div className="max-w-4xl mx-auto p-6 md:p-8 space-y-8 rounded-2xl shadow-xl border border-gray-200">
            ...
        </div>
    </DocumentLayout>
);
```

- Wraps the content in `DocumentLayout` with the title "Student ID Card".
- Uses a centered container with Tailwind styling (max-width, padding, shadow, border).

#### Student Information

```jsx
<div className="bg-white shadow-lg rounded-xl border border-gray-100 p-6 md:p-8">
    <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center gap-3">
        <FaInfoCircle className="text-indigo-500" />
        Your Information
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
        {studentInfo.map((item, index) => (
            <div key={index} className="flex items-center gap-4 p-3 ...">
                <span className="text-indigo-600 text-xl bg-indigo-100 p-2 rounded-full">
                    {item.icon}
                </span>
                <div>
                    <p className="text-xs text-gray-500 ...">{item.label}</p>
                    <p className="text-gray-900 font-semibold ...">{item.value}</p>
                </div>
            </div>
        ))}
    </div>
</div>
```

- Displays student details in a responsive grid (1 column on mobile, 2 on medium screens).
- Each item includes an icon, label, and value.
- Styled with Tailwind (white background, shadow, rounded corners, hover effects on mobile).

#### PDF Preview

```jsx
<div className="bg-gray-50 p-4 rounded-lg shadow-inner border border-gray-200 min-h-[200px] flex items-center justify-center">
    <PDFPreview pdfUrl={pdfUrl} isLoading={isLoading} />
</div>
```

- Renders the generated PDF using the `PDFPreview` component.
- Passes `pdfUrl` and `isLoading` as props.
- Styled with Tailwind (gray background, shadow, border, minimum height).

#### Action Buttons

```jsx
<div className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-6">
    <button
        onClick={handleGenerate}
        disabled={isLoading}
        className={`... ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-gradient-to-r from-blue-600 to-indigo-700 ..."}`}
    >
        {isLoading ? (
            <>
                <svg className="animate-spin ...">...</svg>
                Generating...
            </>
        ) : (
            <>
                <FaFilePdf />
                Generate ID Card
            </>
        )}
    </button>
    {pdfUrl && !isLoading && (
        <a
            href={pdfUrl}
            download="Student_ID_Card.pdf"
            className="... bg-gradient-to-r from-green-500 to-teal-600 ..."
        >
            <FaDownload />
            Download PDF
        </a>
    )}
</div>
```

- **Generate Button**:
  - Triggers `handleGenerate`.
  - Disabled if `isLoading`.
  - Shows a spinner and "Generating..." during loading.
  - Styled with a blue/indigo gradient, hover effects, and focus ring.
- **Download Button**:
  - Appears only when `pdfUrl` exists and not loading.
  - Uses an `<a>` tag with the `download` attribute for direct downloading.
  - Styled with a green/teal gradient, hover effects, and focus ring.

## Styling

- **Tailwind CSS**: Used for responsive, modern styling.
  - Container: `max-w-4xl`, rounded corners, shadow, border.
  - Cards: White background, shadow, padding, rounded corners.
  - Buttons: Gradients, hover scaling, shadows, focus rings.
  - Grid: Responsive layout (`md:grid-cols-2`).
  - Icons: Rounded backgrounds, consistent sizing.
- **Responsive Design**: Adapts to mobile and desktop screens (e.g., flex column on small screens, row on larger screens).
- **Visual Feedback**: Hover effects on student info items (mobile only), animated spinner for loading.

## Assumptions

- **IDCardPDF**: A component that accepts a `student` prop to render the ID card PDF.
- **PDFPreview**: Handles PDF rendering in the browser, accepting `pdfUrl` and `isLoading`.
- **DocumentLayout**: A wrapper component that accepts a `title` prop.
- **newRequest**: A pre-configured Axios instance for API requests.
- **API Endpoint**: `GET /student/${userId}` returns student data with nested `userId` properties (e.g., `userId.name`).
- **localStorage**: Stores `currentUser` with a `user.userId` field.

## Notes

- **Title Mismatch**: The `DocumentLayout` title is set to "Bonafide Certificate" (likely a typo; should be "Student ID Card").
- **Error Handling**: Logs PDF generation errors to the console but lacks user-facing error messages.
- **Static Data**: `validUntil` is hardcoded; consider fetching it dynamically.
- **Unused State**: `pdfBlob` is set but not used (download uses `pdfUrl` directly).
- **Security**: Assumes `userId` is validated server-side; ensure `localStorage` data is secure.

## Future Improvements

- **Error UI**: Display user-friendly error messages for PDF generation failures (e.g., toast notifications).
- **Dynamic ValidUntil**: Fetch the `validUntil` date from the API or calculate it dynamically.
- **Cleanup**: Revoke `pdfUrl` on component unmount to prevent memory leaks:

```jsx
useEffect(() => {
    return () => {
        if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    };
}, [pdfUrl]);
```

- **Validation**: Add checks for incomplete student data before generating the PDF.
- **Accessibility**: Add ARIA attributes and keyboard navigation support.
- **Testing**: Write unit tests for data fetching, PDF generation, and download functionality.
- **Performance**: Optimize PDF generation for large datasets or complex `IDCardPDF` layouts.
- **Download Handler**: Simplify by removing `pdfBlob` and using `pdfUrl` consistently.