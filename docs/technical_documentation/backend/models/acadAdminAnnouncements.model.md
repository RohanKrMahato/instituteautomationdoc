# AcadAdminAnnouncement Schema

## Overview
The `AcadAdminAnnouncement` schema is a Mongoose model designed for managing announcements. It supports structured storage of announcement details, including title, content, importance level, audience targeting, and timestamps. The schema is built using Mongoose, a MongoDB object modeling tool for Node.js, and includes validation, default values, and middleware for automatic timestamp updates.

## Schema Structure
The schema defines the structure of an announcement document stored in MongoDB. Below is the detailed breakdown of each field:

### Fields
- **title** (`String`)
  - **Description**: The title of the announcement.
  - **Required**: Yes, with an error message: "Please provide announcement title".
  - **Constraints**: Trimmed to remove leading/trailing whitespace.
- **content** (`String`)
  - **Description**: The main body or message of the announcement.
  - **Required**: Yes, with an error message: "Please provide announcement content".
- **importance** (`String`)
  - **Description**: Indicates the priority level of the announcement.
  - **Values**: Enum restricted to `Critical`, `High`, `Medium`, `Low`.
  - **Default**: `Medium`.
- **date** (`Date`)
  - **Description**: The date the announcement was posted.
  - **Default**: Current timestamp (`Date.now`).
- **postedBy** (`String`)
  - **Description**: Identifier or name of the user/admin who posted the announcement.
  - **Required**: Yes.
- **audienceType** (`[String]`)
  - **Description**: Specifies the audience type for the announcement (e.g., "All", "Students", "Faculty").
  - **Default**: `["All"]`.
- **targetEmails** (`[String]`)
  - **Description**: List of specific email addresses targeted for the announcement.
  - **Default**: Empty array (`[]`).
- **targetGroups** (`Object`)
  - **Description**: Defines specific groups or criteria for targeting the announcement audience.
  - **Subfields**:
    - **allUniversity** (`Boolean`): If true, targets the entire university. Default: `true`.
    - **students** (`Boolean`): If true, targets students. Default: `false`.
    - **faculty** (`Boolean`): If true, targets faculty. Default: `false`.
    - **departments** (`[String]`): List of department names. Default: `[]`.
    - **programs** (`[String]`): List of academic programs. Default: `[]`.
    - **semester** (`String`): Specific semester for targeting. Default: `""`.
    - **specificEmails** (`String`): Additional email targeting field (single string). Default: `""`.
- **createdAt** (`Date`)
  - **Description**: Timestamp when the announcement was created.
  - **Default**: Current timestamp (`Date.now`).
- **updatedAt** (`Date`)
  - **Description**: Timestamp when the announcement was last updated.
  - **Default**: Current timestamp (`Date.now`).
  - **Behavior**: Automatically updated to the current timestamp on each save via middleware.

### Middleware
The schema includes a pre-save hook to automatically update the `updatedAt` field whenever the document is saved.

```javascript
AcadAdminAnnouncementSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});
```

## Model
The schema is compiled into a Mongoose model named `AcadAdminAnnouncement`, which is used to interact with the MongoDB collection.

```javascript
export const AcadAdminAnnouncement = mongoose.model('AcadAdminAnnouncement', AcadAdminAnnouncementSchema);
```

## Usage
The `AcadAdminAnnouncement` model can be used to create, read, update, and delete announcement documents in the MongoDB database. Below are examples of common operations.

### Example: Creating an Announcement
```javascript
import { AcadAdminAnnouncement } from './path-to-model';

const newAnnouncement = new AcadAdminAnnouncement({
  title: 'Campus Closure Notice',
  content: 'The campus will be closed on 2025-04-25 due to maintenance.',
  importance: 'Critical',
  postedBy: 'admin@university.edu',
  audienceType: ['All'],
  targetGroups: {
    allUniversity: true,
    students: true,
    faculty: true
  }
});

await newAnnouncement.save();
```

### Example: Querying Announcements
```javascript
// Find all critical announcements
const criticalAnnouncements = await AcadAdminAnnouncement.find({ importance: 'Critical' });

// Find announcements for a specific department
const deptAnnouncements = await AcadAdminAnnouncement.find({
  'targetGroups.departments': 'Computer Science'
});
```

### Example: Updating an Announcement
```javascript
await AcadAdminAnnouncement.findByIdAndUpdate(
  announcementId,
  { content: 'Updated content for the announcement.', importance: 'High' },
  { new: true }
);
```

## Important Code Snippets
Below are the key code snippets for the schema and model definition.

### Schema Definition
```javascript
import mongoose from 'mongoose';

const AcadAdminAnnouncementSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Please provide announcement title'],
    trim: true,
  },
  content: {
    type: String,
    required: [true, 'Please provide announcement content'],
  },
  importance: {
    type: String,
    enum: ['Critical', 'High', 'Medium', 'Low'],
    default: 'Medium',
  },
  date: {
    type: Date,
    default: Date.now,
  },
  postedBy: {
    type: String,
    required: true,
  },  
  audienceType: {
    type: [String], 
    default: ['All']
  },
  targetEmails: {
    type: [String],
    default: []
  },
  targetGroups: {
    allUniversity: {
      type: Boolean,
      default: true
    },
    students: {
      type: Boolean,
      default: false
    },
    faculty: {
      type: Boolean,
      default: false
    },
    departments: {
      type: [String],
      default: [] 
    },
    programs: {
      type: [String],
      default: []
    },
    semester: {
      type: String,
      default: ''
    },
    specificEmails: {
      type: String,
      default: ''
    },
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});
```

### Pre-Save Middleware
```javascript
AcadAdminAnnouncementSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});
```

### Model Export
```javascript
export const AcadAdminAnnouncement = mongoose.model('AcadAdminAnnouncement', AcadAdminAnnouncementSchema);
```

## Validation and Error Handling
- **Required Fields**: The `title`, `content`, and `postedBy` fields are mandatory. Attempting to save a document without these will throw a validation error.
- **Enum Validation**: The `importance` field is restricted to `Critical`, `High`, `Medium`, or `Low`. Invalid values will cause a validation error.
- **Default Values**: Fields like `audienceType`, `targetEmails`, and `targetGroups` subfields have defaults to ensure consistent document structure.

## Dependencies
- **Mongoose**: ^7.0.0 or higher
- **MongoDB**: Compatible with MongoDB 4.0 or higher

## Future Enhancements
- Add support for file attachments (e.g., images or PDFs) using a field like `attachments: [{ type: String, url: String }]`.
- Implement text search capabilities using MongoDB’s text indexes for searching `title` and `content`.
- Add a `status` field (e.g., `Draft`, `Published`, `Archived`) to manage announcement lifecycle.
