# FeedbackFacultySelect Component 

## Overview
FeedbackFacultySelect is a React functional component that allows a faculty member to view a list of their courses and navigate to detailed feedback reports for each course. It retrieves the faculty ID from localStorage, fetches courses they teach, and provides navigation to the feedback view page for a selected course.

## Dependencies

```jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './feedback.css';
import newRequest from '../../utils/newRequest';
```

1. **React**: for building the component with hooks like useState and useEffect.
2. **React Router DOM**: useNavigate is used to navigate to the feedback report page.
3. **newRequest**: an Axios-like instance used for API calls.
4. **./feedback.css**: used for custom styles.


## Event Handlers

1. handleCourseSelection(course, instructor): Navigates to the /faculty/feedback/view route, passing necessary course and instructor data via React Router's state.

```jsx
const handleCourseSelection = (course, instructor) => {
  navigate('/faculty/feedback/view', {
    state: {
      facultyId: facultyId,
      courseCode: course.courseCode,
      courseName: course.name,
      instructor: instructor.name,
      semester: course.semester,
      department: instructor.department,
    }
  });
};
```
## Data Fetching
1. Getting Faculty ID: Executed once on mount. Extracts the current user's ID from localStorage.

```jsx
useEffect(() => {
  try {
    const userData = JSON.parse(localStorage.getItem("currentUser"));
    const { user } = userData.data;
    setfacultyId(user.userId);
  } catch (err) {
    setError("Could not retrieve instructor information");
    setLoading(false);
  }
}, []);
```

2. Fetching Courses for the Instructor: Triggered when facultyId becomes available.

```jsx
useEffect(() => {
  if (!facultyId) return;
  const fetchCourses = async () => {
    try {
      const response = await newRequest.get(`/faculty/${facultyId}/courses`);
      setCourses(response.data.courses || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load courses');
      setLoading(false);
    }
  };
  fetchCourses();
}, [facultyId]);
```

## UI Structure
The rendered UI consists of:
- A title prompt.
- A message if no courses are found.
- A grid layout of course cards for each course and instructor pairing.
- A "View Feedback" button to navigate to the report.

```jsx
<h2>Select a course to view feedback:</h2>

<div className="courses-grid">
  {courses.map(course => 
    (course.instructors || []).map(instructor => (
      <div className="course-card" key={`...`}>
        <h3>{course.name}</h3>
        <p>Course Code: {course.code}</p>
        <p>Semester: {course.semester}</p>
        <p>Instructor: {instructor.name}</p>
        <p>Department: {instructor.department}</p>
        <p>Responses: {course.responseCount || 0}</p>
        <button onClick={() => handleCourseSelection(course, instructor)}>View Feedback</button>
      </div>
    ))
  )}
</div>
```

## Loading and Error States
1. Loading:

```jsx
if (loading) return <div className="loading">Loading courses...</div>;
```

2. Error:

```jsx
if (error) return <div className="error-message">{error}</div>;
```
These states ensure the user receives proper visual feedback during API calls and potential failures.

## Scope of Improvement

Area	                Suggestion
Error handling	        Display more specific API errors and validation feedback.
Faculty ID retrieval	Abstract the localStorage logic to a helper utility for safety and reuse.
Performance	            Use React.memo for course card rendering in large datasets.
Pagination / Search	    Add search, sort, or pagination if the course list is large.
Accessibility	        Add semantic roles and ARIA labels for screen readers.
UI polish	            Use animation/transitions or a UI library (e.g., Tailwind UI, Material UI) for a smoother experience.

## Usage
1. Route Setup:
```jsx
<Route path="/faculty/feedback/select" element={<FeedbackFacultySelect />} />
```
2. Auth Requirement:
Ensure the component is only accessible by authenticated users (e.g., inside a PrivateRoute).

3. Navigation to the Component:
Typically invoked after faculty login or from a dashboard.

```jsx
navigate('/faculty/feedback/select');
```