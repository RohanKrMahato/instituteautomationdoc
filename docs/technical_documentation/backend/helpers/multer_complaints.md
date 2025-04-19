# Upload Middleware

## Overview

This middleware configures file uploads for complaint-related images using `multer`. It handles image filtering, naming, and storage location. The uploaded files are saved to a designated directory with size and type restrictions.

## Dependencies

```javascript

import multer, { diskStorage } from 'multer';
import { join, extname } from 'path';
import { existsSync, mkdirSync } from 'fs';
```

## Configuration Details

### Upload Directory

**Path:**
-   Files are saved in `files_folder/complaints_upload/` relative to the project root.

**Creation Logic:**
-   If the directory does not exist, it is created recursively.

```javascript
const uploadDir = join(__dirname, '/../files_folder/complaints_upload/');
```

### Storage Engine

#### `diskStorage`

**destination:**
-   Dynamically checks and creates the upload directory before storing files.

**filename:**
-   Generates a unique filename using the current timestamp and original file name (with spaces replaced by underscores).

```javascript
filename: (req, file, cb) => {
  const timestamp = Date.now();
  const originalName = file.originalname.replace(/\s+/g, '_');
  cb(null, `${timestamp}_${originalName}`);
}
```

### File Filter

**Allowed Types:**
-   `image/jpeg`
-   `image/png`
-   `image/jpg`

**Validation:**
-   Rejects files that do not match allowed MIME types with an error message: `'Only image files are allowed!'`

### Upload Limits

**Size Limit:**

-   Files are limited to a maximum size of `2MB`.

```javascript
limits: {
  fileSize: 2 * 1024 * 1024 // 2MB
}
```

### Export

The configured `upload` middleware is exported as the default module:

```javascript
export default upload;
```

### Usage Example

```javascript
import upload from './middlewares/upload.js';

router.post('/upload', upload.single('image'), (req, res) => {
  res.send('File uploaded successfully');
});`