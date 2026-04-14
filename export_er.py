import json
import base64
import urllib.request
import os

mermaid_code = """erDiagram
    users {
        int id PK
        string username
        string password_hash
        string role
        string status
    }
    company_profiles {
        int id PK
        int user_id FK
        string company_name
        string hr_contact
        string website
    }
    student_profiles {
        int id PK
        int user_id FK
        string name
        string contact
        string resume_path
    }
    drives {
        int id PK
        int company_id FK
        string job_title
        string job_description
        string eligibility_criteria
        date application_deadline
        string status
    }
    applications {
        int id PK
        int student_id FK
        int drive_id FK
        datetime application_date
        string status
    }
    
    users ||--o| company_profiles : "has"
    users ||--o| student_profiles : "has"
    users ||--o{ drives : "creates (if company)"
    users ||--o{ applications : "submits (if student)"
    drives ||--o{ applications : "receives"
"""

state = {
    "code": mermaid_code,
    "mermaid": {"theme": "default"}
}

json_str = json.dumps(state)
b64_str = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{b64_str}"

print(f"Fetching from {url[:50]}...")
# We must use a User-Agent, otherwise mermaid.ink might block default python agent
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        with open('er_diagram.png', 'wb') as out_file:
            out_file.write(response.read())
    print("Successfully exported er_diagram.png")
except Exception as e:
    print(f"Failed: {e}")
