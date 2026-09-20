import os
import secrets
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db
from models.schemas import Application, BankDetails, Partner, Director, UploadedDocument, AdminUser

# Initialize Flask app
app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "kgs_portal.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

# Initialize database
db.init_app(app)

# ========================
# HELPER FUNCTIONS
# ========================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_application_id():
    """Generate unique application ID like KGS20260001."""
    timestamp = datetime.now().strftime('%y')
    # Get the next application number from database
    last_app = Application.query.order_by(Application.id.desc()).first()
    next_num = (last_app.id + 1) if last_app else 1
    return f'KGS{timestamp}{next_num:04d}'


def save_uploaded_file(file, doc_type, app_id):
    """Save uploaded file with unique name and return file info."""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Create unique filename
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f'{app_id}_{doc_type}_{secrets.token_hex(4)}.{file_ext}'
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    return {
        'filename': unique_filename,
        'original_filename': secure_filename(file.filename),
        'file_path': file_path,
        'file_size': os.path.getsize(file_path),
        'file_type': file_ext
    }


def login_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ========================
# CLIENT ROUTES
# ========================

@app.route('/')
def index():
    """Home page - Service selection."""
    return render_template('index.html')


@app.route('/udyam')
def udyam_form():
    """Udyam registration form."""
    return render_template('udyam.html')


@app.route('/gst')
def gst_home():
    """GST service - Business type selection."""
    return render_template('gst_selection.html')


@app.route('/gst/proprietorship')
def gst_proprietorship():
    """GST Proprietorship form."""
    return render_template('gst_proprietorship.html')


@app.route('/gst/partnership')
def gst_partnership():
    """GST Partnership form."""
    return render_template('gst_partnership.html')


@app.route('/gst/llp')
def gst_llp():
    """GST LLP form."""
    return render_template('gst_llp.html')


@app.route('/gst/private-limited')
def gst_private_limited():
    """GST Private Limited Company form."""
    return render_template('gst_private_limited.html')


@app.route('/api/submit-udyam', methods=['POST'])
def submit_udyam():
    """Handle Udyam registration submission."""
    try:
        # Get form data
        data = request.form
        
        # Create new application
        app_id = generate_application_id()
        
        application = Application(
            application_id=app_id,
            service_type='udyam',
            full_name=data.get('fullName'),
            mobile_number=data.get('mobileNumber'),
            email=data.get('email'),
            business_name=data.get('businessName'),
            business_address=data.get('businessAddress'),
            nature_of_business=data.get('natureOfBusiness'),
            aadhaar_number=data.get('aadhaarNumber'),
            pan_number=data.get('panNumber'),
            status='pending'
        )
        
        db.session.add(application)
        db.session.flush()  # Get the ID
        
        # Save bank details
        bank = BankDetails(
            application_id=application.id,
            account_holder_name=data.get('accountHolderName'),
            bank_name=data.get('bankName'),
            account_number=data.get('accountNumber'),
            ifsc=data.get('ifsc')
        )
        db.session.add(bank)
        
        # Handle file uploads
        required_docs = ['aadhaar', 'pan', 'photo', 'signature', 'cheque']
        uploaded_count = 0
        
        for doc_type in required_docs:
            file = request.files.get(doc_type)
            if file:
                file_info = save_uploaded_file(file, doc_type, app_id)
                if file_info:
                    doc = UploadedDocument(
                        application_id=application.id,
                        document_type=doc_type,
                        file_name=file_info['filename'],
                        original_file_name=file_info['original_filename'],
                        file_path=file_info['file_path'],
                        file_size=file_info['file_size'],
                        file_type=file_info['file_type']
                    )
                    db.session.add(doc)
                    uploaded_count += 1
        
        if uploaded_count < len(required_docs):
            return jsonify({'success': False, 'message': 'All required documents must be uploaded'}), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'application_id': app_id,
            'message': 'Application submitted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/submit-gst', methods=['POST'])
