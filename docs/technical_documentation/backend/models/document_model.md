# Student Documents Models

## Overview

This document provides technical details for various Mongoose models that manage student-related documents within the system. These include both application-based and viewable document types.

## Models

### ApplicationDocument Model

The `ApplicationDocument` model handles documents that require administrative approval, such as Bonafide and Passport applications.

#### Schema Definition

```javascript
const applicationDocumentSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'Student', required: true },
  documentType: { type: String, enum: ['Bonafide', 'Passport'], required: true },
  status: { type: String, enum: ['Pending', 'Approved', 'Rejected'], default: 'Pending' },
  certificateNumber: { type: String },
  approvalDetails: {
    approvedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    approvalDate: { type: Date },
    remarks: [{ type: String }]
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});
```

#### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| studentId | ObjectId | Yes | - | References the student submitting the application |
| documentType | String | Yes | - | Type of application ('Bonafide' or 'Passport') |
| status | String | No | 'Pending' | Status of the application |
| certificateNumber | String | No | - | Optional certificate number issued after approval |
| approvalDetails.approvedBy | ObjectId | No | - | References the user who approved the application |
| approvalDetails.approvalDate | Date | No | - | Date when the document was approved |
| approvalDetails.remarks | [String] | No | [] | Comments or feedback regarding approval/rejection |
| createdAt | Date | No | Date.now | Timestamp of creation |
| updatedAt | Date | No | Date.now | Timestamp of last update |

#### Relationships

- **Student (Many-to-One)**: Each document belongs to a student
- **User (Many-to-One)**: Approval is done by an admin user

### Bonafide Model

Details for Bonafide certificate applications, linked to `ApplicationDocument`.

#### Schema Definition

```javascript
const bonafideSchema = new mongoose.Schema({
  applicationId: { type: mongoose.Schema.Types.ObjectId, ref: 'ApplicationDocument', required: true },
  currentSemester: { type: Number, required: true },
  purpose: { type: String, required: true, enum: ['Bank Account Opening', 'Passport Application', 'Visa Application', 'Education Loan', 'Scholarship Application', 'Other'] },
  otherReason: { type: String, required: function() { return this.purpose === 'Other'; } },
  otherDetails: { type: String }
});
```

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| applicationId | ObjectId | Yes | Reference to `ApplicationDocument` |
| currentSemester | Number | Yes | Current semester of the student |
| purpose | String | Yes | Reason for bonafide application |
| otherReason | String | Conditional | Required if purpose is 'Other' |
| otherDetails | String | No | Additional explanation if needed |

### Passport Model

Represents Passport-related applications under the `ApplicationDocument` model.

#### Schema Definition

```javascript
const passportSchema = new mongoose.Schema({
  applicationId: { type: mongoose.Schema.Types.ObjectId, ref: 'ApplicationDocument', required: true },
  applicationType: { type: String, enum: ['fresh', 'renewal'], required: true },
  placeOfBirth: { type: String, required: true },
  semester: { type: Number, required: true },
  mode: { type: String, enum: ['normal', 'tatkal'], required: true },
  tatkalReason: { type: String, required: function() { return this.mode === 'tatkal'; } },
  travelPlans: { type: String, enum: ['yes', 'no'], required: true },
  travelDetails: { type: String, required: function() { return this.travelPlans === 'yes'; } },
  fromDate: { type: Date, required: function() { return this.travelPlans === 'yes'; } },
  toDate: { type: Date, required: function() { return this.travelPlans === 'yes'; } }
});
```

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| applicationId | ObjectId | Yes | Reference to `ApplicationDocument` |
| applicationType | String | Yes | 'fresh' or 'renewal' |
| placeOfBirth | String | Yes | Place of birth of student |
| semester | Number | Yes | Current semester |
| mode | String | Yes | Application mode ('normal' or 'tatkal') |
| tatkalReason | String | Conditional | Required if mode is 'tatkal' |
| travelPlans | String | Yes | 'yes' or 'no' for planned travel |
| travelDetails | String | Conditional | Required if travelPlans is 'yes' |
| fromDate | Date | Conditional | Required if travelPlans is 'yes' |
| toDate | Date | Conditional | Required if travelPlans is 'yes' |

### ViewableDocument Model

Represents documents directly accessible by students without needing approval, such as ID cards and fee details.

#### Schema Definition

```javascript
const viewableDocumentSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'Student', required: true },
  documentType: { type: String, enum: ['ID Card', 'Fee Details'], required: true },
  metadata: {
    generatedDate: { type: Date, default: Date.now },
    validUntil: { type: Date }
  }
});
```

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| studentId | ObjectId | Yes | Reference to student |
| documentType | String | Yes | Type of document ('ID Card', 'Fee Details') |
| metadata.generatedDate | Date | No | Date of document creation |
| metadata.validUntil | Date | No | Validity end date of document |

### IDCard Model

Represents a student's identity card linked to a `ViewableDocument` entry.

#### Schema Definition

```javascript
const idCardSchema = new mongoose.Schema({
  viewableDocumentId: { type: mongoose.Schema.Types.ObjectId, ref: 'ViewableDocument', required: true },
  cardNumber: { type: String, required: true, unique: true },
  validFrom: { type: Date, required: true },
  validUntil: { type: Date, required: true }
});
```

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| viewableDocumentId | ObjectId | Yes | Reference to associated `ViewableDocument` |
| cardNumber | String | Yes | Unique identity card number |
| validFrom | Date | Yes | Card validity start date |
| validUntil | Date | Yes | Card validity end date |

## Model Registration

```javascript
export const ApplicationDocument = mongoose.model('ApplicationDocument', applicationDocumentSchema);
export const Bonafide = mongoose.model('Bonafide', bonafideSchema);
export const ViewableDocument = mongoose.model('ViewableDocument', viewableDocumentSchema);
export const IDCard = mongoose.model('IDCard', idCardSchema);
export const Passport = mongoose.model('Passport', passportSchema);
```

These models are registered with Mongoose for use throughout the application.

## Notes

### Indexing Suggestions
- `studentId`: used frequently for filtering student documents
- `documentType`: used for categorizing document lists
- `status`: in application documents for administrative workflows

### Validation
- Conditional validations for dynamic fields ensure data consistency
- Enum values restrict inputs to valid options

### Performance
- Consider indexing fields used in queries for faster lookups
- Use population (`populate`) to resolve references when necessary

