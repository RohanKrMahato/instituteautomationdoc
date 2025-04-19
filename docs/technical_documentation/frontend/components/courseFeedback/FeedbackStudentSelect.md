# FeedbackStudentSelect Component

## Overview
FeedbackStudentSelect is a React component that enables students to select one of their enrolled courses and navigate to a feedback form. It:
- Retrieves the current student's ID from localStorage
- Fetches their enrolled courses using React Query
- Displays each course in a styled card format
- Navigates to the feedback submission screen on button click

## Dependencies

1. **React Router DOM**: useNavigate – for client-side route transitions
                         useQuery – for managing server state and data fetching
2. **newRequest**: an Axios-like instance used for API calls.
3. **react-icons/fa**: for FontAwesome-style icons used in the UI (FaBookOpen, FaClipboardList, FaBullhorn, etc.)
4. **localStorage.getItem("currentUser")**: used to retrieve the logged-in user’s info.

## Event Handlers
1. handleFeedback: Handles navigation to the feedback form for the selected course using navigate() and passes course details in the state.

```jsx
const handleFeedback = (course) => {
  navigate('/student/feedback/submit', {
    state: {
      courseId: course.id,
      courseName: course.name,
      credits: course.credits,
    }
  });
};
```
## Data Fetching

1. Retrieve Current Student Info
```jsx
const {data:userData} = JSON.parse(localStorage.getItem("currentUser"));
const {userId} = userData.user;
```
- Parses user data from local storage
- Extracts the student’s userId for backend use

2. Fetch Courses with React Query
```jsx
const { isLoading, error, data: studentCourses = [] } = useQuery({
  queryKey: ["courses"],
  queryFn: () =>
    newRequest.get(`/student/${userId}/courses`).then((res) => {
      return res.data.courses || [];
    }),
});
```
- Caches data with key ["courses"]
- Queries GET /student/:userId/courses
- Defaults to an empty array if no data is returned

## UI Structure
Rendered layout includes:
- Header Section
- Title and instructions
- Conditional Views
- Loading Spinner
- Error Display
- No Courses Message
- Course Cards (Grid)
- Course Header: name, icon, ID
- Course Stats: credits, assignments, attendance

- Feedback Button

```jsx

<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
  {studentCourses.map((course) => (
    <div key={course.id} className="course-card">
      {/* Header, Stats, Button */}
    </div>
  ))}
</div>
```
Each card features:
- Pink-accented icons
- Clean, modern layout with Tailwind-style classes
- Responsive design for mobile and desktop views

## Loading and Error States
1. Loading: Displays an animated spinner with Tailwind classes:

```jsx
<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto mb-4"></div>
<p>Loading your courses...</p>
```

2. Error: Displays the error.message or a fallback:

```jsx
<p className="text-red-700 text-lg mb-4">{error.message || "Failed to fetch courses"}</p>
```

3. No Courses: Gracefully handles the case where the student has no enrolled courses:

```jsx
<p className="text-gray-700 text-lg mb-4">You are not enrolled in any courses.</p>
```
## Scope of Improvement

Area	                    Suggestion
------------                ---------------
LocalStorage Parsing	    Use a helper function to extract user ID safely and handle malformed data
Error Granularity	        Distinguish between network errors, unauthorized access, and empty data
Accessibility	            Add semantic roles, ARIA attributes, and alt text for better screen reader support

## Usage
1. Route Setup:
Make sure the following route exists:

```jsx
<Route path="/student/feedback/select" element={<FeedbackStudentSelect />} />
```

2. Auth Requirements:
This component should be protected with an authentication guard (PrivateRoute or similar) since it depends on local user data.

3. Navigation Trigger:
Usually launched after login or from a student dashboard:

```jsx
navigate('/student/feedback/select');
```