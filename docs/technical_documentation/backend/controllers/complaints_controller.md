# Complaints Controller

## Overview

The `ComplaintsController` manages the business logic for handling user complaints within the Institute Automation System. This controller provides functionality for users to create, retrieve, and delete complaints, as well as for administrators to manage complaints and support staff.

## Dependencies

```javascript
import { HostelAdmin as Admin } from "../models/hostelAdmin.model.js";
import { Complaint, SupportStaff } from "../models/complaint.model.js";
import { promises as fs } from 'fs';
import path from 'path';
import { Buffer } from 'buffer';
```

## Controller Methods

### User Complaint Management

#### `createComplaint`
Creates a new complaint in the system.

**Input:**
- `req.body`: Contains complaint details (title, date, description, phoneNumber, timeAvailability, address, locality, category, subCategory, images)
- `req.user`: Contains user information including userId

**Process:**
1. Extracts complaint details from request body
2. Processes and saves any base64-encoded images to the server's filesystem
3. Creates a new Complaint document with the user's data
4. Saves the complaint to the database

**Key Code Snippet**
```javascript
const buffer = Buffer.from(image, 'base64');
await fs.writeFile(path.join(process.cwd(), 'uploads/complaints', filePath), buffer);

const complaint = new Complaint({ ...req.body, userId: req.user.userId, imageUrls: imageNames });
await complaint.save();

```

**Output:**
- Success (201): Returns message and complaint object
- Error (500): Returns error message

**Error Handling:**
- Logs any failures in image processing or database operations
- Returns appropriate status codes and messages

#### `getUserComplaints`
Retrieves complaints created by the authenticated user with pagination.

**Input:**
- `req.body`: May contain pagination options (page, limit)
- `req.user`: Contains userId for the requesting user

**Process:**
1. Extracts pagination parameters (defaulting to page 1, limit 10)
2. Queries the database for complaints matching the user's ID
3. Calculates pagination metadata

**Key Code Snippet**
```javascript
const complaints = await Complaint.find({ userId }).skip(skip).limit(limit).sort({ createdAt: -1 });

```

**Output:**
- Success (200): Returns complaints array and pagination information
- Error (500): Returns error message

#### `deleteComplaint`
Deletes a user's complaint if it's not already resolved.

**Input:**
- `req.body`: Contains _id (complaintId)
- `req.user`: Contains userId for the requesting user

**Process:**
1. Verifies complaint exists and belongs to the requesting user
2. Checks if complaint is in "Resolved" status (preventing deletion)
3. Deletes any associated image files from the filesystem
4. Removes the complaint from the database

**Key Code Snippet**
```javascript
if (complaint.userId.toString() !== userId) return res.status(403).json({ message: "User don't have access" });

for (const imagePath of complaint.imageUrls) {
  await fs.unlink(path.join(process.cwd(), 'uploads/complaints', imagePath));
}
await Complaint.findByIdAndDelete(complaintId);

```

**Output:**
- Success (200): Returns success message
- Error (400/403/404/500): Returns appropriate error message

**Authorization:**
- Verifies requesting user owns the complaint
- Prevents deletion of resolved complaints

### Admin Complaint Management

#### `getAllComplaints`
Retrieves all complaints in the system (admin only).

**Input:**
- `req.body`: May contain pagination options (page, limit)
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Extracts pagination parameters
3. Retrieves paginated complaints from the database

**Key Code Snippet**
```javascript
const admin = await Admin.findOne({ email: req.user.email });
const complaints = await Complaint.find().skip(skip).limit(limit).sort({ createdAt: -1 });

```

**Output:**
- Success (200): Returns complaints array and pagination information
- Error (403/500): Returns appropriate error message

**Authorization:**
- Verifies requesting user is an admin by checking the Admin model

#### `updateStatus`
Updates the status of a complaint (admin only).

**Input:**
- `req.body`: Contains complaintId and updatedStatus
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Updates the complaint's status
3. If status is changed to "Resolved" and complaint was assigned, updates staff records

**Key Code Snippet**
```javascript
const updatedComplaint = await Complaint.findByIdAndUpdate(complaintId, { status: updatedStatus }, { new: true });

if (updatedStatus === 'Resolved' && complaint.assignedStaffId) {
  await SupportStaff.findByIdAndUpdate(complaint.assignedStaffId, { $pull: { assignedComplaints: complaintId } });
}

```

**Output:**
- Success (200): Returns success message and updated complaint
- Error (400/403/404/500): Returns appropriate error message

#### `assignComplaint`
Assigns a complaint to a support staff member (admin only).

**Input:**
- `req.body`: Contains complaintId and supportStaffId
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Checks if support staff exists and has capacity for another complaint
3. If complaint is already assigned, removes it from previous staff's assignments
4. Updates complaint with staff information and changes status to "In Progress"
5. Adds complaint to staff's assigned complaints list

**Key Code Snippet**
```javascript
if (supportStaff.assignedComplaints.length >= 5) return res.status(400).json({ message: "Support staff is busy" });

await Complaint.findByIdAndUpdate(complaintId, {
  assignedName: supportStaff.name,
  assignedStaffId: supportStaffId,
  status: "In Progress"
});
await SupportStaff.findByIdAndUpdate(supportStaffId, { $addToSet: { assignedComplaints: complaintId } });

```

