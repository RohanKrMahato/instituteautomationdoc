# FeedbackStudent Component

## Overview
The FeedbackStudent component allows a student to submit feedback for a specific course they are enrolled in. The feedback form includes multiple sections (e.g., Course Content, Faculty Evaluation, Assessment), each with multiple rating questions, as well as a comment box for open-ended suggestions.

Key features:
- Dynamic form rendering based on predefined sections.
- Star rating selection UI.
- Validation to ensure all questions are answered.
- Submits feedback to the backend via a POST request.
- Fetches course and faculty data dynamically using courseId.

## Dependencies
```jsx

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import newRequest from '../../utils/newRequest'; // Axios instance
import {
  FaArrowLeft, FaStar, FaRegStar,
  FaBook, FaChalkboardTeacher, FaCalendarAlt
} from 'react-icons/fa';
import './feedback.css'; // Custom styles
```
1. **React Router-DOM**: for navigation and accessing location state.
2. **React-icons**: for using FontAwesome icons.
3. **newRequest**: a configured Axios instance for backend calls.

## Event Handlers
1. handleRatingChange(questionId, value): Updates the selected rating for a given question.

```jsx
const handleRatingChange = (questionId, value) => {
    setFeedbackData(prev => ({
      ...prev,
      ratings: { ...prev.ratings, [questionId]: value }
    }));
};
```
2. handleCommentsChange: Updates the comments field in the feedback data.

```jsx
const handleCommentsChange = (e) => {
    setFeedbackData(prev => ({
      ...prev,
      comments: e.target.value
    }));
};
```
3. validateForm(): Ensures that all rating questions are answered before submission.

```jsx
const validateForm = () => {
    const allQuestions = feedbackSections.flatMap(section => section.questions.map(q => q.id));
    const unanswered = allQuestions.filter(id => !feedbackData.ratings[id]);
    if (unanswered.length > 0) {
      setValidationError('Please answer all questions before submitting.');
      return false;
    }
    setValidationError('');
    return true;
};
```

4. handleSubmit: Submits the feedback to the backend if the form is valid.

```jsx
await newRequest.post('/feedback/submit', {
  student: studentId,
  faculty: courseDetails.facultyId,
  course: courseId,
  ...
});
```

5. handleCancel(): Navigates back to the course list page.

```jsx
navigate('/courses');
```

## Data Fetching
Course and faculty details are fetched from the backend using courseId.

```jsx
useEffect(() => {
  const fetchDetails = async () => {
    const courseRes = await newRequest.get(`feedback/course/${courseId}/details`);
    setCourseDetails(courseRes.data);
    ...
  };

  if (courseId) fetchDetails();
}, [courseId]);
```
The courseDetails object provides info like:

- facultyName
- facultyId
- department
- session, year
- courseName, courseCode

## UI Structure
The component layout is structured into the following main parts:

- Course & Faculty Info Card: Contains course title, code, department, credits, faculty name and session details.
- Feedback Form Sections: Dynamically renders sections and questions.
- RatingOption: Used to render ratings.
- Comments Box
- Textarea for additional feedback.


## Loading and Error States
1. Loading: When the component is fetching data:

```jsx
if (loading) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="animate-spin ..."></div>
      <span>Loading course information...</span>
    </div>
  );
}
```

2. Error: If fetching fails or data is missing:

```jsx
if (fetchError || !courseDetails) {
  return (
    <div className="...">
      <p>{fetchError || "Missing required information"}</p>
      <button onClick={handleCancel}>Back to Feedback List</button>
    </div>
  );
}
```

## Usage
This component is intended to be used in a faculty or student dashboard, where a student clicks on a course to submit feedback for it.