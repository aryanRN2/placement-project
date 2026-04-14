# Campus Placement Management System

This is a web-based Campus Placement Management System built with Flask, designed to streamline the recruitment process for students, companies, and administrators. 

## Features
- **Admin Role:** Manage users (approve/reject/blacklist), approve placement drives, and visualize overall statistics.
- **Company Role:** Create placement drives, manage applicants, and update application statuses.
- **Student Role:** Create a profile, upload resumes, and apply to available placement drives.

## Prerequisites
- Python 3.8+
- SQLite (comes pre-installed with Python)

## Installation and Setup Instructions

1. **Navigate to the Project Directory**
Ensure you are in the project folder:
```bash
cd "/Users/aryanmaurya/iitm mad1 project clone"
```

2. **(Optional but Recommended) Create a Virtual Environment**
Creating a virtual environment ensures dependencies do not conflict with your local system.
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
Install all the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

4. **Run the Application**
The application is configured to automatically initialize the database and create a default admin user the first time it is run. Start the Flask server with the following command:
```bash
python3 app.py
```

5. **Access the Application**
Open your web browser and navigate to:
http://127.0.0.co:5000/

## Built-in Accounts to Test
The application creates a default admin user on the first run.
- **Admin Username:** `admin`
- **Admin Password:** `admin`

For Company and Student accounts, please use the registration pages on the portal. (Note: New Company accounts require Admin approval before they can log in).
