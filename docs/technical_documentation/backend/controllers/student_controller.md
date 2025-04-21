# Student Controller

## Overview

The `StudentController` handles student-related functionalities including profile data, course enrollments, document applications, announcements, and course drop operations. It facilitates both student self-service and admin operations through a well-structured set of endpoints.

## Dependencies

```javascript

import { Student } from '../models/student.model.js';
import { Course, StudentCourse, FacultyCourse } from '../models/course.model.js';
import { ApplicationDocument, Bonafide, Passport } from '../models/documents.models.js';
import { Faculty } from '../models/faculty.model.js';
import { CourseDropRequest } from '../models/courseDropRequest.model.js';
import { User } from '../models/user.model.js';`
```

## Controller Methods

### Student Data

#### `getStudent`
Fetches the profile of a specific student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Finds student by `userId`
2.  Populates the associated `User` document

**Key Code Snippet**
```javascript
const studentId = req.params.id;
const user = await Student.findOne({ userId: studentId })
    .populate('userId');
if (!user) {
    return res.status(404).json({ message: 'Student not found' });
}
```

**Output:**
-   Success (200): Returns student document
-   Error (404/500): Appropriate error message

#### `updateStudentProfile`
Updates profile information for a student.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Profile update data

**Process:**
1.  Updates user fields (`name`, `email`, `contactNo`) if present
2.  Updates student model (`hostel`, `roomNo`, `department`, etc.)

**Key Code Snippet**
```javascript
if (updateData.userData) {
    await User.findByIdAndUpdate(
        updateData.userData.userId,
        {
            name: updateData.userData.name,
            email: updateData.userData.email,
            contactNo: updateData.userData.contact
        }
    );
}
const student = await Student.findOneAndUpdate(
    { userId: studentId },
    {
        hostel: updateData.hostel,
        roomNo: updateData.roomNo,
        department: updateData.branch,
        program: updateData.program,
        semester: updateData.semester,
        updatedAt: new Date()
    },
    { new: true }
).populate('userId');
```

**Output:**
-   Success (200): Updated student document
-   Error (404/500): Error message

#### `getStudentFromRollNumber`
Finds the student's userId using their roll number.

**Input:**
-   `req.params.id`: Student's `rollNo`

**Process:**
1.  Searches `Student` model using `rollNo`

**Key Code Snippet**
```javascript
const rollNo = req.params.id;
const student = await Student.findOne({ rollNo: rollNo });
if (!student) {
    return res.status(404).json({ message: 'Student not found' });
}
```

**Output:**
-   Success (200): Returns `userId`
-   Error (404/500): Error message

### Academic Courses

#### `getCompletedCourses`
Fetches completed courses for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `StudentCourse` entries with `isCompleted: true`
2.  Fetches course metadata using `courseCode`
3.  Merges course and performance data

**Key Code Snippet**
```javascript
const user = await Student.findOne({ userId: req.params.id })
    .populate('userId');
const studentCourses = await StudentCourse.find({
    rollNo: user.rollNo,
    isCompleted: true
}).lean();
const courseIds = studentCourses.map(sc => sc.courseId);
const courseDetails = await Course.find({
    courseCode: { $in: courseIds }
}).lean();
```

**Output:**
-   Success (200): Array of completed courses
-   Error (404/500): Error message

#### `getStudentCourses`
Retrieves current approved courses for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Determines session based on current date
2.  Fetches approved `StudentCourse` records
3.  Merges with course data and faculty assignments

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId });
const studentCourses = await StudentCourse.find({ rollNo: student.rollNo, status: 'Approved' });
const courses = await Promise.all(
    studentCourses.map(async (sc) => {
        const course = await Course.findOne({ courseCode: sc.courseId });
        if (!course) return null;
        return {
            id: course.courseCode,
            name: course.courseName,
            credits: course.credits,
            assignments: 8,
            announcements: course.announcements.length,
            attendance: 85
        };
    })
);
```

**Output:**
-   Success (200): Array of current course objects
-   Error (404/500): Appropriate message

#### `dropCourse`
Removes a course from the student's profile.

**Input:**
-   `req.params.studentId`: Student ID
-   `req.params.courseId`: Course ID

**Process:**
1.  Validates student enrollment
2.  Removes course from student and course models

**Key Code Snippet**
```javascript
const student = await Student.findById(studentId);
const courseIndex = student.courses.findIndex(course => course.toString() === courseId);
if (courseIndex === -1) {
    return res.status(404).json({ message: "Course not found in student's enrolled courses" });
}
student.courses.splice(courseIndex, 1);
await student.save();
```

