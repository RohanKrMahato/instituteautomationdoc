# Subscription API Services Module

## Overview

This module provides a collection of API service functions for managing student meal plan subscription requests. It handles the creation of new subscription requests, processing existing requests, and retrieving a list of all subscription requests. The module implements error handling and uses axios for HTTP requests.

---

## Dependencies

- **axios**: Library for making HTTP requests

---

## Module Structure

### Configuration

- **API_URL**: Base URL for all API endpoints
- **axios.defaults**: Global axios configuration settings

### Exported Functions

- **createSubscriptionRequest**: Creates a new meal plan subscription request
- **processSubscriptionRequest**: Updates the status of an existing request
- **getSubscriptionRequests**: Retrieves all subscription requests

---

## Functionality

### Request Creation

- **Endpoint**: `POST /api/subscription-request`
- **Parameters**: studentId, newPlan
- **Returns**: Response data from the server
- **Error Handling**: Throws server response data or generic error message

### Request Processing

- **Endpoint**: `PUT /api/process-request`
- **Parameters**: requestId, status, rejectionReason (optional)
- **Returns**: Response data from the server
- **Error Handling**: Throws server response data or generic error message

### Request Retrieval

- **Endpoint**: `GET /api/subscription-requests`
- **Parameters**: None
- **Returns**: Array of subscription request objects
- **Error Handling**: Throws server response data or generic error message

---

## API Endpoints

### POST /api/subscription-request

Creates a new meal plan subscription request.

**Request Body**:
```javascript
{
  "studentId": "12345678",
  "newPlan": "Premium (19 meals/week)"
}
```

**Success Response**: Returns data from server response

**Error Response**: Returns error from server or generic error message

### PUT /api/process-request

Updates the status of an existing subscription request.

**Request Body**:
```javascript
{
  "requestId": "request123",
  "status": "approved", // or "rejected"
  "rejectionReason": "Optional reason for rejection"
}
```

**Success Response**: Returns data from server response

**Error Response**: Returns error from server or generic error message

### GET /api/subscription-requests

Retrieves all subscription requests.

**Request Parameters**: None

**Success Response**: Returns array of subscription request objects

**Error Response**: Returns error from server or generic error message

---

## Global Configuration

```javascript
axios.defaults.baseURL = process.env.REACT_APP_API_URL || '/api';
axios.defaults.headers.common['Content-Type'] = 'application/json';
```

- Sets the base URL from environment variable or fallback
- Sets default content type header for all requests

---

## Implementation Details

- **Promise-based**: All functions return promises for async/await compatibility
- **Error Extraction**: Attempts to extract response data from errors before falling back to generic messages
- **Optional Parameters**: Support for optional parameters like rejectionReason
- **Environment Variable**: Uses environment variable for API URL with fallback

---

## Best Practices Demonstrated

- **Separation of Concerns**: API logic separated from UI components
- **Error Handling**: Consistent error handling pattern across functions
- **Promise Architecture**: Clean async/await compatible functions
- **Environment Configuration**: Flexible configuration through environment variables
- **Content Type Standardization**: Consistent headers for API requests

---

## Usage

```javascript
import { 
  createSubscriptionRequest, 
  processSubscriptionRequest, 
  getSubscriptionRequests 
} from './path/to/api-services';

// Create a new subscription request
try {
  const result = await createSubscriptionRequest('12345678', 'Premium (19 meals/week)');
  console.log('Request created:', result);
} catch (error) {
  console.error('Error creating request:', error);
}

// Process a subscription request
try {
  const result = await processSubscriptionRequest('request123', 'approved');
  console.log('Request processed:', result);
} catch (error) {
  console.error('Error processing request:', error);
}

// Get all subscription requests
try {
  const requests = await getSubscriptionRequests();
  console.log('All requests:', requests);
} catch (error) {
  console.error('Error fetching requests:', error);
}
```

---

## Enhancement Possibilities

- Add request cancellation support using axios cancel tokens
- Implement request caching for frequently accessed data
- Add pagination support for large request lists
- Include request filtering and sorting functionality
- Add authentication token handling
- Implement request throttling or rate limiting
- Add request timeouts and retry logic
- Include detailed request logging for debugging