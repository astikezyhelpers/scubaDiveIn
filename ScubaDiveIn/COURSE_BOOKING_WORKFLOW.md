# Course Booking Workflow

## Overview
The course booking workflow in ScubaDiveIn is a comprehensive process that allows users to browse, select, and book diving courses through an integrated payment system using Razorpay.

## Workflow Steps

### 1. Course Browsing
- Users can browse available courses through the `/courses` endpoint
- Courses are displayed with key information:
  - Course name and description
  - Price
  - Duration
  - Difficulty level
  - Maximum participants
  - Included items
  - Requirements

### 2. Course Details
- Users can view detailed course information at `/courses/<slug>`
- The course detail page shows:
  - Full course description
  - Course images
  - Pricing details
  - Requirements and prerequisites
  - Included items and equipment

### 3. Booking Initiation
- Users can initiate booking by clicking on the course's booking button
- The system redirects to `/payment/initiate/` with the selected course ID
- The initiate_payment view loads the payment form with course details

### 4. Payment Process
1. **Payment Creation**
   - User fills in required details:
     - Name
     - Email
     - Phone number
   - System creates a Razorpay order via `/payment/create/`
   - Order details are stored in the database

2. **Payment Processing**
   - Razorpay payment form is displayed
   - User completes payment through Razorpay's interface
   - Payment status is tracked in the `RazorpayPayment` model

3. **Payment Verification**
   - Razorpay sends a callback to `/payment/callback/`
   - System verifies payment signature
   - Updates payment status in database
   - Records customer details

### 5. Booking Confirmation
- On successful payment:
  - User is redirected to `/payment/success/`
  - Booking confirmation is displayed
  - Payment details are shown
  - Course details are included

## Data Models

### DivingService
- Stores course information
- Key fields:
  - Name and description
  - Price and duration
  - Difficulty level
  - Maximum participants
  - Requirements and included items

### RazorpayPayment
- Tracks payment information
- Key fields:
  - Order ID and Payment ID
  - Amount and currency
  - Payment status
  - Customer details
  - Booking date
  - Number of participants

## Security Features
- CSRF protection for payment forms
- Payment signature verification
- Secure storage of payment details
- Environment variable configuration for API keys

## Error Handling
- Payment failure handling
- Invalid payment verification
- Missing required fields
- Database transaction management

## Future Enhancements
- Email notifications for booking confirmation
- Booking management dashboard
- Cancellation and refund processing
- Multiple payment method support
- Booking calendar integration 