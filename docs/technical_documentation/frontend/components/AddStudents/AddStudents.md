# Add Student via CSV Upload

## Architecture Overview
The Student CSV Upload feature consists of:
1. A React frontend component (`AddStudents.jsx`)
2. A backend endpoint in `acadAdmin.controller.js`
3. Integration with MongoDB models (`User` and `Student`)

## Frontend Implementation

### Component Structure
The `AddStudents` component is built with React and uses the following libraries:
- **React**: For the UI framework
- **Papa Parse**: For CSV parsing
- **React Query**: For state management and API integration

### State Management
The component maintains the following state:

const [students, setStudents] = useState([]);        // Parsed student data from CSV
const [fileName, setFileName] = useState('');        // Name of uploaded file
const [fileChosen, setFileChosen] = useState(false); // Flag to track if file is uploaded

### Key Functions

#### `useAddStudents`
Creates a mutation function using React Query for sending student data to the backend:

return useMutation({
  mutationFn: (students) =>
    newRequest
      .post("/acadadmin/students/add-students", students)
      .then((res) => {
        console.log("Students added successfully:", res.data);
        return res.data;
      }),
});

1. It creates a mutation hook that handles the API request for adding students, encapsulating the POST request logic in a reusable function.
2. The `mutationFn` defines what happens when the mutation is triggered - it sends the students data to the "/acadadmin/students/add-students" endpoint using the custom `newRequest` axios instance.
3. Upon successful response, it logs the success message and returns the response data

#### `handleFileUpload`
Processes the selected CSV file:
1. Updates UI state with file name
2. Uses Papa Parse to convert CSV to JSON
3. Filters out rows with empty values
4. Updates the students state with valid data

#### `handleRemoveFile`
Resets the component state to allow uploading a different file:
1. Clears the students array
2. Resets file name
3. Resets file chosen flag to false
4. Clears the file input reference

#### `handleSubmit`
Submits processed student data to the backend:
1. Validates that students array is not empty
2. Calls the mutation function from `useAddStudents`
3. Handles success and error cases
4. Resets the form on successful submission

### UI Elements
The component includes:
- File upload input with dynamic styling based on state
- Table display of parsed CSV data
- Submit button (disabled when no valid students are available)
- Confirmation/error alert messaging

## Backend Implementation

### API Endpoint
The backend provides the `/acadadmin/students/add-students` endpoint that:
1. Receives an array of student objects
2. Processes each student individually
3. Returns a summary of operations

### Data Processing Flow

#### Input Validation

if (!Array.isArray(studentsData) || studentsData.length === 0) {
  return res.status(400).json({ message: 'No student data provided' });
}

This validation ensures that the request contains an array of student data.

#### Student Processing Loop
For each student in the array:
1. **Extract student data** from the request object
2. **Validate required fields** (name, email, rollNo, etc.)
3. **Check for duplicates** in both User(using email) and Student(using roll number) collections
// Check for existing user/student
      const existingUser = await User.findOne({ email });
      const existingStudent = await Student.findOne({ rollNo });

4. **Skip incomplete or duplicate records** with appropriate logging
// Skip if required fields are missing
      if (
        !name || !email || !rollNo || !fatherName || !motherName ||
        !department || !batch || !program || !hostel || !roomNo
      ) {
        console.warn(`Skipping incomplete student entry: ${email || rollNo}`);
        continue;
      }

5. **Create user account** with bcrypt-hashed password (using rollNo as password)
// Create user
      const newUser = new User({
        name,
        email,
        password: hashedPassword,
        refreshToken: "abc", // dummy string as a refresh token for testing. 
        contactNo,
        address,
        dateOfBirth,
        bloodGroup,
      });

      const savedUser = await newUser.save();

6. **Create student record** linked to the user account
//create student
const newStudent = new Student({
        userId: savedUser._id,
        email,
        rollNo,
        fatherName,
        motherName,
        department,
        semester,
        batch,
        program,
        hostel,
        roomNo,
      });

      const savedStudent = await newStudent.save();

7. **Track successful insertions** for response

#### Response Handling
Returns:
- Success status (201)
- Count of successfully added students
- Data for inserted students and their associated user accounts

### Security Considerations
1. **Password Security**: Passwords are hashed using bcrypt with a salt factor of 10
2. **Duplicate Prevention**: Checks for existing users/students before insertion
3. **Data Validation**: Skips incomplete records instead of failing the entire batch

## Database Schema Implications

### User Model
Fields used:
- name
- email
- password (hashed)
- refreshToken
- contactNo
- address
- dateOfBirth
- bloodGroup

### Student Model
Fields used:
- userId (reference to User)
- email
- rollNo
- fatherName
- motherName
- department
- semester
- batch
- program
- hostel
- roomNo

## Error Handling
- Frontend provides user feedback through alerts
- Backend implements comprehensive try/catch pattern
- Detailed error logging on the server side
- Appropriate HTTP status codes for different error scenarios

## Performance Considerations
- Processing occurs in memory before database operations
- Validations and duplicate checks are performed for each student
- Database operations are performed sequentially, not in batch