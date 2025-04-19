# CombinedFormsPage Component

## Overview

The `CombinedFormsPage` component is a React-based front-end module designed to provide access to various academic forms for students and faculty at an institution (e.g., IIT Guwahati). It features a tabbed interface to switch between **Undergraduate Forms** and **General Forms**, displaying each form's details in a table with downloadable links for DOC and PDF formats. The component is styled with **Tailwind CSS** for a responsive and modern user interface.

## Dependencies

- **React**: For building the UI and managing state.
- **Tailwind CSS**: For styling the component.

## Component Structure

The `CombinedFormsPage` component is organized into:

1. **Tabbed Navigation**: Buttons to toggle between "Undergraduate Forms" and "General Forms".
2. **Forms Table**: A table displaying form details (Form No, Specialisation, and download links) based on the active tab.
3. **Content Area**: Conditionally renders the table for the selected tab.

## Code Explanation

### Imports

```jsx
import React, { useState } from 'react';
```

- **React** and `useState`: For building the component and managing the active tab state.

### State Management

```jsx
const [activeTab, setActiveTab] = useState('undergraduate');
```

- `activeTab`: Tracks the currently selected tab (`undergraduate` or `general`).
- Initialized to `'undergraduate'` to show undergraduate forms by default.

### Static Data

```jsx
const undergraduateFormsData = [
    {
        formNo: "UG/01",
        specialisation: "Branch Change (For BTech students only)",
        docLink: "https://www.iitg.ac.in/acad/forms/ug/bcform.doc",
        pdfLink: "https://www.iitg.ac.in/acad/forms/ug/bcform.pdf"
    },
    ...
    {
        formNo: "SA/02",
        specialisation: "SA Course Registration Form(This is only for Backlog Students of SA courses)",
        docLink: "https://www.iitg.ac.in/acad/forms/ug/SA_Course_Registration_Form.doc",
        pdfLink: "https://www.iitg.ac.in/acad/forms/ug/SA_Course_Registration_Form.pdf"
    }
];

const generalFormsData = [
    {
        formNo: "Gen/01",
        specialisation: "Application form for foreign students under exchange programmes",
        docLink: "https://www.iitg.ac.in/acad/forms/common/exchange.rtf",
        pdfLink: "https://www.iitg.ac.in/acad/forms/common/exchange.pdf"
    },
    ...
    {
        formNo: "Gen/13(B)",
        specialisation: "Course Registration Form (For Backloggers)",
        docLink: "https://www.iitg.ac.in/acad/forms/common/blankFormBACKLOGGERS.doc",
        pdfLink: "https://www.iitg.ac.in/acad/forms/common/blankFormBACKLOGGERS.pdf"
    }
];
```

- **undergraduateFormsData**: An array of objects representing forms specific to undergraduate students.
- **generalFormsData**: An array of objects for general forms applicable to students, staff, or faculty.
- Each object contains:
  - `formNo`: Unique identifier (e.g., "UG/01", "Gen/13(B)").
  - `specialisation`: Description of the form's purpose.
  - `docLink`: URL to the DOC/RTF version of the form.
  - `pdfLink`: URL to the PDF version of the form.

### Forms Table Renderer

```jsx
const renderFormsTable = (formData) => {
    return (
        <div className="overflow-x-auto shadow-md rounded-lg mt-4">
            <table className="w-full text-left">
                <thead>
                    <tr className="bg-indigo-500 text-white">
                        <th className="py-4 px-6 font-semibold">Form No</th>
                        <th className="py-4 px-6 font-semibold">Specialisation</th>
                        <th className="py-4 px-6 font-semibold text-right">FORMAT</th>
                    </tr>
                </thead>
                <tbody>
                    {formData.map((form, index) => (
                        <tr 
                            key={form.formNo} 
                            className={index % 2 === 0 ? "bg-gray-50" : "bg-white"}
                        >
                            <td className="py-4 px-6 border-t">{form.formNo}</td>
                            <td className="py-4 px-6 border-t">{form.specialisation}</td>
                            <td className="py-4 px-6 border-t text-right">
                                <a href={form.docLink} className="text-blue-600 hover:underline mr-6">DOC</a>
                                <a href={form.pdfLink} className="text-blue-600 hover:underline">PDF</a>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};
```

- **Purpose**: Renders a table for the provided `formData` (either `undergraduateFormsData` or `generalFormsData`).
- **Structure**:
  - A responsive table wrapper (`overflow-x-auto`) with shadow and rounded corners.
  - **Header**:
    - Columns: "Form No", "Specialisation", "FORMAT".
    - Styled with a blue background (`bg-indigo-500`) and white text.
  - **Body**:
    - Maps over `formData` to create rows.
    - Alternates row backgrounds (`bg-gray-50` for even, `bg-white` for odd) for readability.
    - Displays `formNo` and `specialisation`.
    - Provides download links for DOC and PDF formats in the "FORMAT" column, aligned right.
