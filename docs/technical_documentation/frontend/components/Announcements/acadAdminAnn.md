# AcadAdminAnnouncements Component

## Overview

The `AdminAnnouncements` component is a React-based front-end module designed for academic administrators to manage institute-wide announcements. It provides a comprehensive interface for creating, editing, viewing, and deleting announcements with advanced targeting capabilities. The component uses Tailwind CSS for styling and integrates with React Query for data fetching and state management.

## Dependencies

- **React**: Core library for building the UI.
- **React Router DOM**: For navigation (`Link` component).
- **React Icons**: Provides various icons used throughout the interface.
- **React Query (@tanstack/react-query)**: For data fetching, caching, and state management.
- **Tailwind CSS**: For styling the component.
- **Custom Utilities**: Uses a `newRequest` utility for API calls.

## Component Structure

The `AdminAnnouncements` component is a complex form-based component that:

1. Displays a list of existing announcements.
2. Provides a form to create new announcements or edit existing ones.
3. Allows advanced audience targeting with multiple selection options.
4. Handles form validation and submission.
5. Manages loading and error states.

## State Management

The component uses both React's `useState` hooks and React Query for state management:

```jsx
// Component state
const [isAddingAnnouncement, setIsAddingAnnouncement] = useState(false);
const [isEditing, setIsEditing] = useState(false);
const [editingAnnouncementId, setEditingAnnouncementId] = useState(null);
const [formData, setFormData] = useState({...});
const [formErrors, setFormErrors] = useState({});

// React Query hooks
const { isLoading, error, data } = useQuery({...});
const addAnnouncementMutation = useMutation({...});
const editAnnouncementMutation = useMutation({...});
const deleteAnnouncementMutation = useMutation({...});
```

## Form Data Structure

The component manages a complex form state with nested objects:

```jsx
const [formData, setFormData] = useState({
  title: "",
  content: "",  
  importance: "Medium",
  audienceType: "all", // Default audience type
  // Merged audience targeting
  targetGroups: {
    allUniversity: true,
    students: false,
    faculty: false,
    departments: [],
    programs: [],
    semester: "all",
    specificEmails: ""
  }
});
```

## API Integration

The component interacts with several backend endpoints:

- `GET /acadAdmin/announcements`: Fetches all announcements
- `GET /acadAdmin/departments`: Fetches departments for targeting
- `POST /acadAdmin/announcements/add`: Creates a new announcement
- `PUT /acadAdmin/announcements/:id/update`: Updates an existing announcement
- `DELETE /acadAdmin/announcements/:id/delete`: Deletes an announcement

## Component Flow

1. On initial load, fetches existing announcements and departments data.
2. Displays announcements in a list format.
3. When adding/editing an announcement:
   - Shows a form with title, content, importance, and targeting options.
   - Validates user input before submission.
   - Sends data to the backend API.
   - Updates the UI on success or shows errors.

## Key Functions

### Data Fetching

```jsx
// Fetch announcements
const { isLoading, error, data } = useQuery({
  queryKey: ["adminAnnouncements"],
  queryFn: () => 
    newRequest.get("/acadAdmin/announcements").then((res) => {
      return res.data;
    })
});

// Fetch departments
const { isLoading: isDepartmentsLoading, error: departmentsError, data: departmentsData } = useQuery({
  queryKey: ["departments"],
  queryFn: () => 
    newRequest.get("/acadAdmin/departments").then((res) => {
      return res.data;
    }),
  placeholderData: {
    departments: [
      { id: "cse", name: "Computer Science Engineering" },
      // ...other departments
    ]
  }
});
```

### Form Handlers

```jsx
// Handle input change
const handleInputChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({
    ...prev,
    [name]: value
  }));
  // Clear errors
  if (formErrors[name]) {
    setFormErrors(prev => ({
      ...prev,
      [name]: ""
    }));
  }
};

// Handle audience type change
const handleAudienceTypeChange = (type) => {
  // Reset audience targeting when changing type
  const resetTargetGroups = {
    allUniversity: type === 'all',
    students: false,
    faculty: false,
    departments: [],
    programs: [],
    semester: "all",
    specificEmails: ""
  };

  setFormData(prev => ({
    ...prev,
    audienceType: type,
    targetGroups: resetTargetGroups
  }));
};
```

### Form Validation

```jsx
// Validate form
const validateForm = () => {
  const errors = {};
  if (!formData.title.trim()) errors.title = "Title is required";
  if (!formData.content.trim()) errors.content = "Content is required";
  
  // Validate audience selection based on audience type
  if (formData.audienceType === "specific") {
    if (!formData.targetGroups.specificEmails.trim()) {
      errors.specificEmails = "Please enter at least one email address";
    } else if (!validateEmails(formData.targetGroups.specificEmails)) {
      errors.specificEmails = "Please enter valid email addresses separated by commas";
    }
  }
  
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};

// Validate email format
const validateEmails = (emails) => {
  const emailList = emails.split(',').map(email => email.trim());
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailList.every(email => emailRegex.test(email));
};
```

### Form Submission

```jsx
// Handle form submission
const handleSubmit = (e) => {
  e.preventDefault();
  if (!validateForm()) return;
  
  // Prepare announcement data
  let announcementData = {
    title: formData.title,
    content: formData.content,
    importance: formData.importance,
    postedBy: userId,
    targetGroups: formData.targetGroups
  };
  
  // Add backward compatibility fields
  if (formData.audienceType === "all" || formData.targetGroups.allUniversity) {
    announcementData.targetAudience = ["All"];
  } else if (formData.audienceType === "specific") {
    announcementData.targetEmails = formData.targetGroups.specificEmails
      .split(',')
      .map(email => email.trim())
      .filter(email => email);
  }
  
  if (isEditing && editingAnnouncementId) {
    editAnnouncementMutation.mutate({ 
      announcementId: editingAnnouncementId, 
      announcementData 
    });
  } else {
    addAnnouncementMutation.mutate(announcementData);
  }
};
```