**Output:**
-   Success (200): Confirmation message
-   Error (404): Course or student not found

#### `createCourseDropRequest`
Submits a drop request for an enrolled course.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body.courseId`: Course code

**Process:**
1.  Checks enrollment and pending drop requests
2.  Constructs a `CourseDropRequest` with `Pending` status

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId });
const studentCourse = await StudentCourse.findOne({ 
    rollNo: student.rollNo, 
    courseId: courseId,
    status: 'Approved'
});
const dropRequest = new CourseDropRequest({
    studentId: studentId,
    rollNo: student.rollNo,
    courseId: courseId,
    courseName: course.courseName,
    semester: semester,
    status: 'Pending'
});
await dropRequest.save();
```

**Output:**
-   Success (201): Confirmation and request ID
-   Error (400/404/500): Proper error handling

#### `getStudentDropRequests`
Fetches all course drop requests for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `CourseDropRequest` by `rollNo`
2.  Sorts by most recent

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId });
const dropRequests = await CourseDropRequest.find({ 
    rollNo: student.rollNo 
}).sort({ createdAt: -1 });
```

**Output:**
-   Success (200): Array of drop requests
-   Error (404/500): Error message

#### `cancelDropRequest`
Cancels a pending course drop request.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.params.requestId`: Drop request ID

**Process:**
1.  Verifies ownership and pending status
2.  Deletes the request

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId });
const dropRequest = await CourseDropRequest.findById(requestId);
if (dropRequest.rollNo !== student.rollNo) {
    return res.status(403).json({ message: 'Unauthorized to cancel this request' });
}
await CourseDropRequest.findByIdAndDelete(requestId);
```

**Output:**
-   Success (200): Confirmation
-   Error (400/403/404/500): Validated errors

### Course Announcements

#### `getCourseAnnouncements`
Fetches course announcements along with faculty details.

**Input:**
-   `req.params.courseId`: Course code

**Process:**
1.  Retrieves course and announcement list
2.  Enriches each announcement with faculty metadata
3.  Sorts by latest

**Key Code Snippet**
```javascript
const course = await Course.findOne({ courseCode: courseId });
const facultyIds = [...new Set(course.announcements.map(announcement => announcement.postedBy))];
const facultyMembers = await Faculty.find({ facultyId: { $in: facultyIds } });
const announcementsWithFaculty = course.announcements.map(announcement => {
    const faculty = facultyLookup[announcement.postedBy] || null;
    return { ...announcement.toObject(), faculty };
});
```

**Output:**
-   Success (200): Course document with enhanced announcements
-   Error (404/500): Error message

#### `getFacultyByIds`
Retrieves a list of faculty by their IDs.

**Input:**
-   `req.query.ids`: Comma-separated faculty IDs

**Process:**
1.  Queries `Faculty` model using `$in` filter

**Key Code Snippet**
```javascript
const facultyIds = req.query.ids.split(',');
const facultyMembers = await Faculty.find({ facultyId: { $in: facultyIds } });
```

**Output:**
-   Success (200): Array of faculty documents
-   Error (404/500): Error message

### Bonafide Certificate

#### `getStudentBonafideDetails`
Returns student profile data for bonafide application.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Populates basic user details
2.  Maps required student fields

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId })
    .populate('userId', 'name dateOfBirth');
const studentDetails = {
    name: student.userId.name,
    rollNo: student.rollNo,
    fatherName: student.fatherName,
    dateOfBirth: student.userId.dateOfBirth,
    program: student.program,
    department: student.department,
    hostel: student.hostel,
    roomNo: student.roomNo,
    semester: student.semester,
    batch: student.batch,
    enrolledYear: student.batch
};
```

**Output:**
-   Success (200): Returns data for bonafide application
-   Error (404/500): Error message
`createBonafideApplication`
Submits a new bonafide application.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Includes `currentSemester`, `certificateFor`, `otherReason`

**Process:**
1.  Creates `ApplicationDocument` and `Bonafide` records
2.  Handles conditional reason fields

**Key Code Snippet**
```javascript
const applicationDoc = new ApplicationDocument({
    studentId: student._id,
    documentType: 'Bonafide',
    status: 'Pending'
});
await applicationDoc.save();
const bonafide = new Bonafide({
    applicationId: applicationDoc._id,
    currentSemester,
    purpose: certificateFor,
    otherReason: certificateFor === 'Other' ? otherReason : undefined
});
await bonafide.save();
```

