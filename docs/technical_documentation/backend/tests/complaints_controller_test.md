# Complaints Controller Test

## Overview

This document ensures that all core functionalities of the complaints controller are robust and reliable. The suite covers complaint creation, retrieval (by user and by status), updating complaint status, and deleting complaints. Each function is tested for both successful operation and appropriate error handling, guaranteeing a resilient complaint management system.


## Dependencies

**Controllers Tested**
- `createComplaint`
- `getComplaintsByUser`
- `getComplaintsByStatus`
- `updateComplaintStatus`
- `deleteComplaint`

**Models Mocked**
- `Complaint`
- `User`

**Libraries and Tools**
- `jest` for mocking and assertions
- `mongoose` for ObjectId and error simulation
- `jsonwebtoken` for authentication (if used in controller)
- Express.js mock request/response objects


## createComplaint

**Input**
- Expects a JSON body with:
  - `userId`: String (required)
  - `title`: String (required)
  - `description`: String (required)
  - `category`: String (optional)
  - Additional fields as per schema

**Process**
- Validates that all required fields (`userId`, `title`, `description`) are present.
- Checks if the user exists in the database.
- Creates a new complaint document with the provided data and sets default status (e.g., "pending").
- Saves the complaint to the database.
- Handles validation errors (missing fields) and database errors.

**Output**
- 400 Bad Request: If any required field is missing.
- 404 Not Found: If the user does not exist.
- 201 Created: On successful complaint creation, returns the complaint data.
- 500 Internal Server Error: On database or unexpected errors.


## getComplaintsByUser

**Input**
- Expects:
  - `userId` as a URL parameter or query parameter.

**Process**
- Validates that `userId` is provided.
- Queries the complaints collection for all complaints associated with the given user ID.
- Handles cases where no complaints are found or if the user does not exist.

**Output**
- 400 Bad Request: If `userId` is missing.
- 404 Not Found: If no complaints are found for the user.
- 200 OK: Returns an array of complaints for the user.
- 500 Internal Server Error: On database or unexpected errors.


## getComplaintsByStatus

**Input**
- Expects:
  - `status` as a query parameter (e.g., "pending", "resolved", "in-progress").

**Process**
- Validates that the `status` parameter is provided and valid.
- Queries the complaints collection for all complaints matching the given status.
- Handles cases where no complaints match the status.

**Output**

- 400 Bad Request: If `status` is missing or invalid.
- 404 Not Found: If no complaints are found with the specified status.
- 200 OK: Returns an array of complaints matching the status.
- 500 Internal Server Error: On database or unexpected errors.


## updateComplaintStatus

**Input**
- Expects a JSON body with:
  - `complaintId`: String (required)
  - `status`: String (required, e.g., "resolved", "in-progress", "rejected")

**Process**
- Validates that both `complaintId` and `status` are provided.
- Finds the complaint by its ID.
- Updates the complaint's status field.
- Saves the updated complaint document.
- Handles cases where the complaint does not exist or if the status is invalid.

**Output**
- 400 Bad Request: If required fields are missing or status is invalid.
- 404 Not Found: If the complaint is not found.
- 200 OK: Returns the updated complaint.
- 500 Internal Server Error: On database or unexpected errors.


## deleteComplaint

**Input**
- Expects:
  - `complaintId` as a URL parameter or in the request body.

**Process**
- Validates that `complaintId` is provided.
- Finds and deletes the complaint document by its ID.
- Handles cases where the complaint does not exist.

**Output**
- 400 Bad Request: If `complaintId` is missing.
- 404 Not Found: If the complaint is not found.
- 200 OK: Returns a success message or the deleted complaint data.
- 500 Internal Server Error: On database or unexpected errors.

