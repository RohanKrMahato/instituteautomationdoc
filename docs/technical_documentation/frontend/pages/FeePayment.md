# FeePayment Component

## Overview

The `FeePayment` component is a React functional component responsible for:
- Fetching and displaying student fee details.
- Facilitating online fee payments via Razorpay.
- Recording payment details in the backend.
- Generating and downloading fee receipts as PDFs.
- Handling various UI states (loading, error, success, etc.).

It uses modern React hooks, Tanstack Query for data fetching, and integrates with external libraries like `axios`, `react-hot-toast`, and `@react-pdf/renderer`.

---

## Dependencies

The component relies on the following libraries and utilities:
- **React**: For building the UI and managing state.
- **@tanstack/react-query**: For data fetching and mutation handling.
- **axios**: For making HTTP requests to the backend.
- **react-hot-toast**: For displaying toast notifications.
- **@react-pdf/renderer**: For generating PDF receipts.
- **react-router-dom**: For navigation.
- **Razorpay**: For payment processing via the Razorpay checkout script.

---

## Component Structure

The component is structured as follows:
1. **State Management**: Uses `useState` for local state and `useQuery`/`useMutation` for data fetching and mutations.
2. **Helper Functions**: Utility functions for loading scripts, formatting currency, and calculating academic years.
3. **UI Rendering**: Conditionally renders based on loading, error, or data states.
4. **Event Handlers**: Handles payment initiation and receipt downloading.

---

## Code Explanation

### 1. Imports and Setup

The component imports necessary dependencies and utilities.

```jsx
import React, { useState, useEffect } from "react";
import { pdf } from "@react-pdf/renderer";
import FeeReceiptPDF from "../components/documentSection/FeeReceiptPDF";
import axios from "axios";
import newRequest from "../utils/newRequest";
import { useQuerykon, useMutation } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import { useNavigate } from 'react-router-dom';
```

- `FeeReceiptPDF`: A custom component for rendering PDF receipts.
- `newRequest`: A custom axios instance with pre-configured base URL and headers.
- `useQuery` and `useMutation`: For fetching fee data and recording payments.
- `toast`: For user notifications.
- `useNavigate`: For programmatic navigation.

---

### 2. Helper Functions

#### `loadRazorpayScript`

Loads the Razorpay checkout script dynamically.

```jsx
const loadRazorpayScript = (src) => {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
```jsx
const RAZORPAY_SCRIPT_URL = "https://checkout.razorpay.com/v1/checkout.js";
```

- Creates a script element and appends it to the document body.
- Resolves a promise with `true` on successful load, `false` on error.

#### `getCurrentAcademicYear`

Calculates the current academic year based on the month.

```jsx
const getCurrentAcademicYear = () => {
  const today = new Date();
  const month = today.getMonth();
  const year = today.getFullYear();
  return month < 6 ? `${year - 1}-${year}` : `${year}-${year + 1}`;
};
```

- If the month is before July (month < 6), the academic year is `year-1` to `year`.
- Otherwise, it’s `year` to `year+1`.

---

### 3. State and Effects

#### User ID Extraction

Extracts the user ID from `localStorage` on component mount.

```jsx
const [userId, setUserId] = useState(null);

