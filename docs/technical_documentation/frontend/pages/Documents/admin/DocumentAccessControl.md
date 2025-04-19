# Document Access Control System

## Overview

The Document Access Control System is a React-based administrative module that allows academic administrators to manage student document access permissions and student information. This component enables administrators to view, filter, update, and bulk-manage document access rights for transcripts, ID cards, and fee receipts.

## Component Architecture

### Main Component: `DocumentAccessControl`

The main component serves as the container for the entire interface and manages the application state. It implements both list view and detail view modes.

### Subcomponent: `StudentDetails`

A nested component responsible for displaying and editing comprehensive student information when a student is selected for viewing or editing.

## State Management

The component uses React's useState hook to manage multiple state variables:

| State Variable | Type | Description |
|----------------|------|-------------|
| `filters` | Object | Stores current filter criteria (branch, program, semester, search) |
| `selectedStudent` | Object\|null | Currently selected student for detailed view |
| `selectedStudents` | Set | Collection of student IDs selected for bulk operations |
| `isEditing` | Boolean | Flag to toggle edit mode in student details view |
| `students` | Array | List of student records retrieved from the API |
| `pagination` | Object | Contains current page, total pages, and total count |
| `loading` | Boolean | Indicates whether data is being fetched |

## Code Explanation

### Context Implementation

```javascript
const { role, setRole } = useContext(RoleContext);
setRole("acadAdmin");
```

The component accesses the application's role context and sets the current user role to "acadAdmin", ensuring proper authorization.

### Data Fetching

```javascript
const fetchStudents = async () => {
  try {
    setLoading(true);
    const queryParams = new URLSearchParams({
      page: pagination.currentPage,
      limit: 10,
      ...filters
    });

    const response = await newRequest.get(`/acadadmin/students/document-access?${queryParams}`);
    setStudents(response.data.students);
    setPagination({
      currentPage: parseInt(response.data.currentPage),
      totalPages: parseInt(response.data.totalPages),
      total: parseInt(response.data.total)
    });
  } catch (error) {
    toast.error(error.response?.data?.message || "Error fetching students");
  } finally {
    setLoading(false);
  }
};
```

This function fetches student data based on the current pagination state and applied filters. It:
1. Sets the loading state to true
2. Constructs query parameters
3. Makes an API request
4. Updates the students and pagination state with the response data
5. Handles errors with toast notifications
6. Resets the loading state

### Filter Handling

```javascript
const handleFilterChange = (e) => {
  setFilters({ ...filters, [e.target.name]: e.target.value });
  setPagination(prev => ({ ...prev, currentPage: 1 }));
};
```

When filters are changed, this function:
1. Updates the filters state using the input field's name and value
2. Resets pagination to page 1 to show filtered results from the beginning

### Document Access Control

```javascript
const handleToggleAccess = async (studentId, documentType) => {
  try {
    const student = students.find(s => s.id === studentId);
    const updatedAccess = {
      ...student.access,
      [documentType]: !student.access[documentType]
    };

    await newRequest.patch(`/acadadmin/students/${studentId}/document-access`, {
      access: updatedAccess
    });

    setStudents(students.map(student =>
      student.id === studentId
        ? { ...student, access: updatedAccess }
        : student
    ));

    toast.success("Document access updated successfully");
  } catch (error) {
    toast.error(error.response?.data?.message || "Error updating document access");
  }
};
```

This function toggles document access permissions for individual students:
1. Finds the target student in the state
2. Creates an updated access object with the toggled permission
3. Sends a PATCH request to update the access rights
4. Updates the local state to reflect the change
5. Shows success/error notifications

### Bulk Selection

```javascript
const handleBulkSelect = (e) => {
  if (e.target.checked) {
    setSelectedStudents(new Set(students.map(student => student.id)));
  } else {
    setSelectedStudents(new Set());
  }
};

const handleSingleSelect = (studentId) => {
  setSelectedStudents(prev => {
    const newSet = new Set(prev);
    if (newSet.has(studentId)) {
      newSet.delete(studentId);
    } else {
      newSet.add(studentId);
    }
    return newSet;
  });
};
```

These functions handle selection of students for bulk operations:
- `handleBulkSelect` either selects all students or clears selection
- `handleSingleSelect` toggles individual student selection

### Bulk Actions

```javascript
const handleBulkAction = async (action) => {
  try {
    if (!selectedStudents.size) {
      toast.warning("No students selected");
      return;
    }

    // Parse the action string
    const isEnable = action.startsWith('enable');
    let documentType = action.replace(/^(enable|disable)/, '').toLowerCase();
    
    // Convert to correct property names
    if (documentType === 'idcard') {
      documentType = 'idCard';
    } else if (documentType === 'feereceipt') {
      documentType = 'feeReceipt';
    }

    const accessUpdate = {
      [documentType]: isEnable
    };
    
    await newRequest.post('/acadadmin/students/bulk-document-access', {
      studentIds: Array.from(selectedStudents),
      access: accessUpdate
    });

    await fetchStudents();
    toast.success("Bulk update completed successfully");
  } catch (error) {
    toast.error(error.response?.data?.message || "Error performing bulk update");
  }
};
```

