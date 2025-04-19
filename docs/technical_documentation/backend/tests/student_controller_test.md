# Student Controller Test Documentation

## Overview

The student controller test suite ensures robust handling of student profile retrieval, bonafide application management, and related document workflows. All database interactions are mocked to focus on controller logic and to simulate both success and error scenarios.


## Dependencies

- **Controllers Tested**
  - `getStudent`
  - `getStudentBonafideDetails`
  - `createBonafideApplication`
  - `getBonafideApplications`

- **Models Mocked**
  - `Student`
  - `Bonafide`
  - `ApplicationDocument`

- **Libraries and Tools**
  - `jest` for mocking and assertions


## getStudent

**Input**
- Request parameters:
- `id`: String (user ID, required)

**Process**
- Uses the `Student` model to find a student by `userId`.
- Calls `.populate('userId')` to include user details.
- If a student is found, responds with status 200 and the student object.
- If not found, responds with status 404 and an error message.
- Handles missing ID parameter and logs errors as needed.

**Output**
- 200 OK: Returns the student object (including populated user details) if found.
- 404 Not Found: If the student is not found.
- Handles missing ID gracefully (returns 404 or 500 depending on implementation).


## getStudentBonafideDetails

**Input**
- Request parameters:
  - `id`: String (user ID, required)

**Process**
- Uses the `Student` model to find a student by `userId`.
- Calls `.populate('userId')` to get user details.
- If a student is found, constructs a JSON object with:
  - `name` (from `userId.name`)
  - `rollNo`
  - `fatherName`
  - `dateOfBirth` (from `userId.dateOfBirth`)
  - `program`
  - `department`
  - `hostel`
  - `roomNo`
  - `semester`
  - `batch`
  - `enrolledYear` (usually same as `batch`)
- Handles missing or incomplete fields gracefully (returns `undefined` for missing fields).
- Responds with status 200 and the constructed object.
- If not found, responds with status 404 and an error message.
- Handles and logs database errors, responding with status 500 and a generic error message.

**Output**
- 200 OK: Returns a detailed student object for bonafide use, with missing fields as `undefined`.
- 404 Not Found: If the student is not found.
- 500 Internal Server Error: If a database error occurs.


## createBonafideApplication

**Input**
- Request parameters:
  - `id`: String (user ID, required)
- Request body:
  - `currentSemester`: Number (required)
  - `certificateFor`: String (purpose, required)
  - `otherReason`: String (optional, used if `certificateFor` is "Other")

**Process**
- Uses the `Student` model to find a student by `userId`.
- If not found, responds with 404 and an error message.
- If found, creates a new `ApplicationDocument` with:
  - `studentId` (from found student)
  - `documentType`: "Bonafide"
  - `status`: "Pending"
- Saves the `ApplicationDocument`.
- On success, creates a new `Bonafide` document with:
  - `applicationId` (from saved `ApplicationDocument`)
  - `currentSemester`
  - `purpose` (from `certificateFor`)
  - `otherReason` (if applicable)
- Saves the `Bonafide` document.
- Responds with status 201 and a success message including the `applicationId`.
- Handles and logs errors at each step, responding with status 500 and the error message if saving fails.

**Output**
- 201 Created: Returns `{ message: 'Bonafide application submitted successfully', applicationId }` on success.
- 404 Not Found: If the student is not found.
- 500 Internal Server Error: If saving the application or bonafide document fails.


## getBonafideApplications

**Input**
- Request parameters:
  - `id`: String (user ID, required)

**Process**
- Uses the `Student` model to find a student by `userId`.
- If not found, responds with 404 and an error message.
- If found, uses the `ApplicationDocument` model to find all documents for the student with `documentType: 'Bonafide'`.
- Sorts the results (usually by creation date).
- For each application document, uses the `Bonafide` model to find associated bonafide details.
- Aggregates and returns the applications with their bonafide details.
- Handles and logs errors at each step, responding with status 500 and a generic error message if any query fails.

**Output**
- 200 OK: Returns an array of bonafide application records with details.
- 404 Not Found: If the student is not found.
- 500 Internal Server Error: If any database query fails.

