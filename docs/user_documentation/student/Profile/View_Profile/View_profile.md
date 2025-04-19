# View Profile Module

## 1. Overview

This page allows students to view their personal, academic, and hostel-related details. It provides a comprehensive snapshot of the student’s profile, including completed courses, contact information, and programme details. The information is displayed in a read-only format and is fetched from the institute's centralized database.

---

## 2. Page Layout

When you navigate to the **View Profile** page, the following key sections are visible:

- **Profile Photo:** Displayed in a circular frame at the top-left of the profile card.
- **Student Information Card:** Contains detailed fields such as:
  - **Full Name**
  - **Roll Number**
  - **Semester**
  - **Email Address**
  - **Contact Number**
  - **Branch and Programme**
  - **Hostel and Room Number**
  - **Blood Group** and **Date of Birth**
  - **Year of Joining**
  - **Signature Image**

- **Completed Courses Table:** Located below the profile card, listing all completed courses with the following columns:
  - **Course Code**
  - **Course Name**
  - **Department**
  - **Credit/Audit**
  - **Semester**
  - **Credits**
  - **Grade**

---

## 3. Features and How to Use Them

### 3.1 Viewing Profile

Upon navigating to the **Profile → View Profile** section from the sidebar, the profile data is automatically fetched and rendered. The profile section displays:

- **Personal Details:** Name, Roll Number, Email, Contact Number, DOB, Blood Group.
- **Academic Details:** Branch, Programme, Semester, Year of Joining.
- **Hostel Details:** Hostel name and Room number.
- **Authentication Visuals:** Profile picture and uploaded signature image.

> **Note:** All fields are non-editable and displayed for informational purposes only.

---

### 3.2 Viewing Completed Courses

The **Completed Courses** table provides a summary of academic progress in prior semesters.

Each row includes:

- **Course Code:** Unique identifier of the course (e.g., CS777).
- **Course Name:** Name of the completed course (e.g., Computation3).
- **Department:** Offering department (e.g., Computer Science and Engineering).
- **Credit/Audit Status:** Whether the course was taken for credit or audit.
- **Semester:** Semester in which the course was completed.
- **Credits:** Number of credits for the course.
- **Grade:** Final grade awarded (e.g., CC).

---

## 4. Behavior and Validation

- **Read-Only Access:** No fields on the profile page are editable by the user.
- **Data Fetching:** All profile data is dynamically loaded from the server upon accessing the page.
- **Error Handling:** If there's an issue retrieving profile information, an error message may be displayed.

---

## 5. Important Notes

- **Data Accuracy:** If any of the profile information is incorrect or outdated, contact the academic office or administration.
- **Security:** Ensure that your contact and personal details are not shared with unauthorized individuals.
- **Signature and Photo:** Used for official identification and documentation purposes within the institute.
- **Grade Verification:** For transcript and grade-related queries, refer to the academic section or student records portal.

---
