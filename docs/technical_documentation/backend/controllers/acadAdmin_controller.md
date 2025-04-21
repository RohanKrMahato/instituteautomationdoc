# Faculty and Student Management API

This document provides a comprehensive overview of the Faculty and Student Management API, detailing its core functionalities, implementation, and key code snippets. The API is built using Node.js, Express, Mongoose, and MongoDB, designed to manage faculty, students, applications, fees, course drop requests, and document access within an educational institution.

---

## Overview

The API provides endpoints for:
- **Faculty Management**: Adding faculty members with their academic and personal details.
- **Student Management**: Bulk addition of students and managing their document access.
- **Application Management**: Handling document applications (e.g., Bonafide, Passport) with filtering, status updates, and comments.
- **Fee Management**: Managing fee structures, including creation, retrieval, updates, and status toggling.
- **Course Drop Requests**: Managing student requests to drop courses, including approval and enrollment updates.
- **Department Retrieval**: Fetching unique departments from student records.

---

## Key Features and Implementation Details

### 1. Add Faculty (`addFaculty`)

**Purpose**: Creates a new faculty member with associated user and faculty records.

**Implementation**:
- Validates if a user with the provided email already exists.
- Hashes the email as a password using `bcrypt` for security.
- Creates a `User` document with personal details and a dummy refresh token.
- Creates a `Faculty` document linked to the user with academic details.

**Key Code Snippet**:
```javascript
const hashedPassword = await bcrypt.hash(email, 10);
const newUser = new User({
  name, email, password: hashedPassword, refreshToken: "abc",
  contactNo, address, dateOfBirth, bloodGroup
});
const savedUser = await newUser.save();
const newFaculty = new Faculty({
  userId: savedUser._id, email, department, designation,
  yearOfJoining, specialization, qualifications, experience,
  publications, achievements, conferences
});
const savedFaculty = await newFaculty.save();
```

**Explanation**:
- The email is hashed to create a secure password.
- The `User` model stores general user information, while the `Faculty` model stores academic-specific details.
- The `userId` links the `Faculty` document to the `User` document.

---

### 2. Add Students in Bulk (`addStudents`)

**Purpose**: Adds multiple students in a single request, creating user and student records.

**Implementation**:
- Accepts an array of student objects.
- Validates required fields and checks for duplicates (email or roll number).
- Hashes the roll number as a password.
- Creates `User` and `Student` documents for each valid student.

**Key Code Snippet**:
```javascript
for (const student of studentsData) {
  const existingUser = await User.findOne({ email });
  const existingStudent = await Student.findOne({ rollNo });
  if (existingUser || existingStudent) continue;
  const hashedPassword = await bcrypt.hash(rollNo, 10);
  const newUser = new User({ name, email, password: hashedPassword, ... });
  const savedUser = await newUser.save();
  const newStudent = new Student({ userId: savedUser._id, email, rollNo, ... });
  const savedStudent = await newStudent.save();
  insertedStudents.push({ student: savedStudent, user: savedUser });
}
```

**Explanation**:
- Iterates through the student data, skipping entries with missing required fields or duplicates.
- Uses `bcrypt` to hash the roll number for secure password storage.
- Links `Student` to `User` via `userId`.

---

### 3. Get All Applications (`getAllApplications`)

**Purpose**: Retrieves paginated document applications with student details.

**Implementation**:
- Supports pagination via `page` and `limit` query parameters.
- Populates `studentId` and `userId` to include student and user details.
- Enriches response with student names.

**Key Code Snippet**:
```javascript
const applications = await ApplicationDocument.find()
  .populate({
    path: "studentId",
    select: "rollNo department program userId",
    populate: { path: "userId", select: "name" }
  })
  .sort({ createdAt: -1 })
  .limit(limit * 1)
  .skip((page - 1) * limit)
  .lean();
const enrichedApplications = applications.map(app => ({
  ...app,
  studentId: { ...app.studentId, name: app.studentId?.userId?.name }
}));
```

**Explanation**:
- Uses Mongoose’s `populate` to fetch related student and user data.
- Applies pagination using `limit` and `skip`.
- Transforms the response to include the student’s name directly in `studentId`.

---

### 4. Filter Applications (`filterApplications`)

**Purpose**: Filters applications by roll number, document type, and status.

**Implementation**:
- Builds a dynamic query based on query parameters.
- Populates student and approval details.
- Fetches specific document details (e.g., Bonafide, Passport) based on `documentType`.

**Key Code Snippet**:
```javascript
if (rollNo) {
  const student = await Student.findOne({ rollNo: { $regex: `^${rollNo}`, $options: "i" } });
  if (student) query.studentId = student._id;
  else return res.status(200).json([]);
}
const applications = await ApplicationDocument.find(query)
  .populate({ path: "studentId", select: "...", populate: { path: "userId", select: "..." } })
  .populate("approvalDetails.approvedBy", "name")
  .sort({ createdAt: -1 })
  .lean();
const detailedApplications = await Promise.all(
  applications.map(async app => {
    let details;
    switch (app.documentType) {
      case "Bonafide": details = await Bonafide.findOne({ applicationId: app._id }); break;
      case "Passport": details = await Passport.findOne({ applicationId: app._id }); break;
    }
    return { ...app, details, studentName: app.studentId?.userId?.name || "N/A", ... };
  })
);
```

**Explanation**:
- Uses regex for partial roll number matching.
- Dynamically fetches document-specific details using a `switch` statement.
- Enriches response with student and document details.

---