def submit_gst():
    """Handle GST registration submission."""
    try:
        data = request.form
        business_type = data.get('businessType')
        
        app_id = generate_application_id()
        
        application = Application(
            application_id=app_id,
            service_type='gst',
            gst_business_type=business_type,
            full_name=data.get('fullName'),
            mobile_number=data.get('mobileNumber'),
            email=data.get('email'),
            aadhaar_number=data.get('aadhaarNumber'),
            pan_number=data.get('panNumber'),
            status='pending'
        )
        
        if business_type == 'proprietorship':
            application.business_name = data.get('businessName')
            application.business_address = data.get('businessAddress')
            application.nature_of_business = data.get('natureOfBusiness')
        
        elif business_type == 'partnership':
            application.firm_name = data.get('firmName')
            application.firm_pan = data.get('firmPan')
            application.business_address = data.get('businessAddress')
            application.nature_of_business = data.get('natureOfBusiness')
        
        elif business_type == 'llp':
            application.llp_name = data.get('llpName')
            application.llpin = data.get('llpin')
            application.llp_pan = data.get('llpPan')
            application.business_address = data.get('businessAddress')
        
        elif business_type == 'private_limited':
            application.company_name = data.get('companyName')
            application.cin = data.get('cin')
            application.company_pan = data.get('companyPan')
            application.business_address = data.get('businessAddress')
            application.nature_of_business = data.get('natureOfBusiness')
        
        db.session.add(application)
        db.session.flush()
        
        # Save bank details
        bank = BankDetails(
            application_id=application.id,
            account_holder_name=data.get('accountHolderName'),
            bank_name=data.get('bankName'),
            account_number=data.get('accountNumber'),
            ifsc=data.get('ifsc')
        )
        db.session.add(bank)
        
        # Handle partner details for partnership/LLP
        if business_type in ['partnership', 'llp']:
            partner_count = int(data.get('partnerCount', 0))
            for i in range(partner_count):
                partner = Partner(
                    application_id=application.id,
                    name=data.get(f'partner_{i}_name'),
                    mobile=data.get(f'partner_{i}_mobile'),
                    aadhaar=data.get(f'partner_{i}_aadhaar'),
                    pan=data.get(f'partner_{i}_pan')
                )
                db.session.add(partner)
        
        # Handle director details for private limited
        if business_type == 'private_limited':
            director_count = int(data.get('directorCount', 0))
            for i in range(director_count):
                director = Director(
                    application_id=application.id,
                    name=data.get(f'director_{i}_name'),
                    mobile=data.get(f'director_{i}_mobile'),
                    aadhaar=data.get(f'director_{i}_aadhaar'),
                    pan=data.get(f'director_{i}_pan')
                )
                db.session.add(director)
        
        # Handle file uploads
        for file_key in request.files:
            file = request.files.get(file_key)
            if file and file.filename:
                file_info = save_uploaded_file(file, file_key, app_id)
                if file_info:
                    doc = UploadedDocument(
                        application_id=application.id,
                        document_type=file_key,
                        file_name=file_info['filename'],
                        original_file_name=file_info['original_filename'],
                        file_path=file_info['file_path'],
                        file_size=file_info['file_size'],
                        file_type=file_info['file_type']
                    )
                    db.session.add(doc)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'application_id': app_id,
            'message': 'Application submitted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/success/<application_id>')
def success(application_id):
    """Success page after submission."""
    app_record = Application.query.filter_by(application_id=application_id).first()
    if not app_record:
        return redirect(url_for('index'))
    
    return render_template('success.html', application_id=application_id)


# ========================
# ADMIN ROUTES
# ========================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password) and admin.is_active:
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials'), 401
    
    return render_template('admin_login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    """Logout admin."""
    session.clear()
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard with statistics."""
    total_apps = Application.query.count()
    udyam_apps = Application.query.filter_by(service_type='udyam').count()
    gst_apps = Application.query.filter_by(service_type='gst').count()
    
    pending = Application.query.filter_by(status='pending').count()
    under_process = Application.query.filter_by(status='under_process').count()
    completed = Application.query.filter_by(status='completed').count()
    
    stats = {
        'total': total_apps,
        'udyam': udyam_apps,
        'gst': gst_apps,
        'pending': pending,
        'under_process': under_process,
        'completed': completed
    }
    
    return render_template('admin_dashboard.html', stats=stats)


@app.route('/admin/applications')
@login_required
def admin_applications():
    """List all applications with search and filter."""
    page = request.args.get('page', 1, type=int)
    service_filter = request.args.get('service', '')
    status_filter = request.args.get('status', '')
    search_query = request.args.get('search', '')
    
    query = Application.query
    
    if service_filter:
        query = query.filter_by(service_type=service_filter)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search_query:
        query = query.filter(
            (Application.application_id.ilike(f'%{search_query}%')) |
            (Application.full_name.ilike(f'%{search_query}%')) |
            (Application.mobile_number.ilike(f'%{search_query}%')) |
            (Application.pan_number.ilike(f'%{search_query}%')) |
            (Application.aadhaar_number.ilike(f'%{search_query}%'))
        )
    
    query = query.order_by(Application.created_at.desc())
    applications = query.paginate(page=page, per_page=10)
    
    return render_template('admin_applications.html', applications=applications)


@app.route('/admin/application/<application_id>')
@login_required
def admin_application_detail(application_id):
    """View single application details."""
    app_record = Application.query.filter_by(application_id=application_id).first_or_404()
    
    return render_template('admin_application_detail.html', application=app_record)


@app.route('/api/admin/update-status', methods=['POST'])
@login_required
def update_application_status():
    """Update application status."""
    try:
        data = request.json
        application_id = data.get('application_id')
        new_status = data.get('status')
        
        app_record = Application.query.filter_by(application_id=application_id).first_or_404()
        app_record.status = new_status
        app_record.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/download-document/<int:doc_id>')
@login_required
def download_document(doc_id):
    """Download a specific document."""
    doc = UploadedDocument.query.get_or_404(doc_id)
    
    try:
        return send_file(
            doc.file_path,
            as_attachment=True,
            download_name=doc.original_file_name
        )
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ========================
# INITIALIZATION
# ========================

def create_default_admin():
    """Create default admin user if not exists."""
    admin = AdminUser.query.filter_by(username='admin').first()
    
    if not admin:
        admin = AdminUser(
            username='admin',
            password_hash=generate_password_hash('admin@123'),
            email='admin@kgscompany.com',
            full_name='KGS Admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: username='admin', password='admin@123'")


@app.before_request
def before_request():
    """Ensure upload folder exists."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500


# ========================
# MAIN
# ========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
        print("Database initialized and admin user created.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
