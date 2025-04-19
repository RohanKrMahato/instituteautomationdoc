# Fee Models 

This document provides a detailed description of the `FeeBreakdown` and `FeeDetails` schemas used in the application to manage fee structures and individual student fee records.

---

## FeeBreakdown Model

### Schema Definition

```ts
import mongoose from "mongoose";

const feeBreakdownSchema = new mongoose.Schema({
  semesterParity: { type: Number, required: true },
  program: {
    type: String,
    enum: ["BTech", "MTech", "PhD", "BDes", "MDes"],
    required: true,
  },
  isActive: { type: Boolean, default: false },
  tuitionFees: { type: Number, required: true },
  examinationFees: { type: Number, required: true },
  registrationFee: { type: Number, required: true },
  gymkhanaFee: { type: Number, required: true },
  medicalFee: { type: Number, required: true },
  hostelFund: { type: Number, required: true },
  hostelRent: { type: Number, required: true },
  elecAndWater: { type: Number, required: true },
  messAdvance: { type: Number, required: true },
  studentsBrotherhoodFund: { type: Number, required: true },
  acadFacilitiesFee: { type: Number, required: true },
  hostelMaintenance: { type: Number, required: true },
  studentsTravelAssistance: { type: Number, required: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

feeBreakdownSchema.index({ program: 1, semesterParity: 1 }, { unique: true });
```

### Fields

| Field                      | Type      | Required | Default     | Description                                          |
|---------------------------|-----------|----------|-------------|------------------------------------------------------|
| `semesterParity`          | `Number`  | Yes      | -           | Indicates whether it's an odd/even semester          |
| `program`                 | `String`  | Yes      | -           | Academic program (BTech, MTech, etc.)                |
| `isActive`                | `Boolean` | No       | `false`     | Indicates if this breakdown is currently active      |
| `tuitionFees` to `studentsTravelAssistance` | `Number` | Yes | - | Various fee components                               |
| `createdAt` / `updatedAt` | `Date`    | No       | `Date.now`  | Timestamps                                            |

### Indexing
- Composite index on `program` and `semesterParity` to ensure uniqueness and optimize queries.

---

## FeeDetails Model

### Schema Definition

```ts
const feeDetailsSchema = new mongoose.Schema({
  rollNo: { type: String, required: true, ref: "Student" },
  semester: { type: Number, required: true },
  isPaid: { type: Boolean, default: false },
  feeBreakdownData: {
    tuitionFees: { type: Number, required: true },
    examinationFees: { type: Number, required: true },
    registrationFee: { type: Number, required: true },
    gymkhanaFee: { type: Number, required: true },
    medicalFee: { type: Number, required: true },
    hostelFund: { type: Number, required: true },
    hostelRent: { type: Number, required: true },
    elecAndWater: { type: Number, required: true },
    messAdvance: { type: Number, required: true },
    studentsBrotherhoodFund: { type: Number, required: true },
    acadFacilitiesFee: { type: Number, required: true },
    hostelMaintenance: { type: Number, required: true },
    studentsTravelAssistance: { type: Number, required: true },
    program: { type: String, required: true },
    semesterParity: { type: Number, required: true },
    totalAmount: { type: Number, required: true },
  },
  academicYear: { type: String, required: true },
  viewableDocumentId: { type: mongoose.Schema.Types.ObjectId, required: true },
  transactionId: { type: String },
  paymentDetails: {
    razorpayOrderId: String,
    razorpayPaymentId: String,
    razorpaySignature: String,
    amount: Number,
    currency: String,
  },
  paidAt: { type: Date },
}, { timestamps: true });
```

### Fields

| Field                  | Type                         | Required | Description                                     |
|------------------------|------------------------------|----------|-------------------------------------------------|
| `rollNo`               | `String` (ref: `Student`)    | Yes      | Roll number of the student                      |
| `semester`            | `Number`                     | Yes      | Semester number                                 |
| `isPaid`              | `Boolean`                    | No       | Indicates whether the fee is paid               |
| `feeBreakdownData`    | `Object`                     | Yes      | Embedded breakdown of all fees and total amount |
| `academicYear`        | `String`                     | Yes      | Academic year for the fee record                |
| `viewableDocumentId`  | `ObjectId`                   | Yes      | ID of the document viewable to the student      |
| `transactionId`       | `String`                     | No       | Optional transaction reference                  |
| `paymentDetails`      | `Object`                     | No       | Razorpay payment details                        |
| `paidAt`              | `Date`                       | No       | Timestamp when the payment was made             |

### Relationships
- `rollNo` references the `Student` collection.
- `viewableDocumentId` can be used to show a downloadable receipt/invoice.

### Use Cases
- This schema helps store fee records of individual students per semester.
- Payment status and Razorpay details support online payment integration.
- Embeds a snapshot of fee breakdown for auditability and record traceability.

---

## Model Registration

```ts
const FeeBreakdown = mongoose.model("FeeBreakdown", feeBreakdownSchema);
const FeeDetails = mongoose.model("FeeDetails", feeDetailsSchema);
```

---