### 5. Update Application Status (`updateApplicationStatus`)

**Purpose**: Updates the status of an application and adds remarks.

**Implementation**:
- Validates required fields and converts status to proper case.
- Initializes `approvalDetails` if absent.
- Updates status and remarks, saving the changes.

**Key Code Snippet**:
```javascript
const properStatus = status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
application.status = properStatus;
if (remarks) {
  if (!application.approvalDetails.remarks) application.approvalDetails.remarks = [];
  application.approvalDetails.remarks.push(remarks);
}
application.updatedAt = new Date();
const updatedApplication = await application.save();
```

**Explanation**:
- Ensures consistent status formatting (e.g., "Approved" instead of "approved").
- Safely handles remarks addition with array initialization.

---

### 6. Manage Fee Structure (`addFeeStructure`, `getFeeBreakdown`, `toggleFeeBreakdownStatus`, `updateFeeBreakdown`)

**Purpose**: Manages fee structures for programs and semesters.

**Implementation**:
- `addFeeStructure`: Creates or updates a fee structure based on program and semester parity.
- `getFeeBreakdown`: Retrieves fee structures with optional filtering.
- `toggleFeeBreakdownStatus`: Toggles the `isActive` flag.
- `updateFeeBreakdown`: Updates specific fields of a fee structure.

**Key Code Snippet** (addFeeStructure):
```javascript
const existingStructure = await FeeBreakdown.findOne({
  program: processedData.program,
  semesterParity: processedData.semesterParity
});
if (existingStructure) {
  const updatedStructure = await FeeBreakdown.findByIdAndUpdate(
    existingStructure._id,
    { ...processedData, updatedAt: new Date() },
    { new: true }
  );
  return res.status(200).json({ message: "Fee structure updated successfully", ... });
}
const newStructure = new FeeBreakdown(processedData);
await newStructure.save();
```

**Explanation**:
- Checks for existing structures to avoid duplicates.
- Updates or creates a new `FeeBreakdown` document as needed.

---

### 7. Manage Course Drop Requests (`getDropRequests`, `updateDropRequestStatus`)

**Purpose**: Handles student course drop requests and their approval.

**Implementation**:
- `getDropRequests`: Fetches all drop requests with student and course details.
- `updateDropRequestStatus`: Updates request status and removes student enrollment if approved.

**Key Code Snippet** (updateDropRequestStatus):
```javascript
if (status === 'Approved') {
  const student = await Student.findOne({ rollNo: request.rollNo });
  const course = await Course.findOne({ courseCode: request.courseId });
  await StudentCourse.deleteOne({ rollNo: student.rollNo, courseId: course.courseCode });
  await Course.updateOne(
    { courseCode: course.courseCode },
    { $pull: { students: student.userId } }
  );
}
```

**Explanation**:
- On approval, removes the student from the `StudentCourse` and `Course` models.
- Includes robust error handling for missing students or courses.

---

### 8. Manage Student Document Access (`getStudentsWithDocumentAccess`, `updateStudentDocumentAccess`, `bulkUpdateDocumentAccess`)

**Purpose**: Manages student access to documents (transcript, ID card, fee receipt).

**Implementation**:
- `getStudentsWithDocumentAccess`: Retrieves paginated students with access details.
- `updateStudentDocumentAccess`: Updates access for a single student.
- `bulkUpdateDocumentAccess`: Updates access for multiple students.

**Key Code Snippet** (updateStudentDocumentAccess):
```javascript
const student = await Student.findByIdAndUpdate(
  id,
  {
    $set: {
      "documentAccess.transcript": !!access.transcript,
      "documentAccess.idCard": !!access.idCard,
      "documentAccess.feeReceipt": !!access.feeReceipt,
      updatedAt: new Date()
    }
  },
  { new: true }
).populate("userId", "name email contactNo");
```

**Explanation**:
- Uses `$set` to update specific document access fields.
- Ensures boolean values with `!!` operator.

---

### 9. Get All Departments (`getAllDepartments`)

**Purpose**: Retrieves unique departments from student records.

**Implementation**:
- Fetches all students and extracts unique department names using a `Set`.

**Key Code Snippet**:
```javascript
const students = await Student.find({});
const departments = students.map(student => student.department);
const uniqueDepartments = [...new Set(departments)];
```

**Explanation**:
- Simple yet efficient use of `Set` to eliminate duplicates.

---

## Error Handling

- **Try-Catch Blocks**: All endpoints use try-catch to handle errors gracefully.
- **Validation**: Input validation ensures required fields are present and valid.
- **Logging**: Console logs are used for debugging, especially in error scenarios.
- **HTTP Status Codes**:
  - `200`: Successful operation.
  - `201`: Resource created.
  - `400`: Bad request (invalid input).
  - `404`: Resource not found.
  - `500`: Server error.

---

## Security Considerations

- **Password Hashing**: Uses `bcrypt` to securely hash passwords.
- **Duplicate Checks**: Prevents duplicate users/students via email and roll number checks.
- **Data Validation**: Ensures required fields are present and properly formatted.
- **Dummy Refresh Token**: Currently uses a placeholder; production should implement proper JWT-based authentication.

---

## Performance Optimizations

- **Lean Queries**: Uses `.lean()` to reduce memory usage for read-heavy operations.
- **Pagination**: Implements pagination for large datasets (e.g., applications, students).
- **Indexes**: Assumes MongoDB indexes on fields like `email`, `rollNo`, and `program` for faster queries (not shown in code but recommended).

---