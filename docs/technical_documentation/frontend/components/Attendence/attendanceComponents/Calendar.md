# MyCalendar

## Overview

The `MyCalendar` component is a React component that displays student attendance data in a calendar format. It leverages the `react-big-calendar` library to render a customizable calendar view that visualizes attendance events. The component adapts its behavior based on user roles, showing either the logged-in student's attendance or a selected student's attendance for administrative users.

## Dependencies

The component relies on several external libraries and utilities:

- **react-big-calendar**: Provides the calendar UI and functionality
- **moment**: Handles date formatting and manipulation
- **react-router-dom**: Accesses URL parameters
- **@tanstack/react-query**: Manages API data fetching and caching
- **Context API**: Accesses role information through `RoleContext`

## Props

| Prop | Type | Description |
|------|------|-------------|
| `selectedStudent` | String | Optional roll number of a student whose attendance data should be displayed (used when an admin/teacher selects a specific student) |

## State Management

The component manages several state variables using React's `useState` hook:

| State Variable | Type | Description |
|----------------|------|-------------|
| `myEventsList` | Array | Stores the list of attendance events to display on the calendar |
| `view` | String | Controls the current calendar view (month, week, or day) |
| `date` | Date | Controls the current date the calendar is focused on |

## Data Fetching

The component uses two different data fetching mechanisms:

1. **React Query**: Fetches student profile data for the currently logged-in user
2. **Fetch API**: Retrieves attendance events for the specified course and student

### User Data Retrieval

The component retrieves the current user's data from local storage and uses React Query to fetch additional student details:

```jsx
const {data:userData} = JSON.parse(localStorage.getItem("currentUser"));
const {email, userId} = userData.user;

const { isLoading, error, data } = useQuery({
    queryKey: [`${userId}`],
    queryFn: () =>
        newRequest.get(`/student/${userId}`).then((res) => {
            return res.data;
        }),
});
```

### Attendance Data Fetching

Attendance data is fetched using the native Fetch API within a `useEffect` hook:

```jsx
useEffect(() => {
    const fetchData = async () => {
        let rollNoToFetch;
        
        if (role === 'student') {
            rollNoToFetch = data?.rollNo;
        } else if (selectedStudent) {
            rollNoToFetch = selectedStudent;
        }
        if (rollNoToFetch) {
            await fetchEventData(rollNoToFetch);
        }
    };

    fetchData();
}, [selectedStudent, role, courseId]);
```

The `fetchEventData` function handles the actual API call:

```jsx
const fetchEventData = async (rollNo) => {
    try {
        const response = await fetch(`http://localhost:8000/api/attendancelanding/student/${courseId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "rollno": rollNo,
            },
        });

        const dataRecieved = await response.json();

        if (response.ok) {
            setMyEventsList(dataRecieved.eventList || []);
            console.log('Updated events:', dataRecieved.eventList);
        } else {
            console.error("Error fetching attendance data:", dataRecieved.error);
        }
    } catch (error) {
        console.error("Error fetching attendance data:", error);
    }
};
```

## Role-Based Logic

The component implements role-based logic to determine whose attendance data to display:

- For students (`role === 'student'`), it displays the logged-in user's attendance
- For other roles (instructors/administrators), it displays the selected student's attendance

## Calendar Configuration

The calendar is configured with the following settings:

- Multiple view options (month, week, day)
- Dynamic view state management
- Date navigation controls
- Event data binding
- Fixed height styling

```jsx
<Calendar
    views={[Views.MONTH, Views.WEEK, Views.DAY]}
    defaultView={view}
    view={view}
    date={date}
    onView={setView}
    onNavigate={setDate}
    localizer={localizer}
    events={myEventsList}
    startAccessor="start"
    endAccessor="end"
    style={{ height: 350 }}
/>
```

## API Integration

| Endpoint | Method | Purpose | Request Headers |
|----------|--------|---------|----------------|
| `/student/${userId}` | GET | Fetch student profile data | Default headers via `newRequest` utility |
| `/api/attendancelanding/student/${courseId}` | GET | Fetch attendance events | `Content-Type` and `rollno` |

## Code Breakdown

### Initialization and Setup

```jsx
const localizer = momentLocalizer(moment);
function MyCalendar({ selectedStudent }) { 
    // User data retrieval from localStorage
    const {data:userData} = JSON.parse(localStorage.getItem("currentUser"));
    const {email, userId} = userData.user;
    
    // React Query hook for fetching student data
    const { isLoading, error, data } = useQuery({...});
    
    // Context and params hooks
    const { role } = useContext(RoleContext);
    const { id: courseId } = useParams();
    
    // State initialization
    const [myEventsList, setMyEventsList] = useState([]);
    const [view, setView] = useState(Views.WEEK);
    const [date, setDate] = useState(new Date());
    
    // Rest of component...
}
```

This section:
1. Creates a localizer for the calendar using moment.js
2. Retrieves user data from localStorage
3. Sets up React Query for additional data fetching
4. Accesses the user's role from context
5. Gets the course ID from URL parameters
6. Initializes state variables for events, view, and current date

### Data Fetching Effect

The `useEffect` hook determines which student's data to fetch based on the user's role:

```jsx
useEffect(() => {
    const fetchData = async () => {
        let rollNoToFetch;
        
        if (role === 'student') {
            rollNoToFetch = data?.rollNo;
        } else if (selectedStudent) {
            rollNoToFetch = selectedStudent;
        }
        if (rollNoToFetch) {
            await fetchEventData(rollNoToFetch);
        }
    };

    fetchData();
}, [selectedStudent, role, courseId]);
```

This effect runs whenever the selected student, user role, or course ID changes.

### Render Method

```jsx
return (
    <div className='calendar-box'>
        <Calendar
            views={[Views.MONTH, Views.WEEK, Views.DAY]}
            defaultView={view}
            view={view}
            date={date}
            onView={setView}
            onNavigate={setDate}
            localizer={localizer}
            events={myEventsList}
            startAccessor="start"
            endAccessor="end"
            style={{ height: 350 }}
        />
    </div>
);
```

The render method is straightforward, returning a div containing the configured Calendar component.

## Usage Notes

1. The component requires user authentication to function properly, as it retrieves the current user from localStorage
2. The component expects to be used within a route that includes a course ID parameter
3. The `RoleContext` must be properly set up and provided higher in the component tree
4. The API endpoints must be available and return data in the expected format
5. The component assumes the attendance events from the API include `start` and `end` properties as required by react-big-calendar
6. Debug information is logged to the console for development purposes
7. For non-student roles, a `selectedStudent` prop should be provided to view a specific student's attendance

## Data Format

The expected format for attendance events in `myEventsList`:

```javascript
[
  {
    title: "Present" | "Absent" | "Other status",
    start: Date,  // Event start date/time
    end: Date,    // Event end date/time
    allDay: Boolean,  // Whether the event spans the entire day
    // Additional properties as needed
  },
  // More events...
]
```