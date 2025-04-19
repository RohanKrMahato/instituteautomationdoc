# Fee Structure Management System

## Overview

This document provides technical details about the Fee Structure Management React component, which allows academic administrators to add and view fee structures for different programs and semesters.

## Key Features

1. **Dual-View Interface**:
   - Add new fee structures with comprehensive form validation
   - View existing fee structures in a detailed table
   - Tab-based navigation between views

2. **Complete Fee Breakdown**:
   - Supports 14 different fee categories
   - Handles both semester types (Odd/Even)
   - Works with multiple academic programs

3. **Data Management**:
   - Form validation for all required fields
   - API integration for CRUD operations
   - Optimized data fetching with React Query

## Technical Stack

- **Frontend**: React.js with functional components
- **State Management**: React Query for data fetching and mutations
- **UI Library**: DaisyUI (Tailwind CSS component library)
- **Icons**: React Icons (Font Awesome set)
- **API Client**: Custom `newRequest` wrapper (likely around Axios)
- **Form Handling**: React state management with validation

## Code Structure Explanation

### 1. State Management

```javascript
const initialFormData = {
  semesterParity: "", // 0 for Even, 1 for Odd
  year: "",
  program: "",
  // ... other fee fields
};

const [formData, setFormData] = useState(initialFormData);
const [formErrors, setFormErrors] = useState({});
const [activeTab, setActiveTab] = useState("add"); // "add" or "view"
```

- `initialFormData`: Default values for all form fields
- `formData`: Current state of the form
- `formErrors`: Validation error messages
- `activeTab`: Controls which view is displayed

### 2. API Integration with React Query

```javascript
// Mutation for creating new fee structure
const createFeeStructure = useMutation({
  mutationFn: (data) => newRequest.post("/acadadmin/feeControl/addFee", data),
  onSuccess: () => {
    toast.success("Fee structure added successfully");
    setFormData(initialFormData);
    queryClient.invalidateQueries(["fee-structure-list"]);
  },
  // ... error handling
});

// Query for fetching fee structures
const { isLoading, error, data: feeList = [] } = useQuery({
  queryKey: ["fee-structure-list"],
  queryFn: () => newRequest.get("/acadadmin/feeControl/getFeeBreakdown").then((res) => res.data.data),
  enabled: activeTab === "view", // Only fetch when viewing list
});
```

- Uses React Query for efficient data management
- Automatic cache invalidation after successful submission
- Conditional fetching based on active tab

### 3. Form Validation

```javascript
const validateForm = () => {
  const errors = {};
  if (!formData.year) errors.year = "Year is required";
  // ... validation for all other required fields
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};
```

- Comprehensive validation for all fee categories
- Sets error messages in state
- Returns boolean indicating form validity

### 4. Form Submission

```javascript
const handleSubmit = (e) => {
  e.preventDefault();
  if (validateForm()) {
    const submissionData = {
      ...formData,
      semesterParity: formData.semesterParity ? formData.semesterParity : undefined,
    };
    createFeeStructure.mutate(submissionData);
  }
};
```

- Prevents default form submission
- Only submits if validation passes
- Cleans up data before submission
- Triggers mutation

### 5. UI Components

#### Form View (`renderFormView`)

- Organized in clear sections:
  1. **Basic Information**: Year, Program, Semester Type
  2. **Fee Details**: All 14 fee categories
- Each field:
  - Shows appropriate icon
  - Displays validation errors
  - Has consistent styling
- Responsive grid layout

#### List View (`renderListView`)

- Handles loading, error, and empty states
- Displays fee structures in a scrollable table
- Shows all fee categories with proper formatting
- Hover effects for better UX
- Compact view with abbreviated headers

### 6. Tab Navigation

```javascript
<div className="inline-flex rounded-lg p-1 shadow-inner space-x-1 border border-indigo-200">
  <button onClick={() => setActiveTab("add")} className={`...`}>
    <FaPlus /> Add Fee Structure
  </button>
  <button onClick={() => setActiveTab("view")} className={`...`}>
    <FaListAlt /> Fee Structures List
  </button>
</div>
```

- Visual indicator for active tab
- Gradient styling for selected tab
- Smooth transitions between views

## Technical Considerations

1. **Performance**:
   - Conditional data fetching reduces unnecessary API calls
   - Memoization could be added for complex components
   - Virtual scrolling could help with large fee structure lists

2. **Security**:
   - Assumes authentication is handled at higher level
   - No sensitive data handling in the component itself

3. **Accessibility**:
   - Semantic HTML structure
   - Clear form labels
   - Sufficient color contrast
   - Keyboard navigable

4. **Error Handling**:
   - Form validation with clear error messages
   - API error handling with toast notifications
   - Loading states for better UX

## Integration Points

1. **API Endpoints**:
   - POST `/acadadmin/feeControl/addFee` - Add new fee structure
   - GET `/acadadmin/feeControl/getFeeBreakdown` - Get fee structure list

2. **Components**:
   - `DocumentLayout`: Wrapper for consistent page structure
   - Uses shared `newRequest` API client

3. **Dependencies**:
   - React Query for data management
   - react-icons for UI icons
   - react-hot-toast for notifications
   - DaisyUI/Tailwind CSS for styling

## Future Enhancements

1. **Editing Capability**:
   - Add edit functionality for existing fee structures
   - Pre-fill form with existing data

2. **Filtering/Searching**:
   - Add filters for year, program, semester type
   - Search functionality for easier navigation

3. **Export Options**:
   - Export fee structures as CSV/PDF
   - Printable views

4. **Batch Operations**:
   - Import fee structures from CSV
   - Copy existing fee structures for new years

5. **Enhanced UI**:
   - Charts for fee breakdown visualization
   - Comparison views between different fee structures
   - More detailed empty states