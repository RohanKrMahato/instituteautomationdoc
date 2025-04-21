# AllAnnouncements Component: Technical Documentation

## Overview

The `AllAnnouncements` component is a React functional component responsible for fetching, filtering, and displaying a list of announcements to a student. It leverages several libraries and techniques for efficient data handling and a user-friendly interface.

## Dependencies

- **React (`useState`, `useEffect`):**  Manages component state and lifecycle.
- **`react-router-dom` (`Link`):** Enables navigation within the application.
- **`react-icons/fa`:** Provides Font Awesome icons for visual enhancements.
- **`@tanstack/react-query` (`useQuery`):**  Facilitates efficient data fetching, caching, and updating.
- **`newRequest`:** A custom utility module (likely using Axios or Fetch) for making API calls.
- **Tailwind CSS:**  Provides utility classes for styling.

## Functionality

1. **Data Fetching:** Uses `useQuery` from `react-query` to asynchronously fetch announcement data from the server via the `newRequest.get(`/student/${userId}/announcements`)` call.  The `userId` is retrieved from `localStorage`.  The API response is expected to be a JSON object containing an `announcements` array and a `count` property.

2. **State Management:**  `useState` hooks manage:
    - `searchTerm`:  The user's search query.
    - `filterType`:  The type of announcements to display ("all", "course", "admin").
    - `importanceFilter`: The importance level to filter by ("all", "Critical", "High", "Medium", "Low").

3. **Filtering:**  The `filteredAnnouncements` array is derived from the fetched `data.announcements` array.  It applies filtering based on `searchTerm`, `filterType`, and `importanceFilter` using JavaScript's `filter()` method.  This filtering happens client-side.

4. **Error Handling:** The component gracefully handles loading and error states using the `isLoading` and `error` properties provided by `useQuery`.  Appropriate UI elements are displayed in each case.

5. **UI Rendering:** The component renders:
    - A header with the title "All Announcements".
    - A filter section with input fields for search and dropdown menus for type and importance.
    - A summary section displaying total announcement count, course announcement count, and admin announcement count.
    - An announcement list, displaying each announcement with its title, content, date, author, type, importance level, and attachments (if any).  Date formatting and importance styling are handled by helper functions.

6. **Helper Functions:**
    - `formatDate`: Converts a date string into a user-friendly format.
    - `getImportanceClass`: Returns a Tailwind CSS class based on the announcement's importance level for colored badges.
    - `getImportanceLabel`: Returns a descriptive label for the announcement's importance level.


## Code Explanation with Examples

**1. Data Fetching with `useQuery`:**

```javascript
const { isLoading, error, data } = useQuery({
  queryKey: ["allAnnouncements"],
  queryFn: () => newRequest.get(`/student/${userId}/announcements`).then((res) => res.data),
});
```

This fetches data, handles loading, and caches the result.  `queryKey` ensures unique caching. `queryFn` performs the API call.

**2. Filtering `filteredAnnouncements`:**

```javascript
const filteredAnnouncements = data?.announcements?.filter(announcement => {
  const matchesSearch = announcement.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                        announcement.content.toLowerCase().includes(searchTerm.toLowerCase());
  const matchesType = filterType === "all" || announcement.type === filterType;
  const matchesImportance = importanceFilter === "all" || announcement.importance === importanceFilter;
  return matchesSearch && matchesType && matchesImportance;
}) || [];
```

This filters the announcements array based on the search term and selected filters. The `|| []` handles cases where `data.announcements` is null or undefined.

**3. Date Formatting:**

```javascript
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};
```

This function formats the date for better readability.

**4. Importance Styling:**

```javascript
const getImportanceClass = (importance) => {
  switch (importance) {
    case 'Critical': return 'bg-red-500';
    case 'High': return 'bg-orange-500';
    case 'Medium': return 'bg-blue-500';
    case 'Low': return 'bg-green-500';
    default: return 'bg-blue-500';
  }
};
```

This function maps importance levels to Tailwind CSS classes for colored badges.

**5.  Rendering an Announcement:**

```jsx
{filteredAnnouncements.map((announcement) => (
  <div key={announcement.id} className="bg-white rounded-lg shadow-md p-4">
    <div className={`${getImportanceClass(announcement.importance)} text-white font-bold px-2 py-1 rounded`}>
      {getImportanceLabel(announcement.importance)}
    </div>
    <h3>{announcement.title}</h3>
    <p>{announcement.content}</p>
    <p>Posted by: {announcement.postedBy} on {formatDate(announcement.date)}</p>
    {/* ... render attachments ... */}
  </div>
))}
```

This shows how an individual announcement is rendered using the helper functions and Tailwind CSS classes.


## Assumptions

- The `newRequest` module is correctly configured to interact with the backend API.
- The API endpoint `/student/{userId}/announcements` returns a JSON object with the expected structure.
- The `currentUser` object is reliably stored in `localStorage`.
- Announcement objects have the necessary properties (`title`, `content`, `date`, `type`, `importance`, `postedBy`, `attachments`).


## Potential Improvements

- **Server-side filtering:**  Performing filtering on the server would be more efficient for large datasets.
- **Pagination:** Implementing pagination would improve performance for very long lists of announcements.
- **Error handling:** More robust error handling could provide more specific feedback to the user.
- **Accessibility:** Adding ARIA attributes would improve accessibility for screen readers.
- **Testing:**  Adding unit and integration tests would improve code quality and maintainability.


