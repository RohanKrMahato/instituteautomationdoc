# MongoDB Configuration

## Overview

The `mongoDb.js` file provides the configuration and utility required to establish a connection with a MongoDB database using the Mongoose ODM (Object Document Mapper). This setup enables the rest of the application to interact with the MongoDB database in a streamlined and schema-based manner.

## Dependencies

```javascript
import mongoose from 'mongoose';`
```

This line imports the **Mongoose** library, which is used to define schemas, models, and interact with MongoDB using JavaScript promises.

## Connection Method
### `connectDB`
An asynchronous function that establishes a connection to the MongoDB database.

```javascript

const connectDB = async () => {
  try {
    const conn = await mongoose.connect("mongodb+srv://divyansh:KrHRg7mgeh7tgNiU@cluster0.qhaz53w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0");
    console.log(`MongoDB Connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
  }
};
```

### **Explanation:**

**Input:**
-   No input parameters; it uses a hardcoded connection string (though typically this should come from environment variables).

**Process:**
1.  **`mongoose.connect(...)`** is used to initiate the connection to the MongoDB Atlas cluster using the provided connection URI.
2.  If the connection is successful, the host of the connected server is logged using `conn.connection.host`.
3.  If the connection fails, the error is caught and logged, and `process.exit(1)` is called to stop the application immediately, preventing further issues.

**Output:**
-   Returns the connection object if successful.
-   Terminates the application if the connection fails.

**Best Practice Note:**
-   The connection string is currently hardcoded and includes credentials. In production environments, this should be securely stored in environment variables (`process.env.MONGODB_URI`), as commented in the code.

## Error Handling Strategy
-   The `connectDB` function uses a `try-catch` block to handle any issues that occur while connecting to MongoDB.
-   Logs the error details to the console for debugging.
-   Calls `process.exit(1)` to safely terminate the Node.js process if the connection fails, avoiding unstable runtime behavior.

* * * * *

## Security Considerations
1.  **Credential Exposure:**
    -   Hardcoding sensitive credentials like database passwords in source files poses a security risk.
    -   It is strongly recommended to use environment variables instead (`process.env.MONGODB_URI`).

2.  **Failure Safety:**
    -   The application halts on database connection failure to prevent errors due to lack of DB access.