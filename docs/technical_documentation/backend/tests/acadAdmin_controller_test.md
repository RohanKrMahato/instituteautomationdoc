# Academic Admin Test

## Overview

This file contains unit tests for the functions in `acadAdmin.controller.js`, covering various admin operations like handling document applications, fee structures, and document access rights.

The test suite uses:
- **Jest**: for unit testing and mocking
- **node-mocks-http**: to simulate HTTP request/response
- **Mocked Mongoose Models**: to replace real DB interactions

##  Test Environment Setup

###   Mocks

```js
jest.mock('../models/documents.models.js');
jest.mock('../models/student.model.js');
jest.mock('../models/course.model.js');


##Lifecycle HOOKS

beforeEach(() => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  jest.clearAllMocks();
});

** Process **
1.Suppresses error logs during test runs.
2.Clears mocks between tests to avoid side effects.


## Application Management

### getAllApplications
** Purpose **
Test how the controller handles database failures when fetching applications.

** Test Case **
- Simulates a database error like "DB Connection Failed" or "Connection timeout"
- Expects HTTP 500 response with an error message.

** Output **
- res.stausCode === 500
- res._getJSONData().message contains the error string

##  filterApplications
** Test Cases **
- Filter by rollNo,type,status
- Handle non-existent roll numbers
- Filter Bonafide applications by status
- Handle invalid roll number formats

** Mocks**
- Student.findOne returns either student or null
- ApplicationDocument.find is chained with .populate().sort().lean()
- Passport.findOne and Bonafide.findOne return type-specific details
- Filter Bonafide applications by status
- Handle invalid roll number formats

** Output:
- Status 200 with matching filtered results
- Status 200 with [] for invalid roll numbers


## getApplicationById

** Purpose **
Retrieve application details by document ID.

** Test Cases **
- Passport application with PassportNumber
- Bonafide application with reason

** Mocks**
- ApplicationDocument.findById().populate().lean()
- Passport.findOne,Bonafide.findOne

** Output **
- Status 200
- Detailed document information returned in response


## updateApplicationStatus
** Purpose
Ensure the controller appends a new remark to existing remarks and saves the updated application.

** Mocks **
- ApplicationDocument.findById returns mock object with save method.

** Output **
- Status 400
- Error message indicating missing or invalid fields
 
## Document Access Management

### getstudentWithDocument Access
** Purpose **
- Verify filtering behavior for fetching students with document access.

** Mocks **
- Filter by name, branch, and semester
- Filter by department ECE and semester 4

** Output**
- Status 200
- List of matched students


###  bulkupdateDocumentAccess
** Purpose **
Ensure input validation for bulk updating student access.

** Test Case **
- studentIds is an empty array
- studentIds is not an array
** Output **
- Status 400
- Error message indicating invalid input






