**Output:**
- Success (200): Returns success message and updated complaint
- Error (400/403/404/500): Returns appropriate error message

**Business Rules:**
- Staff cannot be assigned more than 5 active complaints
- Re-assignment handles removal from previous staff's list

#### `getComplaintsByStatus`
Retrieves complaints filtered by status with pagination (admin only).

**Input:**
- `req.body`: Contains status and optional pagination options (page, limit)
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Extracts status filter and pagination parameters
3. Queries the database for complaints matching the status

**Output:**
- Success (200): Returns filtered complaints array and pagination information
- Error (400/403/500): Returns appropriate error message

#### `getComplaintById`
Retrieves detailed information about a specific complaint.

**Input:**
- `req.params`: Contains id (complaintId)

**Process:**
1. Retrieves the complaint document by ID

**Output:**
- Success (200): Returns success message and complaint details
- Error (400/404/500): Returns appropriate error message

### Support Staff Management

#### `createSupportStaff`
Creates a new support staff member (admin only).

**Input:**
- `req.body`: Contains staff details (name, phone, etc.)
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Creates a new SupportStaff document
3. Saves the staff to the database

**Key Code Snippet**
```javascript
const supportStaff = new SupportStaff(req.body);
await supportStaff.save();

```

**Output:**
- Success (201): Returns success message and staff object
- Error (403/500): Returns appropriate error message

#### `deleteSupportStaff`
Removes a support staff member from the system (admin only).

**Input:**
- `req.body`: Contains supportStaffId
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Deletes the support staff document from the database

**Key Code Snippet**
```javascript
await SupportStaff.findByIdAndDelete(req.body.supportStaffId);

```

**Output:**
- Success (200): Returns success message
- Error (403/404/500): Returns appropriate error message

#### `getAllSupportStaff`
Retrieves all support staff in the system (admin only).

**Input:**
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Retrieves all support staff from the database

**Key Code Snippet**
```javascript
const supportStaff = await SupportStaff.find();

```

**Output:**
- Success (200): Returns success message and staff array
- Error (403/500): Returns appropriate error message

#### `getFilteredSupportStaff`
Retrieves support staff filtered by category and subcategory (admin only).

**Input:**
- `req.query`: Contains category and subCategory
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies the requesting user is an admin
2. Queries the database for staff matching the category/subcategory criteria
3. Sorts results by number of assigned complaints

**Key Code Snippet**
```javascript
const supportStaff = await SupportStaff.find({
  $and: [
    { $expr: { $lt: [{ $size: { $ifNull: ["$assignedComplaints", []] } }, 5] } },
    {
      $or: [
        { categories: { $in: [category] } },
        { categories: { $size: 0 } },
        { categories: { $exists: false } }
      ]
    },
    {
      $or: [
        { subCategories: { $in: [subCategory] } },
        { subCategories: { $size: 0 } },
        { subCategories: { $exists: false } }
      ]
    }
  ]
});

```

**Output:**
- Success (200): Returns success message and filtered staff array
- Error (400/403/500): Returns appropriate error message

**Business Logic:**
- Returns staff who handle the specific category/subcategory
- Returns staff with fewer than 5 assigned complaints
- Prioritizes staff with fewer current assignments

#### `updateSupportStaffAvailability`
Updates a support staff's availability status (admin only).

**Input:**
- `req.body`: Contains supportStaffId and isAvailable
- `req.user`: Contains email for authorization check

**Process:**
1. Verifies inputs are valid
2. Updates the staff's availability status in the database

**Key Code Snippet**
```javascript
await SupportStaff.findByIdAndUpdate(supportStaffId, { isAvailable }, { new: true });

```

**Output:**
- Success (200): Returns success message and updated staff object
- Error (400/404/500): Returns appropriate error message

## Error Handling Strategy

The controller implements comprehensive error handling throughout:
- Input validation with descriptive error messages
- Authentication/authorization checks with 403 responses
- Resource not found scenarios with 404 responses
- Server errors with 500 responses
- Detailed console logging for troubleshooting

## File System Operations

For complaint images, the controller:
1. Receives Base64-encoded images in request body
2. Decodes to binary data
3. Creates a unique filename with timestamp
4. Saves to `uploads/complaints` directory
5. Stores filename references in the complaint document
6. Deletes files when complaint is deleted

## Performance Considerations

The controller implements several performance optimizations:
- Pagination for all list endpoints
- Appropriate MongoDB indexing on commonly queried fields
- Minimized in-memory processing except where necessary (e.g., complex sorting)
- Efficient query patterns using MongoDB's aggregation pipeline where appropriate

## Security Considerations

1. **Authorization:**
   - All administrative operations require admin authentication
   - User operations are limited to their own resources
   - Role-based access control patterns throughout

2. **Input Validation:**
   - All user inputs are validated before processing
   - Proper error responses for invalid inputs

3. **File Operations:**
   - Secure file naming with timestamps to prevent collisions
   - Created files are properly associated with complaint records
   - Clean-up operations for deleted resources