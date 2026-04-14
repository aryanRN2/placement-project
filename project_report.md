# App Dev Project Report

## 1. Student Details
**Name:** Aryan Maurya
**Roll Number:** BS22XXXX (Please update with your exact roll number)
**Email:** aryannsv@gmail.com
**About Me:** I am a student at the IIT Madras BS Degree program with a strong interest in web application development. I enjoy building practical, functional applications that solve real-world problems.

## 2. Project Details
**Project Title:** Campus Placement Management System

**Problem Statement:**
To design and build a web-based application that streamlines the campus placement process, enabling companies to post job drives, students to build profiles and apply for positions, and administrators to oversee and manage the entire workflow efficiently.

**Approach:**
The app is built using Flask as the backend framework with a modular structure. It implements secure Role-Based Access Control (RBAC) with three distinct roles: Admin, Company, and Student. It uses SQLite and Flask-SQLAlchemy for database management, and Jinja2 templates for the frontend interface.

## 3. AI/LLM Declaration
I utilized AI tools like Gemini to assist in drafting initial boilerplate code, troubleshooting syntax errors, and generating sections of my project documentation. The AI served primarily as a learning and debugging assistant to refine my implementation logic.

## 4. Technologies and Frameworks
- **Backend:** Python, Flask, Werkzeug
- **Database:** SQLite, Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Frontend:** HTML, CSS, Jinja2 Templates

## 5. Database Schema / ER Diagram
The application uses five main interconnected tables:
- **Users:** `id`, `username`, `password_hash`, `role` (admin/company/student), `status` (pending/approved/blacklisted)
- **Company Profiles:** `id`, `user_id` (FK), `company_name`, `hr_contact`, `website`
- **Student Profiles:** `id`, `user_id` (FK), `name`, `contact`, `resume_path`
- **Drives:** `id`, `company_id` (FK), `job_title`, `job_description`, `eligibility_criteria`, `application_deadline`, `status`
- **Applications:** `id`, `student_id` (FK), `drive_id` (FK), `application_date`, `status`

*Relationships:*
- A User can have one associated Profile (either Company or Student).
- A Company can create multiple Drives (One-to-Many).
- A Drive can receive multiple Applications (One-to-Many).
- A Student can submit multiple Applications (One-to-Many).

## 6. API Resource Endpoints
- `GET/POST /login` - User authentication.
- `GET/POST /register_student` - Student registration and profile creation.
- `GET/POST /register_company` - Company registration and profile creation.
- `GET /logout` - User logout.
- `GET /admin/dashboard` - Admin dashboard to view stats, manage users, and search.
- `GET /admin/user_status/<id>/<action>` - Admin actions to approve/blacklist/reject users.
- `GET /admin/drive_status/<id>/<action>` - Admin actions to approve/reject drives.
- `GET /company/dashboard` - Company dashboard showing upcoming and closed drives.
- `GET/POST /company/create_drive` - Create a new placement drive.
- `GET /company/view_applications/<drive_id>` - View student applications for a specific drive.
- `POST /company/update_application/<app_id>` - Update the status of a student application.
- `GET /student/dashboard` - Student dashboard showing approved drives and application status.
- `POST /student/apply/<drive_id>` - Apply to an available placement drive.
- `GET /student/history` - View a history of applied drives.
- `GET/POST /student/profile` - Manage student profile and upload resume.

## 7. Architecture and Features
**Architecture Overview:**
The application follows the Model-View-Controller (MVC) pattern adapted for Flask. The architecture relies on Flask routes (Controllers) to handle requests, Flask-SQLAlchemy (Models) to manage data and relationships within a SQLite DB, and Jinja2 (Views) to dynamically render the HTML pages presented to the user.

**Implemented Features:**
- **Role-Based Routing:** Seamless and secure redirection based on user roles (Admin, Company, Student).
- **Admin Control Panel:** Admins can moderate new company registrations and placement drives to ensure quality control.
- **Company Tools:** Companies can manage job offerings and smoothly update candidate application statuses (Applied, Shortlisted, Selected, Rejected, Waiting).
- **Student Portal:** Students can build their profiles, directly upload their resumes, and track their application progress.
- **Comprehensive Search:** Admin dashboard features integrated search functionality to easily find students and companies.

## 8. Video Presentation
[Insert the link to your demo video here]
