# FeePayment Component

## Overview
The `FeePayment` component is a React-based front-end module designed for handling academic fee payments at IIT Guwahati. It integrates with the Razorpay payment gateway, displays student details, fee breakdowns, and payment statuses, and allows users to download fee receipts as PDFs. The component is styled using Tailwind CSS and follows a modular, responsive design.

## Dependencies
- **React**: For building the UI and managing state.
- **Razorpay**: For processing payments via the checkout.js script.
- **Axios**: For making HTTP requests to the backend.
- **@react-pdf/renderer**: For generating PDF receipts.
- **Tailwind CSS**: For styling the component.

## Component Structure
The component is structured into several sections:
1. **Student Identification**: Displays student details (name, roll number, programme, semester, and photo).
2. **Fee Overview**: Summarizes the fee status (total, paid, due) with a payment action button.
3. **Fee Breakdown**: Lists detailed fee particulars with amounts.
4. **Payment Confirmation**: Shows payment history and allows downloading receipts (visible post-payment).

## Code Explanation

### Imports
```jsx
import React, { useState, useEffect } from "react";
import { pdf } from "@react-pdf/renderer";
import FeeReceiptPDF from "../components/documentSection/FeeReceiptPDF";
import axios from 'axios';
```
- Imports React hooks for state and lifecycle management.
- Imports `pdf` for generating PDF documents.
- Imports a custom `FeeReceiptPDF` component for receipt generation.
- Imports `axios` for API calls to the backend.

### Helper Function: `loadRazorpayScript`
```jsx
const loadRazorpayScript = (src) => {
    return new Promise((resolve) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = () => resolve(true);
        script.onerror = () => resolve(false);
        document.body.appendChild(script);
    });
};
const RAZORPAY_SCRIPT_URL = 'https://checkout.razorpay.com/v1/checkout.js';
```
- Dynamically loads the Razorpay checkout.js script.
- Returns a Promise resolving to `true` on successful load, `false` on failure.
- Appends the script to the document body.

### State Management
```jsx
const [isPaid, setIsPaid] = useState(false);
const [paymentDetails, setPaymentDetails] = useState(null);
const [isLoading, setIsLoading] = useState(true);
const [isDownloading, setIsDownloading] = useState(false);
```
- `isPaid`: Tracks payment status (true if paid).
- `paymentDetails`: Stores transaction details (e.g., transaction ID, amount).
- `isLoading`: Manages loading state during API calls or payment processing.
- `isDownloading`: Prevents multiple PDF downloads by tracking download state.

### Static Data
```jsx
const student = { ... }; // Student details
const feeParticularsData = [ ... ]; // Fee breakdown items
const calculatedTotal = feeParticularsData.reduce(...);
const adjustmentAmount = 0.00;
const payableAmount = (calculatedTotal - adjustmentAmount) * 0 + 2; // DEV ONLY
const feeDataForPDF = [ ... ];
const feeSummary = { ... };
```
- `student`: Hardcoded student data (e.g., name, roll number).
- `feeParticularsData`: Array of fee items (e.g., Tuition Fees, Hostel Rent).
- `calculatedTotal`: Sums all fee amounts.
- `adjustmentAmount`: Any fee adjustments (set to 0).
- `payableAmount`: Net amount to pay (set to 2 INR for testing).
- `feeDataForPDF`: Data for PDF generation, including totals and adjustments.
- `feeSummary`: Summary for the fee overview table (semester, fee type, status).

### Effect Hook: `useEffect`
```jsx
useEffect(() => {
    const fetchFeeStatus = async () => {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulated delay
        const alreadyPaid = false; // Simulated initial state
        setIsPaid(alreadyPaid);
        if (alreadyPaid) {
            setPaymentDetails({ ... }); // Mock paid details
        } else {
            setPaymentDetails(null);
        }
        setIsLoading(false);
    };
    fetchFeeStatus();
}, []);
```
- Runs on component mount to fetch initial payment status.
- Simulates an API call with an 800ms delay.
- Sets `isPaid` and `paymentDetails` based on the simulated response.