This function applies document access changes to multiple selected students:
1. Validates that students are selected
2. Parses the action to determine document type and enable/disable state
3. Normalizes document type names
4. Creates the access update object
5. Sends a bulk update request
6. Refreshes the student data
7. Shows appropriate notifications

### Student Detail Management

```javascript
const handleSelectStudent = (studentId) => {
  const student = students.find((s) => s.id === studentId);
  setSelectedStudent(student);
  setIsEditing(false);
};
```

This function selects a student for detailed viewing:
1. Finds the student in the current state
2. Updates the selectedStudent state
3. Resets the editing mode

### Student Profile Update

```javascript
const handleSaveStudent = async (updatedData) => {
  try {
    // Update document access
    await newRequest.patch(`/acadadmin/students/${updatedData.id}/document-access`, {
      access: updatedData.access
    });

    // Update student profile
    await newRequest.put(`/student/${updatedData.userId}/profile`, {
      userData: {
        userId: updatedData.userId,
        name: updatedData.name,
        email: updatedData.email,
        contact: updatedData.contact
      },
      hostel: updatedData.hostel,
      roomNo: updatedData.roomNo,
      branch: updatedData.branch,
      program: updatedData.program,
      semester: updatedData.semester
    });

    // Refresh student data
    const queryParams = new URLSearchParams({
      page: pagination.currentPage,
      limit: 10,
      ...filters
    });
    
    const response = await newRequest.get(`/acadadmin/students/document-access?${queryParams}`);
    setStudents(response.data.students);
    
    // Update selected student
    const updatedStudent = response.data.students.find(s => s.id === selectedStudent.id);
    if (updatedStudent) {
      setSelectedStudent(updatedStudent);
    }

    setIsEditing(false);
    toast.success("Student information updated successfully");
  } catch (error) {
    toast.error(error.response?.data?.message || "Error updating student information");
  }
};
```

This comprehensive function handles student data updates:
1. Updates document access permissions
2. Updates student profile information
3. Refreshes the student list
4. Updates the selected student view
5. Exits edit mode
6. Shows appropriate notifications

### StudentDetails Subcomponent

```javascript
const StudentDetails = ({ student, isEditing, onSave }) => {
  const [editData, setEditData] = useState(student);

  const handleChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };

  // Return JSX with student details and edit functionality
};
```

This nested component:
1. Maintains its own state for edit operations
2. Provides input handlers for form fields
3. Renders a detailed view of student information
4. Conditionally renders form inputs or static text based on editing state
5. Provides controls for saving changes

## API Endpoints

The component interacts with the following API endpoints:

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|-------------|----------|
| `/acadadmin/students/document-access` | GET | Fetch students with filtering and pagination | Query parameters | `{ students: [], currentPage: int, totalPages: int, total: int }` |
| `/acadadmin/students/:id/document-access` | PATCH | Update document access for a student | `{ access: { [documentType]: boolean } }` | Success message |
| `/acadadmin/students/bulk-document-access` | POST | Update document access for multiple students | `{ studentIds: [], access: { [documentType]: boolean } }` | Success message |
| `/student/:userId/profile` | PUT | Update student profile information | Student data object | Success message |

## UI Components

### List View Components

1. **Filters Bar**: Input fields and dropdowns to filter students by various criteria
2. **Bulk Action Controls**: Selection indicator and dropdown for bulk operations
3. **Student Table**: Tabular view of students with toggle controls for document access
4. **Pagination Controls**: Buttons to navigate between pages of students

### Detail View Components

1. **Personal Information Section**: Student name, email, contact, etc.
2. **Academic Information Section**: Branch, program, semester, CGPA
3. **Hostel Information Section**: Hostel name and room number
4. **Document Access Section**: Toggle controls for document access permissions
5. **Action Buttons**: Controls to edit, save, or cancel changes

## Error Handling

The component implements comprehensive error handling using try/catch blocks around all asynchronous operations. The `react-hot-toast` library provides user-friendly notifications for:
- Successful operations
- Failed API requests
- Validation errors
- Missing selection errors

## Dependencies

- **React Core**: Uses React hooks for state management
- **Context API**: For role-based access control
- **newRequest**: Custom API client for backend communication
- **react-hot-toast**: For notification system

## Security Considerations

1. **Role-Based Access**: The component sets the user role to "acadAdmin"
2. **Input Validation**: Form fields should have server-side validation
3. **API Security**: Endpoints should verify user permissions
4. **Data Privacy**: Only necessary student information is displayed

## Performance Optimizations

1. **Pagination**: Limits the amount of data loaded at once
2. **Controlled Inputs**: Prevents unnecessary re-renders
3. **Optimistic UI Updates**: Updates UI before server confirmation
4. **Conditional Rendering**: Only renders necessary components

## Future Enhancements

1. **Sortable Tables**: Add column sorting capabilities
2. **Export Functionality**: Add ability to export data to CSV/Excel
3. **Batch Student Creation**: Implement bulk student creation
4. **Audit Logging**: Track changes to document access permissions
5. **Advanced Filtering**: Add date range and additional filters