useEffect(() => {
  try {
    const { data: userData } = JSON.parse(localStorage.getItem("currentUser"));
    const { userId } = userData.user;
    setUserId(userId);
    console.log("User ID set:", userId);
  } catch (error) {
    console.error("Error parsing user data from localStorage:", error);
  }
}, []);
```

- Parses the `currentUser` item from `localStorage`.
- Sets the `userId` state for use in API calls.
- Logs errors if parsing fails.

#### Fee Data Fetching

Fetches student fee data using `useQuery`.

```jsx
const {
  data: feeData,
  isLoading,
  error,
  refetch,
} = useQuery({
  queryKey: ["studentFeeData", userId],
  queryFn: async () => {
    const response = await newRequest.get(`/student/${userId}/fees`);
    return response.data;
  },
  enabled: !!userId,
  retry: 1,
  onError: (error) => {
    console.error("Failed to fetch fee data:", error);
    if (error.response?.status !== 404) {
      toast.error("Failed to load fee details");
    }
  },
});
```

- `queryKey`: Ensures cache uniqueness based on `userId`.
- `queryFn`: Fetches fee data from the backend.
- `enabled`: Only runs if `userId` is available.
- `retry`: Limits retries to 1.
- `onError`: Shows a toast error unless the error is a 404 (fee structure not available).

---

### 4. Payment Processing

#### `recordPayment` Mutation

Records payment details in the backend.

```jsx
const recordPayment = useMutation({
  mutationFn: (paymentData) => {
    console.log("Sending payment data to backend:", paymentData);
    return newRequest.post(`/student/${userId}/fees/payment`, paymentData);
  },
  onSuccess: (response, paymentData) => {
    console.log("Payment record success response:", response.data);
    toast.success("Payment recorded successfully");
    navigate(`/documents/feereceipt?semester=${feeData.student.nextSemester}`);
  },
  onError: (error) => {
    console.error("Error recording payment:", error);
    toast.error(error.response?.data?.message || "Failed to record payment");
  },
});
```

- `mutationFn`: Sends payment data to the backend.
- `onSuccess`: Shows a success toast and navigates to the fee receipt page.
- `onError`: Shows an error toast with the backend message or a default message.

#### `handlePayFee`

Initiates the payment process with Razorpay.

```jsx
const handlePayFee = async () => {
  if (!feeData || feeData.feeStatus?.isPaid) {
    toast.error("Payment already completed or invalid fee data");
    return;
  }

  toast.loading("Initializing payment...", { id: "payment-init" });

  try {
    const scriptLoaded = await loadRazorpayScript(RAZORPAY_SCRIPT_URL);
    if (!scriptLoaded) {
      toast.error("Failed to load payment gateway...");
      return;
    }

    const backendUrl = "process.env.REACT_APP_API_URL/payment/create-order";
    const orderPayload = { amount: payableAmount, currency: "INR" };
    const { data } = await axios.post(backendUrl, orderPayload);

    const options = {
      key: process.env.REACT_APP_RAZORPAY_KEY_ID,
      amount: data.amount,
      currency: data.currency,
      name: "IIT Guwahati",
      description: `Fee Payment - ${feeSummary.semester}`,
      order_id: data.orderId,
      handler: function (response) {
        const paymentData = {
          semester: Number(feeData.student.nextSemester),
          feeBreakdownId: feeData.feeBreakdown._id,
          transactionId: response.razorpay_payment_id,
          academicYear: getCurrentAcademicYear(),
          paymentDetails: {
            razorpayOrderId: response.razorpay_order_id,
            razorpayPaymentId: response.razorpay_payment_id,
            razorpaySignature: response.razorpay_signature,
            amount: payableAmount,
            currency: data.currency,
          },
          isPaid: true,
          paidAt: new Date().toISOString(),
        };
        recordPayment.mutate(paymentData);
      },
      prefill: {
        name: feeData?.student?.name || "",
        email: feeData?.student?.email || "",
        contact: feeData?.student?.contact || "",
      },
      notes: {
        address: "IIT Guwahati, Assam, India",
        roll_number: feeData?.student?.rollNo || "",
        semester: feeSummary.semester,
      },
      theme: { color: "#007bff" },
      modal: {
        ondismiss: () => {
          toast.dismiss("payment-init");
        },
      },
    };

    if (window.Razorpay) {
      const rzp = new window.Razorpay(options);
      rzp.on("payment.failed", (response) => {
        toast.error(`Payment Failed: ${response.error.description || "Unknown error"}`);
      });
      rzp.open();
    } else {
      toast.error("Payment gateway failed to initialize.");
    }
  } catch (error) {
    toast.error(`Payment failed: ${error.message}`);
  }
};
```

- Checks if payment is already completed or fee data is invalid.
- Loads the Razorpay script.
- Creates a payment order via the backend.
- Configures Razorpay options, including:
  - Payment metadata (amount, currency, order ID).
  - Success handler to record payment.
  - Prefill data for student details.
  - Custom notes and theme.
- Opens the Razorpay checkout modal.
- Handles payment failure and errors with appropriate toasts.

---

### 5. Receipt Generation

#### `handleDownloadReceipt`

Generates and downloads a PDF receipt.

```jsx
const handleDownloadReceipt = async () => {
  if (!feeData?.feeStatus?.isPaid || isDownloading) return;
  setIsDownloading(true);
  toast.loading("Generating receipt...");

  try {
    const transactionDetails = paymentDetails || {
      slNo: 1,
      feeType: feeSummary.feeType,
      feeAmount: payableAmount,
      transactionId: "FEE" + feeData.feeStatus?.feeDetailsId?.substring(0, 10),
      dateTime: new Date().toLocaleString("sv-SE"),
      status: "Success",
    };

    const blob = await pdf(
      <FeeReceiptPDF
        student={feeData.student}
        semester={feeSummary.semester}
        feeData={feeDataForPDF}
        isPaid={true}
        transactionDetails={transactionDetails}
      />
    ).toBlob();

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `Fee_Receipt_${feeData.student.rollNo}_${feeSummary.semester}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild link);
    URL.revokeObjectURL(url);
    toast.success("Receipt downloaded successfully");
  } catch (error) {
    console.error("Error generating or downloading PDF receipt:", error);
    toast.error("Failed to generate PDF receipt");
  } finally {
    setIsDownloading(false);
  }
};
```

- Checks if payment is complete and no download is in progress.
- Prepares transaction details for the PDF.
- Uses `@react-pdf/renderer` to generate a PDF blob.
- Creates a downloadable link and triggers the download.
- Cleans up the URL and DOM.
- Shows success or error toasts.

---

### 6. UI Rendering

The component conditionally renders based on state:

#### No User ID

```jsx
if (!userId) {
  return (
    <div className="max-w-[1000px] mx-auto my-10 px-10 py-[35px] bg-white rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.08)] text-gray-800 text-center p-12">
      <h1 className="text-2xl font-semibold mb-4 text-gray-900">Fee Payment</h1>
      <div className="p-8 bg-yellow-50 rounded-lg border border-yellow-200">
        <p className="text-lg text-yellow-800">
          Unable to load user information. Please log in again.
        </p>
      </div>
    </div>
  );
}
```

- Displays an error if user data cannot be loaded.

#### Loading State

```jsx
if (isLoading) {
  return (
    <div className="max-w-[1000px] mx-auto my-10 px-10 py-[35px] bg-white rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.08)] text-gray-800 text-center p-12 text-lg text-gray-600">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
      <p>Loading Fee Details...</p>
    </div>
  );
}
```

- Shows a spinner and loading message.

#### No Fee Structure or Max Semester

```jsx
if ((error && error.response?.status === 404) || feeData?.isMaxSemesterReached) {
  return (
    <div className="max-w-[1000px] mx-auto my-10 px-10 py-[35px] bg-white rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.08)] text-gray-800 text-center p-12">
      <h1 className="text-2xl font-semibold mb-4 text-gray-900">Fee Payment</h1>
      <div className="p-8 bg-yellow-50 rounded-lg border border-yellow-200">
        <p className="text-lg text-yellow-800">
          {feeData?.isMaxSemesterReached
            ? feeData.message || "You have completed the maximum number of semesters..."
            : "Fee payment is not yet available for the next semester..."}
        </p>
      </div>
    </div>
  );
}
```

- Displays a warning if no fee structure is available or the student has completed their program.

#### Main Content

The main UI includes:
- **Student Details**: Displays student name, roll number, program, and semester.
- **Fee Overview**: A table summarizing semester, fee type, total fee, paid amount, due amount, status, and action (pay button).
- **Fee Breakdown**: A detailed table of fee particulars, total, adjustments, and net payable amount.
- **Payment Confirmation**: A success message and receipt view button if payment is complete.

Example of the fee overview table:

```jsx
<table className="w-full border-collapse">
  <thead>
    <tr>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800`}>Semester</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800`}>Fee Type</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800 text-right`}>Total Fee</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800 text-right`}>Fee Paid</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800 text-right`}>Amount Due</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800`}>Status</th>
      <th className={`${thBaseClasses} bg-blue-100 text-blue-800`}>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr className="transition-colors duration-250 ease even:bg-gray-50 hover:bg-blue-50">
      <td className={cellBaseClasses}>{feeSummary.semester}</td>
      <td className={cellBaseClasses}>{feeSummary.feeType}</td>
      <td className={`${cellBaseClasses} text-right font-medium tracking-tight`}>
        {formatCurrency(feeSummary.totalFee)}
      </td>
      <td className={`${cellBaseClasses} text-right font-medium tracking-tight`}>
        {formatCurrency(feeSummary.feePaid)}
      </td>
      <td className={`${cellBaseClasses} text-right font-medium tracking-tight ${
        !feeData.feeStatus?.isPaid ? "text-red-700 font-bold" : ""
      }`}>
        {formatCurrency(feeSummary.feeToBePaid)}
      </td>
      <td className={`${cellBaseClasses} text-center`}>
        <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider border ${
          feeData.feeStatus?.isPaid
            ? "text-green-800 bg-green-100 border-green-200"
            : "text-red-800 bg-red-100 border-red-200 font-bold"
        }`}>
          {feeSummary.remarks}
        </span>
      </td>
      <td className={`${cellBaseClasses} text-center`}>
        {!feeData.feeStatus?.isPaid ? (
          <button
            onClick={handlePayFee}
            className={`${buttonBaseClasses} bg-gradient-to-r from-blue-500 to-blue-700 text-white hover:from-blue-600 hover:to-blue-800`}
            disabled={recordPayment.isLoading}
          >
            {recordPayment.isLoading ? "Processing..." : "Proceed to Pay"}
          </button>
        ) : (
          <span className="text-green-700 font-bold">✓ Payment Complete</span>
        )}
      </td>
    </tr>
  </tbody>