### Payment Handler: `handlePayFee`
```jsx
const handlePayFee = async () => {
    setIsLoading(true);
    const scriptLoaded = await loadRazorpayScript(RAZORPAY_SCRIPT_URL);
    if (!scriptLoaded) {
        alert('Failed to load payment gateway...');
        setIsLoading(false);
        return;
    }
    try {
        const { data } = await axios.post('http://localhost:8000/api/payment/create-order', { amount: payableAmount, currency: 'INR' });
        const { orderId, currency, amount: amountInPaise } = data;
        const options = { ... }; // Razorpay options
        const rzp = new window.Razorpay(options);
        rzp.on('payment.failed', (response) => { ... });
        rzp.open();
    } catch (error) {
        alert(`Payment failed: ${error.message || 'Unknown error'}`);
        setIsLoading(false);
    }
};
```
- Loads Razorpay script and initiates payment.
- Sends a POST request to create a payment order.
- Configures Razorpay options (e.g., key, amount, prefill data).
- Opens the Razorpay checkout modal.
- Handles success (`handler`) and failure (`payment.failed`) events.
- Updates state on successful payment.

### PDF Download Handler: `handleDownloadReceipt`
```jsx
const handleDownloadReceipt = async () => {
    if (!isPaid || !paymentDetails || isDownloading) return;
    setIsDownloading(true);
    try {
        const blob = await pdf(<FeeReceiptPDF ... />).toBlob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `Fee_Receipt_${student.rollNumber}_Sem${student.currentSemester}.pdf`;
        link.click();
        URL.revokeObjectURL(url);
    } catch (error) {
        alert("Failed to generate PDF receipt...");
    } finally {
        setIsDownloading(false);
    }
};
```
- Generates a PDF receipt using `FeeReceiptPDF`.
- Converts the PDF to a blob and creates a downloadable link.
- Triggers download and cleans up the URL.
- Prevents multiple downloads with `isDownloading`.

### Formatting: `formatCurrency`
```jsx
const formatCurrency = (amount) => {
    const numericAmount = Number(amount);
    if (isNaN(numericAmount)) {
        return '₹ --.--';
    }
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', ... }).format(numericAmount);
};
```
- Formats numbers as INR currency (e.g., ₹ 1,00,000.00).
- Handles invalid amounts by returning a placeholder.

### Rendering
The component renders conditionally:
- **Loading State**: Displays a loading message if `isLoading` is true and no data is available.
- **Main UI**: Renders student details, fee overview, breakdown, and payment history (if paid).
- Uses Tailwind CSS for responsive, modern styling (e.g., shadows, gradients, hover effects).
- Tables use consistent styling with hover effects and conditional formatting (e.g., red for due amounts).

## Styling with Tailwind CSS
- **Container**: `max-w-[1000px] mx-auto my-10 px-10 py-[35px] bg-white rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.08)]`.
- **Buttons**: Gradient backgrounds (e.g., `bg-gradient-to-r from-blue-500 to-blue-700`), hover effects, and disabled states.
- **Tables**: Responsive with `overflow-x-auto`, alternating row colors (`even:bg-gray-50`), and hover effects (`hover:bg-blue-50`).
- **Badges**: Color-coded status indicators (e.g., green for paid, red for due).

## Environment Variables
- `REACT_APP_RAZORPAY_KEY_ID`: Razorpay API key for payment processing.
- Must be set in the `.env` file for the payment gateway to work.

## Notes
- The payable amount is hardcoded to 2 INR for testing (`payableAmount = 2`).
- The backend URL (`http://localhost:8000/api/payment/create-order`) assumes a local server.
- The `FeeReceiptPDF` component is not included but is assumed to accept `student`, `semester`, `feeData`, `isPaid`, and `transactionDetails` props.
- Error handling is implemented for payment failures, script loading, and PDF generation.

## Future Improvements
- Replace hardcoded student and fee data with API calls.
- Add backend verification for payment signatures.
- Implement a loading spinner for better UX.
- Support multiple payment methods or currencies.
- Add accessibility attributes (e.g., ARIA labels).