**Output:**
-   Success (201): Application ID
-   Error (404/500): Error message

#### `getBonafideApplications`
Returns all bonafide applications submitted by a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Queries documents of type `Bonafide`
2.  Enriches with bonafide-specific data

**Key Code Snippet**
```javascript
const applications = await ApplicationDocument.find({ 
    studentId: student._id,
    documentType: 'Bonafide'
}).sort({ createdAt: -1 });
const applicationDetails = await Promise.all(applications.map(async (app) => {
    const bonafide = await Bonafide.findOne({ applicationId: app._id });
    if (!bonafide) return null;
    return {
        applicationDate: app.createdAt,
        certificateFor: bonafide.purpose === 'Other' ? bonafide.otherReason : bonafide.purpose,
        currentSemester: bonafide.currentSemester,
        remarks: app.approvalDetails?.remarks || '',
        documentStatus: app.status === 'Pending' ? 'Documents Under Review' : 'Documents Verified',
        currentStatus: app.status
    };
}));
```

**Output:**
-   Success (200): Array of applications
-   Error (404/500): Error message

### Passport Certificate

#### `getStudentPassportDetails`
Fetches student information for passport application.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Fetches student and user profile fields

**Key Code Snippet**
```javascript
const student = await Student.findOne({ userId: studentId })
    .populate('userId', 'name dateOfBirth email');
const studentDetails = {
    name: student.userId.name,
    rollNo: student.rollNo,
    department: student.department,
    programme: student.program,
    dateOfBirth: student.userId.dateOfBirth,
    email: student.userId.email,
    contactNumber: student.userId.contactNo || '',
    hostelName: student.hostel,
    roomNo: student.roomNo,
    fathersName: student.fatherName,
    mothersName: student.motherName
};
```

**Output:**
-   Success (200): Populated profile object
-   Error (404/500): Error message

#### `submitPassportApplication`
Creates a passport application entry.

**Input:**
-   `req.params.id`: Student `userId`
-   `req.body`: Includes `applicationType`, `placeOfBirth`, `semester`, etc.

**Process:**
1.  Creates `ApplicationDocument`
2.  Creates associated `Passport` document

**Key Code Snippet**
```javascript
const applicationDoc = new ApplicationDocument({
    studentId: student._id,
    documentType: 'Passport',
    status: 'Pending'
});
await applicationDoc.save();
const passport = new Passport({
    applicationId: applicationDoc._id,
    applicationType,
    placeOfBirth,
    semester,
    mode,
    tatkalReason,
    travelPlans,
    travelDetails,
    fromDate: travelPlans === 'yes' ? fromDate : undefined,
    toDate: travelPlans === 'yes' ? toDate : undefined
});
await passport.save();
```

**Output:**
-   Success (201): Application ID
-   Error (404/500): Error message


#### `getPassportApplications`
Lists all passport applications for a student.

**Input:**
-   `req.params.id`: Student `userId`

**Process:**
1.  Retrieves `ApplicationDocument` of type `Passport`
2.  Fetches and maps associated `Passport` data

**Key Code Snippet**
```javascript
const applications = await ApplicationDocument.find({
    studentId: student._id,
    documentType: 'Passport'
}).sort({ createdAt: -1 }).lean();
const passportApplications = await Promise.all(
    applications.map(async (app) => {
        const passportDoc = await Passport.findOne({ applicationId: app._id });
        return {
            applicationDate: new Date(app.createdAt).toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }),
            applicationType: passportDoc.applicationType,
            mode: passportDoc.mode,
            remarks: app.approvalDetails?.remarks || '',
            otherDetails: passportDoc.mode === 'tatkal' ? `Tatkal Application - ${passportDoc.tatkalReason}` : 'Regular Application',
            documentStatus: app.status === 'Pending' ? 'Documents Under Review' : 'Documents Verified',
            currentStatus: app.status
        };
    })
);
```

**Output:**
-   Success (200): Array of passport applications
-   Error (404/500): Error message

## Error Handling Strategy
-   All endpoints validate required fields and return specific error messages
-   Logs detailed errors to the console
-   Differentiates between `404`, `400`, and `500` errors for clarity

## Security Considerations
1.  **Authentication & Authorization:**
    -   Assumes upstream middleware handles session validation
2.  **Validation:**
    -   Every endpoint validates inputs before accessing the database
3.  **Sensitive Data:**
    -   Only public student info is exposed; passwords and secure fields are omitted