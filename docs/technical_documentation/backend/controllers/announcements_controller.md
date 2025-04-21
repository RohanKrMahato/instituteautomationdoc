# Announcements Controller

## Overview

The `announcements.controller` manages course-specific announcements within the academic system. Faculty can post, update, or delete announcements for a course, and students can retrieve all relevant announcements. Each announcement can optionally include attachments and is enriched with faculty metadata.

## Dependencies

```javascript

import { Course } from '../models/course.model.js';
import { Faculty } from '../models/faculty.model.js';
import { Student } from '../models/student.model.js';
import { StudentCourse } from '../models/course.model.js';
import { User } from '../models/user.model.js';`
```
## Controller Methods

### Announcement Management

#### `getCourseAnnouncements`
Retrieves announcements for a specific course.

**Input:**
-   `req.params`: Contains `courseId` (course code)

**Process:**
1.  Fetches course by course code.
2.  Collects all unique `postedBy` faculty IDs from announcements.
3.  Fetches faculty data and builds a lookup table.
4.  Enriches each announcement with faculty details.
5.  Sorts announcements by date in descending order.

**Key Code Snippet**
```javascript
const course = await Course.findOne({ courseCode: courseId });
const facultyMembers = await Faculty.find({ facultyId: { $in: facultyIds } });

const announcementsWithFaculty = course.announcements.map(announcement => ({
  ...announcement.toObject(),
  faculty: facultyLookup[announcement.postedBy] || null
}));
```

announcementsWithFaculty.sort((a, b) => new Date(b.date) - new Date(a.date));
**Output:**
-   Success (200): Returns course object with enriched announcements.
-   Error (404/500): Returns error message.

#### `addCourseAnnouncement`
Adds a new announcement to a course (faculty use).

**Input:**
-   `req.params`: Contains `courseId`
-   `req.body`: Contains `title`, `content`, `importance` (optional), and `postedBy`

**Process:**
1.  Validates required fields.
2.  Fetches course by course code.
3.  Creates new announcement object with current date.
4.  Pushes it to the course's announcement array and saves.

**Key Code Snippet**
```javascript
const newAnnouncement = {
  title,
  content,
  importance: importance || 'Medium',
  date: new Date(),
  postedBy
};

course.announcements.push(newAnnouncement);
await course.save();
```


**Output:**
-   Success (201): Returns success message and added announcement.
-   Error (400/404/500): Returns error message.

#### `updateCourseAnnouncement`
Updates an existing course announcement (faculty use).

**Input:**
-   `req.params`: Contains `courseId`, `announcementId`
-   `req.body`: Contains updated `title`, `content`, `importance`, `attachments` (optional)

**Process:**
1.  Validates required fields.
2.  Locates course and finds announcement index by ID.
3.  Updates the relevant fields in the announcement.
4.  Saves the updated course document.

**Key Code Snippet**
```javascript
const announcementIndex = course.announcements.findIndex(
  ann => ann.id.toString() === announcementId
);

course.announcements[announcementIndex].title = title;
course.announcements[announcementIndex].content = content;
course.announcements[announcementIndex].importance = importance || 'Medium';

if (attachments) {
  course.announcements[announcementIndex].attachments = attachments;
}

await course.save();

```


**Output:**
-   Success (200): Returns success message and updated announcement.
-   Error (400/404/500): Returns error message.

#### `deleteCourseAnnouncement`
Deletes a course announcement (faculty use).

**Input:**
-   `req.params`: Contains `courseId`, `announcementId`

**Process:**
1.  Locates course by course code.
2.  Finds and removes the announcement by ID from the announcements array.
3.  Saves the updated course document.

**Key Code Snippet**
```javascript
const announcementIndex = course.announcements.findIndex(
  ann => ann.id.toString() === announcementId
);

course.announcements.splice(announcementIndex, 1);
await course.save();

```


**Output:**
-   Success (200): Returns success message.
-   Error (404/500): Returns error message.

## Error Handling Strategy

-   All endpoints are wrapped in try-catch blocks.
-   Descriptive error messages and appropriate HTTP status codes.
-   Validation is applied for required fields (`title`, `content`, `postedBy`, etc.).
-   Logs errors to the server console for debugging.

## Business Logic and Enrichment

-   Announcements are enhanced with metadata about the posting faculty.
-   Sorting is applied to show the most recent announcements first.
-   Optional fields like `importance` and `attachments` are supported.