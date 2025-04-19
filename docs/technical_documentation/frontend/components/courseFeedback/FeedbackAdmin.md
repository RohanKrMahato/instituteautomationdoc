# FeedbackAdmin Component 

## Overview
The FeedbackAdmin component allows platform administrators to globally enable or disable the feedback collection system for all courses. It fetches the current feedback status from the server and provides a toggle button to change the state.
It features:
- Server-controlled toggle for feedback system
- Real-time UI updates with user feedback
- Styled, responsive layout using Tailwind CSS

## Dependencies
1. **React**: for component state and lifecycle management
2. **newRequest**: an Axios-like instance used for API calls.
3. **Tailwind CSS**: used for UI styling and responsiveness

## Event Handlers
1. handleToggle: Toggles the global feedback status by making a POST request to the server.

```jsx
const handleToggle = async () => {
  try {
    setSaving(true);
    setError('');
    const res = await newRequest.post('/feedback/admin/set', { active: !isActive });
    setIsActive(res.data.isActive);
  } catch (err) {
    setError(err.response?.data?.message || 'Could not update feedback status.');
  } finally {
    setSaving(false);
  }
};
```
- Uses optimistic UI approach with immediate visual feedback
- Handles API errors gracefully
- Updates local state based on server response

## Data Fetching

```jsx
useEffect(() => {
  const fetchStatus = async () => {
    try {
      setLoading(true);
      const res = await newRequest.get('/feedback/admin/status');
      setIsActive(res.data.isActive);
    } catch (err) {
      setError(err.response?.data?.message || 'Could not load feedback status.');
    } finally {
      setLoading(false);
    }
  };
  fetchStatus();
}, []);
```
- Runs once on mount
- Retrieves the global status of the feedback system (true or false)
- Error message is shown if fetch fails

## UI Structure
The component layout is clean and admin-friendly:

1. Main Container:
```jsx
<div className="max-w-xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-16 mb-8">
```
- Centered card layout
- Max width controlled (max-w-xl)
- Shadow and padding add visual hierarchy

2. Status and Toggle Area:
```jsx
<div className="flex flex-col md:flex-row md:items-center md:justify-between bg-pink-50 rounded-lg p-6 mb-6">
```
- Responsive flex layout
- Displays current status and toggle button side by side on larger screens

3. Toggle Button
```jsx
<button
  className={isActive ? "bg-red-500 ..." : "bg-green-500 ..."}
  onClick={handleToggle}
  disabled={saving}
>
  {saving ? "Deactivating..." : "Deactivate Feedback"}
</button>
```
- Red indicates deactivation; green indicates activation
- Button is disabled during API operation to prevent multiple calls
- Dynamically changes label based on state

## Loading and Error States

1. Loading Spinner: Shown while fetching the feedback status.
```jsx
if (loading) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
      <span className="ml-4 text-gray-600 text-lg">Loading status...</span>
    </div>
  );
}
```

2. Error Display: Renders a red alert box when API calls fail, handles both fetch and toggle errors.
```jsx
{error && (
  <div className="bg-red-100 text-red-700 px-4 py-2 rounded mb-4">
    {error}
  </div>
)}
```


## Scope of Improvement

Area	                Suggestion
Optimistic UI	        Temporarily show status as toggled while waiting for API response
Success Notification	Add toast/snackbar for successful toggle confirmation
Retry Strategy	        Implement automatic retry using React Query or exponential backoff on failure
Audit Logging	        Optionally log admin toggle actions for security/compliance

## Usage
1. Route Setup:
Ensure the route is protected and part of the admin panel:

```jsx
<Route path="/admin/feedback/control" element={<FeedbackAdmin />} />
```

2. Access Control:
This component must be restricted to admin users only, ideally using a PrivateRoute or role-based guard.

3. Navigation:
Trigger via an admin dashboard button or menu:

```jsx
navigate('/admin/feedback/control')
```