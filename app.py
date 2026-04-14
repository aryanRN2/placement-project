import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, CompanyProfile, StudentProfile, Drive, Application



app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
        new_admin = User(username='admin', password_hash=hashed_password, role='admin', status='approved')
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created (username 'admin', password 'admin')")

def create_admin2():
    admin = User.query.filter_by(username='admin2').first()
    if not admin:
        hashed_password = generate_password_hash('admin2', method='pbkdf2:sha256')
        new_admin = User(username='admin2', password_hash=hashed_password, role='admin', status='approved')
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created (username 'admin', password 'admin')")

with app.app_context():
    db.create_all()
    create_admin()
    create_admin2()

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            if user.status != 'approved':
                flash(f"Account is {user.status}. You cannot login.", "danger")
                return redirect(url_for('login'))
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('login.html')

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('register_student'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
       
        new_user = User(username=username, password_hash=hashed_password, role='student', status='approved')
        db.session.add(new_user)
        db.session.commit()
        





        new_profile = StudentProfile(user_id=new_user.id, name=name)
        db.session.add(new_profile)
        db.session.commit()
        
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for('login'))
        
    return render_template('register_student.html')

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('register_company'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        









        new_user = User(username=username, password_hash=hashed_password, role='company', status='pending')
        db.session.add(new_user)
        db.session.commit()
        
        new_profile = CompanyProfile(user_id=new_user.id, company_name=company_name)
        db.session.add(new_profile)
        db.session.commit()
        
        flash("Registration successful. Wait for Admin approval.", "info")
        return redirect(url_for('login'))
        
    return render_template('register_company.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('index'))
        
    search_query = request.args.get('search', '')
    


    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()
    
   
   
    if search_query:
        
        
        student_query = User.query.join(StudentProfile).filter(User.role == 'student', 
            (User.username.ilike(f'%{search_query}%')) | (StudentProfile.name.ilike(f'%{search_query}%')))
        students = student_query.all()
        
        
        company_query = User.query.join(CompanyProfile).filter(User.role == 'company',
            (User.username.ilike(f'%{search_query}%')) | (CompanyProfile.company_name.ilike(f'%{search_query}%')))
        companies = company_query.all()
    else:
        students = User.query.filter_by(role='student').all()
        companies = User.query.filter_by(role='company').all()

        
    pending_companies = User.query.filter_by(role='company', status='pending').all()
    pending_drives = Drive.query.filter_by(status='pending').all()
    approved_drives = Drive.query.filter_by(status='approved').all()
    
    return render_template('admin_dashboard.html', 
        total_students=total_students, total_companies=total_companies,
        total_drives=total_drives, total_applications=total_applications,
        students=students, companies=companies, 





        pending_companies=pending_companies, pending_drives=pending_drives,
        approved_drives=approved_drives, search_query=search_query)

@app.route('/admin/user_status/<int:user_id>/<action>')
@login_required






def admin_user_status(user_id, action):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    if action == 'approve':
        user.status = 'approved'
        flash(f"User {user.username} approved.", "success")
    elif action == 'blacklist':
        user.status = 'blacklisted'
        flash(f"User {user.username} blacklisted.", "warning")
    elif action == 'reject':
        db.session.delete(user) # Or change status to rejected
        flash(f"User {user.username} application rejected/deleted.", "danger")
        
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/drive_status/<int:drive_id>/<action>')
@login_required
def admin_drive_status(drive_id, action):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
        
    drive = Drive.query.get_or_404(drive_id)
    if action == 'approve':
        drive.status = 'approved'
        flash("Drive approved.", "success")
    elif action == 'reject' or action == 'close':
        drive.status = 'closed' if action == 'close' else 'rejected'
        flash(f"Drive marked as {drive.status}.", "warning")
        
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/company/dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        return redirect(url_for('index')) 
        
    drives = Drive.query.filter_by(company_id=current_user.id).all()
    upcoming_drives = [d for d in drives if d.status != 'closed']
    closed_drives = [d for d in drives if d.status == 'closed']
    
    return render_template('company_dashboard.html', upcoming_drives=upcoming_drives, closed_drives=closed_drives)


@app.route('/company/view_applications/<int:drive_id>')
@login_required
def view_applications(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('index'))
        
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('company_dashboard'))
        
    applications = Application.query.filter_by(drive_id=drive_id).all()
    return render_template('view_applications.html', drive=drive, applications=applications)

@app.route('/company/update_application/<int:app_id>', methods=['POST'])
@login_required
def update_application(app_id):
    if current_user.role != 'company':
        return redirect(url_for('index'))
        
    application = Application.query.get_or_404(app_id)
    if application.drive.company_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('company_dashboard'))
        
    new_status = request.form.get('status')
    if new_status in ['Applied', 'Shortlisted', 'Selected', 'Rejected', 'Waiting']:
        application.status = new_status
        db.session.commit()
        flash("Application status updated.", "success")
    
    return redirect(url_for('view_applications', drive_id=application.drive_id))

@app.route('/company/create_drive', methods=['GET', 'POST'])
@login_required
def create_drive():
    if current_user.role != 'company':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        eligibility = request.form.get('eligibility')
        deadline_str = request.form.get('deadline')
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for('create_drive'))
            
        new_drive = Drive(
            company_id=current_user.id,
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility,
            application_deadline=deadline,
            status='pending' # Needs admin approval
        )
        db.session.add(new_drive)
        db.session.commit()
        
        flash("Drive created successfully and is pending Admin approval.", "success")
        return redirect(url_for('company_dashboard'))
        
    return render_template('create_drive.html')
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
        
    approved_drives = Drive.query.filter_by(status='approved').all()
    
    
    applied_drive_ids = [app.drive_id for app in Application.query.filter_by(student_id=current_user.id).all()]
    
    return render_template('student_dashboard.html', drives=approved_drives, applied_drive_ids=applied_drive_ids)

@app.route('/student/apply/<int:drive_id>', methods=['POST'])
@login_required
def apply_drive(drive_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
        
    drive = Drive.query.get_or_404(drive_id)
    if drive.status != 'approved':
        flash("You can only apply to approved drives.", "danger")
        return redirect(url_for('student_dashboard'))
        
    existing_app = Application.query.filter_by(student_id=current_user.id, drive_id=drive.id).first()
    if existing_app:
        flash("You have already applied to this drive.", "warning")
    else:
        new_app = Application(student_id=current_user.id, drive_id=drive.id)
        db.session.add(new_app)
        db.session.commit()
        flash("Applied successfully!", "success")
        
    return redirect(url_for('student_dashboard'))

@app.route('/student/history')
@login_required
def student_history():
    if current_user.role != 'student':
        return redirect(url_for('index'))
        
    applications = Application.query.filter_by(student_id=current_user.id).all()
    return render_template('student_history.html', applications=applications)

@app.route('/student/profile', methods=['GET', 'POST'])
@login_required
def student_profile():
    if current_user.role != 'student':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        
        current_user.student_profile.name = name
        current_user.student_profile.contact = contact
        
  
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                filename = secure_filename(f"{current_user.username}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                current_user.student_profile.resume_path = file_path
                
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('student_profile'))
        
    return render_template('student_profile.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
