# Meal Plan Models

## Overview

This document describes the Mongoose data models used in the meal management system, focusing on two key models: `MealPlanRequest` and `MealSubscription`. These models track user meal plan change requests and active meal subscriptions.

## Models

### MealPlanRequest Model

The `MealPlanRequest` model stores requests by users to change their meal plans.

#### Schema Definition

```javascript
const mealPlanRequestSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  rollNo: { type: String, required: true },
  currentPlan: { type: String, enum: ['None', 'Basic', 'Premium', 'Unlimited'], required: true },
  newPlan: { type: String, enum: ['None', 'Basic', 'Premium', 'Unlimited'], required: true },
  status: { type: String, enum: ['Pending', 'Approved', 'Rejected'], default: 'Pending', required: true, index: true },
  rejectionReason: { type: String, trim: true },
  processedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  processedAt: { type: Date }
}, { timestamps: true });
```

#### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| userId | ObjectId | Yes | - | References the User who made the request |
| rollNo | String | Yes | - | Roll number of the student |
| currentPlan | String | Yes | - | The user’s current meal plan |
| newPlan | String | Yes | - | The meal plan the user wants to switch to |
| status | String | Yes | "Pending" | Status of the request |
| rejectionReason | String | No | - | Reason for rejection if status is "Rejected" |
| processedBy | ObjectId | No | - | Admin/staff who processed the request |
| processedAt | Date | No | - | Timestamp when the request was processed |
| createdAt | Date | Auto | - | Automatically generated timestamp |
| updatedAt | Date | Auto | - | Automatically updated timestamp |

### MealSubscription Model

The `MealSubscription` model stores current and historical subscription data for a user.

#### Schema Definition

```javascript
const mealSubscriptionSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, unique: true },
  rollNo: { type: String, required: true, unique: true },
  subscriptionId: { type: String, unique: true, sparse: true },
  currentPlan: { type: String, enum: ['None', 'Basic', 'Premium', 'Unlimited'], required: true, default: 'None' },
  startDate: { type: Date },
  endDate: { type: Date },
  isActive: { type: Boolean, default: false, required: true }
}, { timestamps: true });
```

#### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| userId | ObjectId | Yes | - | References the User who has the subscription |
| rollNo | String | Yes | - | Roll number of the student |
| subscriptionId | String | No | - | Optional identifier for the subscription |
| currentPlan | String | Yes | "None" | The user's active meal plan |
| startDate | Date | No | - | Start date of the subscription |
| endDate | Date | No | - | End date of the subscription |
| isActive | Boolean | Yes | false | Whether the subscription is currently active |
| createdAt | Date | Auto | - | Automatically generated timestamp |
| updatedAt | Date | Auto | - | Automatically updated timestamp |

## Relationships

- **User (One-to-One)**: Each subscription and request is associated with one user
- **Admin (Many-to-One)**: `processedBy` in MealPlanRequest references an admin User who reviewed the request

## Usage

- `MealPlanRequest` helps track change requests and their status.
- `MealSubscription` helps determine a user’s current meal plan and its validity.

## Indexing and Performance

- `userId` and `status` fields in `MealPlanRequest` are indexed for quick lookups.
- `userId` and `rollNo` in `MealSubscription` are marked as `unique` to avoid duplicate subscriptions.