- **Styling**:
  - Uses Tailwind CSS for layout, colors, and spacing.
  - Links are blue with hover underlines (`text-blue-600 hover:underline`).

### Main Rendering

```jsx
return (
    <div className="p-6 max-w-6xl mx-auto">
        <h1 className="text-4xl text-gray-700 font-medium mb-6">University Forms</h1>
        
        <div className="flex mb-4 border-b">
            <button
                className={`py-2 px-4 font-medium ${activeTab === 'undergraduate' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('undergraduate')}
            >
                Undergraduate Forms
            </button>
            <button
                className={`py-2 px-4 font-medium ${activeTab === 'general' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('general')}
            >
                General Forms
            </button>
        </div>
        
        {activeTab === 'undergraduate' && (
            <>
                <h2 className="text-2xl text-gray-700 font-medium mb-4">Undergraduate Forms</h2>
                {renderFormsTable(undergraduateFormsData)}
            </>
        )}
        
        {activeTab === 'general' && (
            <>
                <h2 className="text-2xl text-gray-700 font-medium mb-4">General Forms</h2>
                {renderFormsTable(generalFormsData)}
            </>
        )}
    </div>
);
```

- **Container**:
  - A centered container (`max-w-6xl mx-auto`) with padding (`p-6`).
- **Title**:
  - Displays "University Forms" in large, gray text (`text-4xl text-gray-700`).
- **Tabs**:
  - Two buttons for "Undergraduate Forms" and "General Forms".
  - Active tab is highlighted with blue text and a bottom border (`text-indigo-600 border-b-2`).
  - Inactive tabs are gray with a hover effect (`text-gray-500 hover:text-gray-700`).
- **Content**:
  - Conditionally renders the table for the active tab.
  - Includes a subheading (`h2`) matching the tab name.
  - Calls `renderFormsTable` with the appropriate data (`undergraduateFormsData` or `generalFormsData`).

### Export

```jsx
export default CombinedFormsPage;
```

- Exports the `CombinedFormsPage` component as the default export for use in the application.

## Styling

- **Tailwind CSS**: Used for responsive, modern styling.
  - **Container**: Centered with a max-width (`max-w-6xl`), padded (`p-6`).
  - **Title**: Large, gray, medium-weight text (`text-4xl text-gray-700 font-medium`).
  - **Tabs**: Flex layout, blue highlight for active tab, gray with hover for inactive.
  - **Table**:
    - Full-width, left-aligned text.
    - Blue header (`bg-indigo-500 text-white`).
    - Alternating row colors (`bg-gray-50`/`bg-white`) for readability.
    - Bordered cells (`border-t`) for separation.
    - Download links aligned right with blue text and hover underlines.
  - **Wrapper**: Shadow and rounded corners for the table (`shadow-md rounded-lg`).

## Assumptions

- **Static Data**: The forms data is hardcoded; in a real application, it might be fetched from an API or CMS.
- **External Links**: The `docLink` and `pdfLink` URLs are assumed to be valid and accessible.
- **No Authentication**: The component does not restrict access to forms; authentication might be handled elsewhere.
- **Routing**: Assumes integration with a router (e.g., React Router) to render the component at a specific path (e.g., `/documents/othersform`).

## Notes

- **Hardcoded URLs**: The form links point to `iitg.ac.in`, which may need updating if the domain or paths change.
- **No Error Handling**: The component assumes links are valid; broken links could degrade UX.
- **Accessibility**: Lacks ARIA attributes for the table and tab buttons; keyboard navigation may be limited.
- **Static Tabs**: Only two tabs are supported; adding more categories (e.g., postgraduate forms) would require extending the tab logic.
- **Download Behavior**: Links open in the browser; consider adding `download` attributes for direct downloads:

```jsx
<a href={form.docLink} download className="...">DOC</a>
<a href={form.pdfLink} download className="...">PDF</a>
```

## Future Improvements

- **Dynamic Data**: Fetch forms data from an API to support updates without code changes.
- **Search/Filter**: Add a search bar or filter to find forms by keyword or category.
- **Accessibility**:
  - Add `role="tablist"` and `aria-selected` to tabs.
  - Use `role="table"` and `scope="col"` for table headers.
  - Ensure keyboard navigation for tabs and links.
- **Error Handling**: Display a message or fallback for broken links.
- **Download Tracking**: Log download events for analytics.
- **Responsive Enhancements**: Add mobile-friendly features like collapsible rows or smaller text.
- **Testing**: Write unit tests for tab switching, table rendering, and link accessibility.
- **Additional Tabs**: Support more form categories (e.g., postgraduate, faculty-specific).
- **Form Previews**: Allow previewing PDFs before downloading.
- **Authentication**: Restrict access to certain forms based on user role (e.g., faculty-only forms).