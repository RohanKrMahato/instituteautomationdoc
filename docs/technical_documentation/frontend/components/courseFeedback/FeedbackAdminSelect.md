# FeedbackAdminSelect Component

## Overview
The FeedbackAdminSelect component provides academic administrators with a searchable list of courses to view feedback reports. It fetches a list of available courses from the server and allows filtering by course title or code. Upon selection, the user is navigated to a feedback view page with course-specific data.

## Dependencies
1. **React**: Component logic and lifecycle
2. **React Router DOM** : Navigation between routes (useNavigate)
3. **feedback.css**: Controls layout and visuals of the UI elements

## Event Handlers

1. handleSearchChange: Updates the search term state as the user types in the input.

```jsx
const handleSearchChange = (e) => setSearchTerm(e.target.value);
```

2. handleCourseSelect(course): Navigates to the feedback viewing page, passing selected course data using React Router's state.

```jsx
const handleCourseSelect = (course) => {
  navigate('/acadAdmin/feedback/view', {
    state: {
      courseName: course.title,
      courseCode: course.courseCode,
      facultyId: course.facultyId,
      semester: course.semester,
      department: course.department,
    }
  });
};
```

## Data Fetching
fetchAvailableCourses: Fetches available course data on initial render using the fetch API.

```jsx

useEffect(() => {
  fetchAvailableCourses();
}, []);

const fetchAvailableCourses = async () => {
  try {
    const response = await fetch('/acadAdmin/courses');
    if (!response.ok) throw new Error('Failed to fetch courses');
    const data = await response.json();
    setCourses(data.courses || []);
    setLoading(false);
  } catch (err) {
    setError('Failed to load available courses');
    setLoading(false);
  }
};
```
- If the API call fails, a user-friendly error message is shown
- Course list is stored in the courses state

## UI Structure

1. Search Input: Allows dynamic filtering of the course list.
```jsx
<input
  type="text"
  placeholder="Search courses by name or code..."
  ...
/>
```

2. Course Grid: Courses are filtered and rendered as interactive cards.

```jsx
<div className="courses-grid">
  {filteredCourses.map(course => (
    <div key={course.id} className="course-card" onClick={() => handleCourseSelect(course)}>
      <h3>{course.title}</h3>
      <p className="course-code">{course.code}</p>
      <p className="course-instructor">Instructor: {course.instructor}</p>
      <div className="course-stats">
        <span>{course.enrolledStudents} students</span>
        <span>{course.feedbackCount || 0} feedback submissions</span>
      </div>
      <button className="view-feedback-btn">View Feedback</button>
    </div>
  ))}
</div>
```

## Loading and Error States
1. Loading State: Displayed while the course list is being fetched.

```jsx
if (loading) return <div className="loading">Loading available courses...</div>;
```

2. Error State: Shown when API call fails.

```jsx
{error && <div className="error-message">{error}</div>}
```

3. No Courses Found: If the course list is empty or no matches are found.

```jsx
<div className="no-courses">
  {searchTerm ? 'No courses match your search criteria.' : 'No courses available.'}
</div>
```

## Scope of Improvement

Area	                Suggestion
-----------             ---------------
Loading Skeletons	    Add animated skeleton cards instead of plain "Loading..." text
Pagination	            Support for large course lists by paginating the results
Accessibility	        Improve keyboard navigation and add ARIA labels

## Usage

1. Route Setup
Ensure the component is properly routed in the admin panel:
```jsx
<Route path="/acadAdmin/feedback/select" element={<FeedbackAdminSelect />} />
```

2. Navigation to View Page

When a course is selected, the component navigates to:
```bash
/acadAdmin/feedback/view
```
and passes this data in state:

```jsx
{
  courseName,
  courseCode,
  facultyId,
  semester,
  department
}
```
The target route (/acadAdmin/feedback/view) should extract this data using useLocation().