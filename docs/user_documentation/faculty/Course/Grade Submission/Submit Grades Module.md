# **Submit Grades Module

## **1\. Overview**

This page allows faculty members to submit grades for students enrolled in a specific course, in this case, identified as "CS101". It provides a table listing the enrolled students and an interface for entering their respective grades. Functionality for importing grades from a file is also available. The submitted grades are then stored in the institute's academic records system.

---

## **2\. Page Layout**

When a faculty member navigates to the "Submit Grades for Course CS101" page, the following key sections are typically visible:

* **Page Title:** Clearly indicates the purpose of the page and the specific course for which grades are being submitted (e.g., "Submit Grades for Course CS101").

* **Grade Submission Table:** A table listing the students enrolled in the course. The table includes the following columns:

  * **Roll Number:** The unique identification number for each student (e.g., 2201011039).  
  * **Name:** The name of the student.  
  * **Grade:** An input field (e.g., a text box or a dropdown menu) where the faculty member can enter the grade for the corresponding student.  
* **Import File Option:** A button or link that allows faculty to upload grades from an external file. The supported file format is usually specified (e.g., "Format: Roll Number, Grade").

* **Submission Button:** A prominent button, usually labeled "Submit Grades," which, when clicked, saves the entered grades to the system.

* **Instructional Message:** A message providing guidance or important information regarding grade submission (e.g., "\*All students must have grades assigned before submission").

---

## **3\. Features and How to Use Them**

### **3.1 Viewing Enrolled Students**

Upon accessing the "Submit Grades for Course CS101" page, a list of all students enrolled in the CS101 course is displayed in the Grade Submission table, along with their Roll Numbers and Names.

### **3.2 Entering Grades Manually**

To enter grades for individual students:

1. Locate the row corresponding to the student for whom you want to enter a grade.  
2. In the "Grade" column for that student, enter the appropriate grade using the provided input field. The system may have specific formatting or validation rules for the grades (e.g., letter grades, numerical values).  
3. Repeat this process for all students in the list.

### **3.3 Importing Grades from a File**

To upload grades from an external file:

1. Click the **Import File** button.  
2. A file selection dialog will appear, allowing you to browse and select the grade file from your computer. Ensure that the file is in the specified format (e.g., CSV with "Roll Number" and "Grade" columns).  
3. Once the file is uploaded, the system will process the data and populate the Grade Submission table with the grades from the file. Review the imported grades for accuracy.

### **3.4 Submitting Grades**

Once all grades have been entered or imported and reviewed:

1. Click the **Submit Grades** button.  
2. The system will save the entered grades to the database. A confirmation message may be displayed upon successful submission.

**Note:** Ensure that all students have been assigned a grade before submitting. The instructional message "\*All students must have grades assigned before submission" highlights this requirement.

---

## **4\. Behavior and Validation**

* **Student Data Retrieval:** The list of enrolled students is dynamically fetched from the system for the specific course (CS101).  
* **Grade Input Validation:** The system may have validation rules to ensure that the entered grades are in the correct format and within the acceptable range.  
* **Data Saving:** Clicking the "Submit Grades" button triggers the process of saving the grades to the institute's database, linking them to the respective students and the course.  
* **Potential Error Handling:** The system should provide feedback or error messages if there are issues with the submitted data (e.g., invalid grade format, missing grades).

---

## **5\. Important Notes**

* **Course Specificity:** This page is specific to the "CS101" course. Faculty will have similar pages for their other assigned courses, accessible from the "My Faculty Courses" page.  
* **Grade Accuracy:** Faculty are responsible for ensuring the accuracy of the grades submitted.  
* **Submission Deadlines:** Adhere to the institute's prescribed time for grade submission.  
* **Post-Submission Actions:** Once grades are submitted, there might be restrictions on further modifications. Refer to the institute's grade change policy if corrections are needed.  
* **File Format for Import:** Pay close attention to the specified file format for importing grades to avoid errors during the upload process.