</table>
```

- Uses Tailwind CSS for styling.
- Conditionally styles the status and action columns based on payment status.

---

### 7. Utility Functions

#### `formatCurrency`

Formats amounts as Indian Rupees.

```jsx
const formatCurrency = (amount) => {
  const numericAmount = Number(amount);
  if (isNaN(numericAmount)) {
    return "₹ --.--";
  }
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numericAmount);
};
```

- Converts the amount to a number.
- Returns a formatted string with the INR symbol and two decimal places.

---

## Styling

The component uses **Tailwind CSS** for styling, with custom classes for:
- Responsive layout (`max-w-[1000px] mx-auto`).
- Card-like containers (`bg-white rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.08)]`).
- Tables (`border-collapse`, `text-left`, `hover:bg-blue-50`).
- Buttons (`bg-gradient-to-r`, `hover:shadow-lg`).
- Status badges (`rounded-full`, `text-green-800 bg-green-100`).

---

## Error Handling

- **LocalStorage Errors**: Logs errors and displays a user-friendly message.
- **API Errors**: Handles 404s (no fee structure) separately; shows toasts for other errors.
- **Payment Errors**: Displays specific error messages from Razorpay or the backend.
- **PDF Generation Errors**: Shows a toast if PDF generation fails.

---

## Assumptions and Limitations

- Assumes a backend API at `/student/:userId/fees` and `/student/:userId/fees/payment`.
- Assumes environment variables (`REACT_APP_API_URL`, `REACT_APP_RAZORPAY_KEY_ID`) are set.
- Razorpay script must be accessible at the specified URL.
- Limited to INR currency for payments.
- No support for partial payments or refunds.
- PDF generation requires the `FeeReceiptPDF` component to be correctly implemented.

---

## Future Improvements

- Add support for multiple payment gateways.
- Implement retry logic for failed payments.
- Add a payment history section.
- Support partial payments or installment plans.
- Improve accessibility (ARIA labels, keyboard navigation).
- Add unit tests for helper functions and hooks.

---