### Edit and Delete Operations

```jsx
// Handle edit announcement
const handleEditAnnouncement = (announcement) => {
  setIsEditing(true);
  setEditingAnnouncementId(announcement._id);
  
  // Determine audience type
  let audienceType = "all";
  if (announcement.targetEmails && announcement.targetEmails.length > 0) {
    audienceType = "specific";
  } else if (
    // Complex conditions for determining if targeted...
  ) {
    audienceType = "targeted";
  }
  
  // Convert old format to new format if needed
  const targetGroups = announcement.targetGroups || {
    // Mapping logic
  };
  
  setFormData({
    title: announcement.title,
    content: announcement.content,
    importance: announcement.importance,
    audienceType: audienceType,
    targetGroups: targetGroups
  });
  
  setIsAddingAnnouncement(true);
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Handle delete announcement
const handleDeleteAnnouncement = (announcementId) => {
  if (window.confirm("Are you sure you want to delete this announcement?")) {
    deleteAnnouncementMutation.mutate(announcementId);
  }
};
```

## Helper Functions

```jsx
// Format date function
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};

// Get importance style
const getImportanceClass = (importance) => {
  switch (importance) {
    case 'Critical':
      return 'bg-red-500';
    case 'High':
      return 'bg-orange-500';
    case 'Medium':
      return 'bg-blue-500';
    case 'Low':
      return 'bg-green-500';
    default:
      return 'bg-blue-500';
  }
};

// Format target audience for display
const formatTargetAudience = (announcement) => {
  // Complex logic to format audience information from different data structures
  // Returns a formatted string like "All University" or "Students, Faculty, 2 Departments"
};
```

## Rendering Logic

The component has three main rendering sections:

1. **Header and Admin Info Card**: Shows basic information and stats.
2. **Add/Edit Form**: Conditionally rendered when creating or editing an announcement.
3. **Announcements List**: Shows all existing announcements with action buttons.

The component also handles loading and error states:

```jsx
// Loading state
if (isLoading) {
  return (
    <div className="p-6 flex justify-center items-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading announcements...</p>
      </div>
    </div>
  );
}

// Error state
if (error) {
  return (
    <div className="p-6 flex justify-center items-center min-h-screen">
      <div className="text-center bg-white p-8 rounded-lg shadow-lg border border-red-200 max-w-md">
        <FaExclamationTriangle className="text-5xl text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-3">Error</h2>
        <p className="text-gray-600 mb-6">
          {error.response?.data?.message || "There was an error loading announcements. Please try again later."}
        </p>
        <Link
          to="/profile"
          className="inline-flex items-center justify-center gap-2 bg-purple-500 text-white py-2 px-6 rounded-md font-medium hover:bg-purple-600 transition duration-300"
        >
          <FaArrowLeft className="text-sm" />
          Return to Profile
        </Link>
      </div>
    </div>
  );
}
```

## Styling

- **Tailwind CSS**: Used extensively for a modern, responsive design.
  - **Layout**: Centered layout with maximum width (`max-w-4xl mx-auto`).
  - **Cards**: White backgrounds (`bg-white`), padding (`p-6`), rounded corners (`rounded-lg`), shadows (`shadow-md`).
  - **Forms**: Clearly labeled fields with validation styling.
  - **Buttons**: Color-coded buttons with hover effects.
  - **Lists**: Clean separation with dividers (`divide-y divide-gray-200`).
  - **Status indicators**: Color-coded tags for importance levels.

## Data Structure

### Announcement Object

```javascript
{
  _id: "123456", // MongoDB ObjectId
  title: "Course Registration Open",
  content: "Registration for Fall 2023 courses is now open...",
  importance: "High", // "Critical", "High", "Medium", "Low"
  postedBy: "user123", // User ID of author
  postedByName: "Admin", // Display name of author
  createdAt: "2023-08-15T10:30:00.000Z", // Creation timestamp
  updatedAt: "2023-08-15T10:30:00.000Z", // Last update timestamp
  
  // Audience targeting - multiple formats supported for backward compatibility
  targetGroups: {
    allUniversity: false,
    students: true,
    faculty: false,
    departments: ["cse", "ece"],
    programs: ["BTech"],
    semester: "3",
    specificEmails: ""
  },
  
  // Legacy fields
  targetAudience: ["Students", "CSE Department"],
  targetProgram: ["BTech"],
  targetSemester: "3",
  targetEmails: []
}
```

## Assumptions

- **Authentication**: The user is already authenticated, and their user ID is available in localStorage.
- **API Structure**: Backend API endpoints follow RESTful conventions and return data in the expected format.
- **Role-Based Access Control**: Only users with admin privileges can access this component.
- **Fallback Data**: Uses placeholder data for departments if the API doesn't return expected data.

## Future Improvements

- **Pagination**: Add pagination for handling large numbers of announcements.
- **Scheduled Posting**: Allow scheduling announcements for future publication.
- **Attachments**: Support file attachments with announcements.
- **Performance Optimization**: Memoize expensive computations and render operations.
- **Accessibility**: Improve keyboard navigation and screen reader support.