# Hostel Controller Test 

## Overview

The hostel controller test suite ensures robust handling of student leave requests, retrieval of leave records (by student and for all students), and updating of leave status. All database interactions are mocked to focus on controller logic and to simulate both success and error scenarios.


## Dependencies

- **Controllers Tested**
  - `studentLeave`
  - `getStudentLeave`
  - `getAllLeaves`
  - `updateAnyLeave`

- **Models Mocked**
  - `Student`
  - `HostelLeave`

- **Libraries and Tools**
  - `jest` for mocking and assertions


## studentLeave

**Input**
- Request body fields:
  - `studentId`: String (required)
  - `email`: String (required)
  - `startDate`: Date (required)
  - `endDate`: Date (required)
  - `reason`: String (required)

**Process**
- Checks if all required fields are present. If any are missing, responds with 400 and an error message.
- Validates that `endDate` is after `startDate`. If not, responds with 400 and an error message.
- Looks up the student by `email` using the `Student` model.
  - If not found, responds with 404 and an error message.
  - If the found student's `rollNo` does not match `studentId`, responds with 400 and an error message.
- If all validations pass, creates a new leave request in the `HostelLeave` model with:
  - `rollNo`, `startDate`, `endDate`, `reason`, and status set to `"Pending"`.
- Handles and reports database errors during student lookup or leave creation.

**Output**
- 200 OK: `{ message: 'Leave request submitted successfully' }` on success.
- 400 Bad Request: If required fields are missing, dates are invalid, or student ID does not match email.
- 404 Not Found: If student is not found.
- 500 Internal Server Error: On database or unexpected errors.


## getStudentLeave

**Input**
- Request parameter:
  - `id`: String (student user ID, required)

**Process**
- Looks up the student by `userId` using the `Student` model.
  - If not found, responds with 404 and an error message.
- If found, retrieves all leave records for the student's `rollNo` using the `HostelLeave` model.
  - If no leaves are found (empty array or null), responds with 404 and an error message.
- Handles and reports database errors during either operation.

**Output**
- 200 OK: Returns an array of leave objects for the student.
- 404 Not Found: If student is not found or no leaves are found.
- 500 Internal Server Error: On database or unexpected errors.


## getAllLeaves

**Input**
- No input parameters.

**Process**
- Retrieves all leave records from the `HostelLeave` model.
  - If no leaves are found (empty array or null), responds with 404 and an error message.
- Handles and reports database errors.

**Output**
- 200 OK: Returns an array of all leave objects.
- 404 Not Found: If no leaves are found.
- 500 Internal Server Error: On database or unexpected errors.


## updateAnyLeave

**Input**
- Request parameters:
  - `id`: String (leave request ID, required)
- Request body:
  - `status`: String (new status, e.g., "Approved" or "Rejected")

**Process**
- Attempts to update the leave record with the specified ID using `HostelLeave.findByIdAndUpdate`, setting the new status.
- If the leave record is not found, responds with 404 and an error message.
- If the update is successful, responds with 200 and the updated leave object.
- Handles and reports database errors.

**Output**
- 200 OK: `{ message: 'Leave request updated successfully', leave: { ...updatedLeave } }` if update is successful.
- 404 Not Found: If leave request is not found.
- 500 Internal Server Error: On database or unexpected errors.

