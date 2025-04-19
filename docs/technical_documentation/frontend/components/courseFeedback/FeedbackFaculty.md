# FeedbackFaculty Component

## Overview
FeedbackFaculty is a React functional component that displays a feedback report for a specific course taught by a faculty member. It shows two main views:
- A summary of ratings on different course aspects.
- A list of student comments.
The component uses course data passed through route navigation state and pulls feedback details from a backend API.

## Dependencies
```jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import newRequest from '../../utils/newRequest';
import { FaArrowLeft, FaChartBar, FaCommentDots, FaStar } from "react-icons/fa";
```

1. **React (useState, useEffect)**: for component lifecycle and state handling.
2. **React Router DOM**: useLocation – to access course details passed via navigation.
                         useNavigate – to go back to the previous page.
                         useParams – unused but imported.
3. **newRequest**: an Axios-like instance used for API calls.
4. **React-icons**: for UI icons (FaArrowLeft, FaChartBar, etc.).

## Event Handlers
1. setActiveTab: Switches between the "Summary" and "Comments" tab.

```jsx
onClick={() => setActiveTab('summary')}
onClick={() => setActiveTab('comments')}
```

2. navigate: Navigates back to the course list page.

```jsx
onClick={() => navigate(-1)}
```

## Data Fetching

```jsx
useEffect(() => {
  if (!selectedCourseCode) {
    setError('No course code provided.');
    setLoading(false);
    return;
  }
  const fetchFeedbackData = async () => {
    try {
      const res = await newRequest.get(`/feedback/faculty/${facultyId}/${selectedCourseCode}`);
      const { statistics, feedback } = res.data;
      setFeedbackStats(statistics);
      setFeedbacks(feedback);
      setLoading(false);
    } catch (err) {
      setError('Failed to load feedback data');
      setLoading(false);
    }
  };
  fetchFeedbackData();
}, [selectedCourseCode]);
```
- Uses useEffect to trigger data fetch on mount.
- Retrieves statistics and feedback from API.
- If selectedCourseCode is missing, shows an error early.

## UI Structure

1. Header & Navigation:
```jsx
<button onClick={() => navigate(-1)} className="...">
  <FaArrowLeft /> Back to Courses
</button>
```

2. Course Info:
```jsx
<h1>{selectedCourseName}</h1>
<p>{selectedCourseCode} | {selectedDepartment}</p>
```

3. Tab Buttons
```jsx
<button className={activeTab === 'summary' ? '...' : '...'}>Summary</button>
<button className={activeTab === 'comments' ? '...' : '...'}>Comments</button>
```

Summary Tab: Loops over feedback sections and shows:
Comments Tab: Lists all feedback comments with date and student label.

```jsx
{feedbackStats?.sections?.map((section) => (
  <div key={section.id}>
    <h2>{section.title}</h2>
    {Object.entries(section.questions).map(([questionId, question]) => (
      <div key={questionId}>
        <h3>{feedbackQuestions[questionId]}</h3>
        <div>Avg: {question.average}/5</div>
        ...
      </div>
    ))}
  </div>
))}

{feedbacks.map((feedback, index) => (
  <div key={index}>
    <div>{new Date(feedback.createdAt).toLocaleDateString()}</div>
    <div>Student: {feedback.student || 'Anonymous'}</div>
    <p>"{feedback.comments}"</p>
  </div>
))}
```
## Loading and Error States

1. Loading Spinner:

```jsx
if (loading) return (
  <div>
    <div className="animate-spin ..."></div>
    <p>Loading feedback report...</p>
  </div>
);
```

2. Error Handling:
```jsx
if (error) return (
  <div className="text-red-600">
    {error}
    <button onClick={() => navigate(-1)}>Back</button>
  </div>
);
```
3. Invalid Course Fallback:

```jsx
if (!courseCode) return (
  <div className="text-red-600">
    Invalid course information
    <button onClick={() => navigate(-1)}>Back</button>
  </div>
);
```

## Scope of Improvement

Area	                Suggestions
----------------      ------------------
Code Reuse	          Move repeated navigation buttons into a reusable component.
UI Framework	        Use a UI library like Tailwind UI, Material UI, or Chakra for consistency.
Charting	            Use bar charts or radar graphs (e.g., chart.js) for feedback summary.
Pagination/Filtering	Add filters or pagination for long feedback comment lists.
Error Feedback	      Show specific API errors or validation issues.
Accessibility	        Add ARIA labels for screen readers.

## Usage
This component is intended to be used in a faculty dashboard where an instructor clicks on a course to view its feedback.