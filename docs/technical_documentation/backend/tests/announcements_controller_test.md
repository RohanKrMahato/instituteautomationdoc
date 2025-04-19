# Course Announcements Controller Test 

***This document provides technical documentation for the test suite implemented for the course announcements controller.***

## Overview
This test suite is designed to validate the functionality of course announcements endpoints in the Express app. It tests routes for retrieving, adding, updating, and deleting announcements. The suite uses mocked models to simulate database behavior and ensure controller logic functions correctly.


## Dependencies

- express: For creating the Express application
- supertest: For making HTTP assertions
- body-parser: To parse incoming request bodies
- jest: For mocking and writing test cases
- Models: course.model.js, faculty.model.js, student.model.js, user.model.js (mocked)

## Function: GET /api/courses/:courseId/announcements

***Input***
- Path parameter: courseId

 ***Process***
- Fetches the course using the given courseId.
- Converts each announcement into a plain object.
- Retrieves all faculty data.
- Matches postedBy ID from announcements with faculty list.
- Adds faculty details to each announcement.

***Output***
- 200: List of announcements with faculty details
- 404: Course not found
- 500: Internal server error


## Function: POST /api/courses/:courseId/announcements

***Input***
- Path parameter: courseId
- Request body: title, content, postedBy, importance (optional)

***Process***
- Validates required fields (title, content, postedBy).
- Fetches the course by courseId.
- Creates a new announcement object.
- Adds the announcement to the course's announcements array.
- Saves the updated course document.

**Output***
- 201: Announcement created successfully
- 400: Missing required fields
- 404: Course not found
- 500: Internal server error


## Function: PUT /api/courses/:courseId/announcements/:announcementId

***Input***
- Path parameters: courseId, announcementId
- Request body: title, content, importance (optional), attachments (optional)

***Process***
- Validates that required fields are not empty.
- Retrieves the course using courseId.
- Searches for the announcement by announcementId.
- Updates the announcement's fields.
- Saves the updated course document.

***Output***
- 200: Announcement updated successfully
- 400: Missing or invalid fields
- 404: Announcement or course not found


## Function: DELETE /api/courses/:courseId/announcements/:announcementId

***Input***
- Path parameters: courseId, announcementId

***Process***
- Fetches the course using courseId.
- Removes the announcement with the given announcementId from the announcements array.
- Saves the updated course document.

***Output***
- 200: Announcement deleted successfully
- 404: Course or announcement not found
- 500: Internal server error



