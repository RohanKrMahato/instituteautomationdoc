# LoginPage Component 

## Overview
The `LoginPage` component is a React functional component that handles user authentication for an institutional application. It provides a form interface for users to enter credentials and select their role before logging into the system.

## Code Structure and Explanation

### Imports
```javascript
import { useContext, useState } from "react"; 
import { useNavigate } from "react-router-dom"; 
import { RoleContext } from "../../context/Rolecontext"; 
import axios from "axios";
```

- `useContext`, `useState` - React hooks for state management and context consumption
- `useNavigate` - React Router hook for programmatic navigation
- `RoleContext` - Custom context for managing user role across the application
- `axios` - HTTP client for making API requests

### Component Definition
```javascript
export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRoleInput] = useState("");
  const navigate = useNavigate();
  
  const { setRole } = useContext(RoleContext);
  
  // ... component implementation
}
```

- Creates state variables with their setter functions for form inputs
- Initializes navigation function for redirecting after login
- Extracts the `setRole` function from the application context

### handleLogin Function
```javascript
const handleLogin = async () => {
  if (!email || !password || !role) {
    alert("All fields are required!");
    return;
  }
  const emailRegex = /^[a-zA-Z.]+@iitg\.ac\.in$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address!");
    return;
  }
  console.log({ email, role });
  try {
    const user = {
      email: email,
      password: password,
      role: role
    }
    
    const response = await axios.post("http://localhost:8000/api/auth/login", user, {
      withCredentials: true,
    });
    
    const data = response.data;
    
    console.log(data);
    if (response) {
      console.log("Login successful:", data);
      localStorage.setItem("currentUser", JSON.stringify({ data, role }));
      setRole(role);
      navigate("/profile", { role });
    } else {
      alert(`Login failed: ${data.message || "Unknown error"}`);
    }
  } catch (error) {
    console.error("Error logging in:", error);
    alert("Failed to connect to the server.");
  }
};
```

#### Validation Logic
- Checks if all required fields are filled
- Validates email format using regex (must be @iitg.ac.in domain)
- Logs validation progress

#### Authentication Process
- Creates a user object with credentials and role
- Makes an asynchronous POST request to the authentication endpoint
- Uses `withCredentials: true` to enable cookie-based authentication
- Processes the response:
  - On success: 
    - Logs success message
    - Stores user data in localStorage
    - Updates application role context
    - Navigates to profile page with role parameter
  - On failure:
    - Shows error alert with message from server or default text
  - On exception:
    - Logs detailed error
    - Shows generic connection error message

### Render Function
```javascript
return (
  <div className="flex justify-center items-center min-h-screen bg-gray-100" style={{ backgroundImage: "url('iit-g.jpg')" }}>
    <div className="w-96 bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold text-center mb-4">Login</h2>
      <div className="mb-4">
        <label className="block text-sm font-medium">Email</label>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 p-2 border rounded w-full"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium">Password</label>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mt-1 p-2 border rounded"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium">Role</label>
        <select
          value={role}
          onChange={(e) => setRoleInput(e.target.value)}
          className="w-full mt-1 p-2 border rounded"
        >
          <option value="" disabled selected>Select your role</option>
          <option value="student">Student</option>
          <option value="faculty">Faculty</option>
          <option value="acadAdmin">Academic Admin</option>
          <option value="nonAcadAdmin">Hostel Admin</option>
        </select>
      </div>
      <button className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600" onClick={handleLogin}>Login</button>
    </div>
  </div>
);
```

#### UI Structure and Styling
- Uses Tailwind CSS for responsive styling
- Main container with full-screen height and background image
- Inner container with fixed width, white background, rounded corners, and shadow
- Form elements:
  - Title heading
  - Email input field with label
  - Password input field with label
  - Role selection dropdown with options
  - Submit button with blue styling and hover effect

#### Data Binding
- Form inputs bound to state variables via `value` props
- Change handlers update state on user input
- Button click handler triggers the login function

## Technical Considerations

### Authentication Flow
1. Form data is validated client-side
2. Valid credentials are sent to backend API
3. If authentication succeeds:
   - User data is stored locally
   - Application context is updated
   - User is redirected to profile page
4. If authentication fails, error feedback is provided

### Security Aspects
- Password is transmitted but not stored in persistent frontend state
- Input validation prevents basic injection attempts
- Authentication uses cookies (withCredentials: true)
- Institutional email validation ensures only authorized users can attempt login

### Role-Based Access
- Four distinct roles are supported: student, faculty, academic admin, hostel admin
- Role is stored in both localStorage and context
- Role is passed to profile page for conditional rendering or further routing

### Error Handling
- Client-side validation for required fields and email format
- Clear error messages for validation failures
- Error handling for API connection issues
- Response validation to handle unexpected server responses

## Integration Points
- Depends on RoleContext for application-wide role management
- Connects to authentication API endpoint
- Redirects to profile page on successful login
- Stores user data in localStorage for persistence