# CourseForm Component 

## Overview
The `CourseForm` component is a React functional component that provides a user interface for registering new courses in an academic management system. The component allows users to input course details and add multiple program configurations (program/department/semesters/type mappings) before submitting the data to a backend API.

## Code Structure and Explanation

### Imports
```javascript
import React, { useState } from 'react';
import axios from 'axios';
```
- `React` and `useState` hook for component structure and state management
- `axios` for making HTTP requests to the backend API

### Component Definition and State Management
```javascript
const CourseForm = () => {
  const [courseData, setCourseData] = useState({
    courseCode: '',
    courseName: '',
    maxIntake: '',
    faculty: '',
    slot: '',
    credits: '',
    year: '',
    session: ''
  });

  const [config, setConfig] = useState({
    program: '',
    department: '',
    semesters: [],
    type: ''
  });

  const [configurations, setConfigurations] = useState([]);
  
  // ... component implementation
}
```

- **courseData**: Object state that stores the main course details
- **config**: Object state for the current program configuration being edited
- **configurations**: Array state that stores all finalized program configurations

### Event Handlers

#### Course Data Handler
```javascript
const handleCourseChange = (e) => {
  setCourseData({ ...courseData, [e.target.name]: e.target.value });
};
```
- Updates the courseData state using computed property names
- Preserves existing data with the spread operator

#### Configuration Handlers
```javascript
const handleConfigChange = (e) => {
  const { name, value } = e.target;
  setConfig({ ...config, [name]: value });
};

const handleSemesterChange = (e) => {
  const value = e.target.value;
  const isChecked = e.target.checked;

  if (isChecked) {
    setConfig({ ...config, semesters: [...config.semesters, value] });
  } else {
    setConfig({
      ...config,
      semesters: config.semesters.filter((s) => s !== value)
    });
  }
};
```
- `handleConfigChange`: Updates text and select inputs in the config state
- `handleSemesterChange`: Special handler for checkbox group that:
  - Adds semester to array when checked
  - Removes semester from array when unchecked

#### Configuration Management
```javascript
const addConfiguration = () => {
  if (!config.program || !config.department || !config.semesters.length || !config.type) {
    alert('Please fill all fields in configuration');
    return;
  }

  setConfigurations([...configurations, config]);
  setConfig({ program: '', department: '', semesters: [], type: '' });
};
```
- Validates that all configuration fields are filled
- Adds the current config to the configurations array
- Resets the config form fields for the next entry

### Form Submission
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  const payload = {
    ...courseData,
    configurations
  };

  try {
    console.log(payload);
    const res = await axios.post('http://localhost:8000/api/course/register-course', payload);
    alert('Course registered successfully!');
    setCourseData({
      courseCode: '',
      courseName: '',
      maxIntake: '',
      faculty: '',
      slot: '',
      credits: '',
      year: '',
      session: ''
    });
    setConfigurations([]);
  } catch (err) {
    console.error(err);
    alert('Failed to register course');
  }
};
```
- Prevents default form submission behavior
- Creates a combined payload with course data and configurations
- Sends data to backend API using axios
- Provides success/failure feedback via alerts
- Resets form data upon successful submission

### Render Function

```javascript
return (
  <div className="max-w-2xl mx-auto p-6 bg-white rounded shadow">
    <h2 className="text-xl font-bold mb-4">Course Registration</h2>
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Course Details Section */}
      {[
        { name: 'courseCode', label: 'Course Code' },
        { name: 'courseName', label: 'Course Name' },
        {name:'courseDepartment', label:'Course Department'},
        { name: 'faculty', label: 'Faculty ID' },
        { name: 'maxIntake', label: 'Max Intake', type: 'number' },
        { name: 'slot', label: 'Slot' },
        { name: 'credits', label: 'Credits', type: 'number' },
        { name: 'year', label: 'Academic Year (e.g., 2024)' },
        { name: 'session', label: 'Session (e.g., Spring)' }
      ].map((field) => (
        <div key={field.name}>
          <label className="block font-semibold">{field.label}</label>
          <input
            type={field.type || 'text'}
            name={field.name}
            value={courseData[field.name]}
            onChange={handleCourseChange}
            className="w-full border rounded p-2"
            required
          />
        </div>
      ))}

      <hr className="my-4" />

      {/* Program Configuration Section */}
      <h3 className="text-lg font-semibold">Add Program Configuration</h3>
      
      {/* Program, Department, Semester, Type fields */}
      
      <button
        type="button"
        onClick={addConfiguration}
        className="bg-blue-600 text-white px-4 py-2 rounded mt-2"
      >
        Add Configuration
      </button>

      {/* Display Configurations */}
      {configurations.length > 0 && (
        <div className="bg-gray-100 p-4 rounded mt-4">
          <h4 className="font-bold mb-2">Added Configurations</h4>
          <ul className="list-disc list-inside">
            {configurations.map((cfg, index) => (
              <li key={index}>
                Program: {cfg.program}, Dept: {cfg.department}, Semesters: [{cfg.semesters.join(', ')}], Type: {cfg.type}
              </li>
            ))}
          </ul>
        </div>
      )}

      <button
        type="submit"
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Submit Course
      </button>
    </form>
  </div>
);
```

#### UI Structure and Elements
1. **Container**: Centered form with maximum width and shadow styling
2. **Course Details Section**: 
   - Dynamic rendering of form fields using an array map
   - Each field includes a label and an input with appropriate type
   - All fields are required
3. **Program Configuration Section**:
   - Fields for program, department, and course type
   - Checkbox grid for selecting multiple semesters
   - Button to add the current configuration
4. **Configurations Display**:
   - Conditionally rendered when configurations exist
   - List format showing all added configurations
5. **Submit Button**:
   - Green styled button that triggers form submission

## Technical Considerations

### Data Structure
- Course data includes basic details like code, name, faculty, credits
- Each configuration represents a course-program mapping with:
  - Program name
  - Department
  - List of applicable semesters
  - Course type (Core/Elective)

### Form Design Patterns
- Field grouping for logical organization
- Dynamic field rendering for code efficiency
- Two-step data entry (course details + configurations)
- Intermediate data staging with preview capability

### Validation
- Client-side validation ensures configurations have all required fields
- Required attributes on inputs prevent submission with empty fields
- Server-side validation is assumed (not shown in this component)

### User Experience
- Clear visual separation between sections
- Feedback for successful configuration addition
- Visual list of added configurations for verification
- Success/error messages on form submission

### API Integration
- POST request to a dedicated course registration endpoint
- Complete payload includes both course details and configurations
- Error handling with user feedback

## Integration Points
- Connects to course registration API endpoint
- Depends on Tailwind CSS for styling
- Assumes authorization/authentication is handled elsewhere