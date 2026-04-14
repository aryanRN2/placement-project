# Campus Placement Management System - Detailed Project Report

## 1. Introduction and Objectives
The Campus Placement Management System is a comprehensive, web-based platform designed to bridge the gap between educational institutions, their students, and recruiting companies. The primary objective of this project is to digitize and streamline the conventional, manually intensive placement drives that take place in academic institutions. 

By centralizing the workflow, the application mitigates communication delays, prevents data silo issues, and ensures a transparent recruitment process. It provides personalized dashboards and specialized tools for three distinct user roles: **Administrators (Institution), Companies (Recruiters), and Students (Candidates)**.

## 2. Technology Stack and Architecture
The application is built using modern, lightweight web technologies to ensure swift performance and ease of deployment.

- **Backend Framework:** Python with Flask. Flask was chosen for its micro-framework flexibility, allowing for rapid development without unnecessary boilerplate.
- **Database:** SQLite managed via Flask-SQLAlchemy (an Object-Relational Mapper). This allows the application to interact with the database using Python objects instead of raw SQL, enhancing security against SQL injection and simplifying data manipulation.
- **Frontend Layer:** HTML5, CSS3, and Jinja2 templating engine. Jinja2 handles dynamic data rendering directly from the backend to the frontend, utilizing control structures like loops and conditionals to build the UI dynamically.
- **Authentication & Security:** Flask-Login manages user sessions and cookies securely. The `Werkzeug.security` module is used for cryptographic hashing (`pbkdf2:sha256`) of user passwords.

The system strictly follows the **Model-View-Controller (MVC) architectural pattern**:
- **Models (`models.py`):** Define the database tables, constraints, and relationships.
- **Views (`templates/`):** The Jinja2 templates that present the user interface and handle user inputs via forms.
- **Controllers (`app.py`):** The routing layer that accepts HTTP requests, processes business logic, queries the Models, and returns the appropriate Views.

---

## 3. Database Schema and ER Model
The system relies on a relational database design containing five primary interconnected tables:

1. **Users Table:** The central authentication table holding `id`, `username`, `password_hash`, `role` (admin/company/student), and account `status` (pending/approved/blacklisted).
2. **Company Profiles Table:** Contains detailed company metadata linked to the `Users` table via a Foreign Key. Stores the `company_name`, `hr_contact`, and `website`.
3. **Student Profiles Table:** Linked to the `Users` table, storing personal details like `name`, `contact`, and a `resume_path` (storing the server directory path to the user's uploaded PDF/document).
4. **Drives Table:** Created by Companies, this table holds recruiting event data: `job_title`, `job_description`, `eligibility_criteria`, `application_deadline`, and current `status`.
5. **Applications Table:** The junction table connecting Students to Drives. It tracks the `application_date` and the real-time `status` of their candidacy (Applied, Shortlisted, Selected, Rejected, Waiting).

---

## 4. In-Depth Feature Breakdown

### A. Core Authentication and Security (RBAC)
The core of the application heavily relies on Role-Based Access Control (RBAC).
- **Session Management:** Once logged in, `Flask-Login` tracks the user session. All standard routes are protected by the `@login_required` decorator, strictly prohibiting unauthenticated access.
- **Role Validation:** Inside every protected endpoint, the system explicitly checks `current_user.role`. If a Student attempts to access a Company dashboard via URL manipulation, the system intercepts the request, flashes an "Unauthorized access" warning, and redirects them to safety.
- **Password Cryptography:** Plain-text passwords are never stored. Upon registration, passwords are obfuscated using salted hashes, ensuring user data safety even if the database is theoretically compromised.

### B. Administrator Module
The Admin acts as the ultimate moderator of the platform to maintain quality and prevent spam. An Admin account is automatically seeded into the database on the system's first launch.
- **Global Dashboard:** Provides high-level statistical widget summaries (total students, total companies, active drives, total applications).
- **Account Moderation:** When a new Company registers, their account is flagged as `pending`. They cannot log in until the Admin reviews and upgrades their status to `approved`. Admins can also `blacklist` malicious or inactive accounts.
- **Drive Moderation:** Similarly, when a company posts a new placement drive, it is hidden from students until an Admin verifies the job details and marks the drive as `approved`.
- **Global Search Engine:** Admins have access to an integrated search bar allowing them to quickly query Usernames, Student Names, or Company Names using `ILIKE` pattern matching in SQLAlchemy.

### C. Company (Recruiter) Module
Companies utilize the platform to scout talent and manage their recruitment pipelines.
- **Registration & Verification:** Companies register with an HR contact and website. They must patiently wait for administrative verification before posting jobs.
- **Drive Creation:** Verified companies can initialize "Drives" (Job Postings). They submit detailed requirement schemas including a job title, exhaustive description, strict eligibility criteria, and a hard deadline date.
- **Application Tracking System (ATS):** 
    - Companies have a visually clean dashboard to separate "Upcoming Drives" from "Closed Drives".
    - Clicking a specific drive opens a Candidate Management panel.
    - Here, the company can view all students who applied. 
    - **Status Updates:** The company can dynamically update a student's application status from 'Applied' to 'Shortlisted', 'Waiting', 'Selected', or 'Rejected'. This instantly reflects on the student's personal portal.

### D. Student Module
The student portal is designed for ease-of-use, allowing candidates to highlight their skills and apply without friction.
- **Profile Management:** Students register and have access to update their profile configurations.
- **Resume Parsing & Uploading:** Utilizing `werkzeug.utils.secure_filename`, the system provides a safe gateway for students to upload their resumes to the filesystem (`static/uploads/`). The system securely formats the filename to prevent path traversal attacks and links the file path directly to the `StudentProfile` database record.
- **Drive Discovery:** The student dashboard dynamically renders all Administrative-approved job drives. Drives are presented in an easy-to-read card layout displaying eligibility requirements and deadlines.
- **One-Click Applications:** Applying to a drive is a frictionless, one-click process. The backend validates if the student has already applied to prevent duplicate database entries (`existing_app` check). Once successfully verified, a new record is created in the `Applications` table.
- **Application History:** A dedicated history page acts as the student's personal ledger, showing real-time feedback. Because the application uses an interconnected relational database, when a Company updates a student’s status to "Shortlisted", the student sees the update immediately upon refreshing their history panel.

---

## 5. Potential Future Enhancements
While the current system satisfies the foundational needs of a placement cell, future iterations could include:
- **Email Notifications:** Integrating `Flask-Mail` so students receive an automated email when their application status moves to "Selected" or "Shortlisted".
- **Advanced Resume Parsing:** Using NLP libraries to automatically extract skills from student resumes and rank them against the Drive's eligibility criteria.
- **Pagination & Analytics:** As the database scales with thousands of records, backend pagination for the Admin dashboard and dynamic visual pie-charts (using Chart.js) for application analytics would improve the UX.

## 6. Conclusion
The Campus Placement Management System effectively digitalizes an otherwise chaotic administrative process. By strictly utilizing the MVC paradigm natively adapted for Flask, the application achieves a clean separation of concerns. The usage of SQLAlchemy ensures robust relational data integrity, while the Jinja2 templates create a reactive surface for users. The system successfully restricts unauthorized actions via its rigid Role-Based Access Control, ensuring that companies, administrators, and students experience a secure, streamlined, and user-friendly recruitment journey.
