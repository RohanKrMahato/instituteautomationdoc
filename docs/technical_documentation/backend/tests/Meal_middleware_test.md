# Meal Middleware Test 

## Overview

The meal middleware test suite ensures robust validation and processing of meal-related requests in the application. Middleware functions are tested for correct handling of input, validation logic, and error responses. The suite uses mocked request and response objects to simulate Express.js middleware behavior and focuses on both successful and error scenarios for each function.


## Dependencies

- **Middleware Functions Tested**
  - `validateMealRequest`
  - `checkMealAvailability`
  - `authorizeMealAdmin`

- **Models Mocked**
  - `Meal`
  - `User`

- **Libraries and Tools**
  - `jest` for mocking and assertions


## validateMealRequest

**Input**
- Expects the incoming request (`req`) to have a `body` with:
  - `date`: Date string (required)
  - `mealType`: String (e.g., "breakfast", "lunch", "dinner"; required)
  - `items`: Array of meal items (required)

**Process**
- Checks if all required fields (`date`, `mealType`, `items`) are present in the request body.
- If any field is missing, responds with a 400 status and an error message.
- If all fields are present, calls `next()` to proceed to the next middleware or controller.

**Output**
- 400 Bad Request: If any required field is missing, returns `{ message: 'All fields are required' }`.
- Calls `next()` if all validations pass.


## checkMealAvailability

**Input**
- Expects the incoming request (`req`) to have a `body` with:
  - `date`: Date string (required)
  - `mealType`: String (required)

**Process**
- Uses the `Meal` model to check if a meal already exists for the given date and meal type.
- If a meal already exists, responds with a 409 status and an error message.
- If no meal exists, calls `next()` to proceed.

**Output**
- 409 Conflict: If a meal already exists for the given date and type, returns `{ message: 'Meal already exists for this date and type' }`.
- Calls `next()` if the meal is available for creation.


## authorizeMealAdmin

**Input**
- Expects the incoming request (`req`) to have a `user` object with:
  - `role`: String (should be "mealAdmin")

**Process**
- Checks if the user's role is "mealAdmin".
- If not, responds with a 403 status and an error message.
- If the user is authorized, calls `next()` to proceed.

**Output**
- 403 Forbidden: If the user is not a meal admin, returns `{ message: 'Access denied: Meal admin only' }`.
- Calls `next()` if the user is authorized.

