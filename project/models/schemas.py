from datetime import datetime
from models import db


class Application(db.Model):
    """Stores main application information for both Udyam and GST."""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    service_type = db.Column(db.String(20), nullable=False)  # 'udyam' or 'gst'
    gst_business_type = db.Column(db.String(50))  # 'proprietorship', 'partnership', 'llp', 'private_limited'
    
    # Personal Details
    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False, index=True)
    email = db.Column(db.String(100))
    
    # Business Details
    business_name = db.Column(db.String(100))
    business_address = db.Column(db.Text)
    nature_of_business = db.Column(db.String(200))
    
    # Identity Details
    aadhaar_number = db.Column(db.String(20), nullable=False, index=True)
    pan_number = db.Column(db.String(20), nullable=False, index=True)
    
    # GST Specific Fields
    firm_name = db.Column(db.String(100))
    firm_pan = db.Column(db.String(20))
    llp_name = db.Column(db.String(100))
    llpin = db.Column(db.String(20))
    llp_pan = db.Column(db.String(20))
    company_name = db.Column(db.String(100))
    cin = db.Column(db.String(30))
    company_pan = db.Column(db.String(20))
    
    # Status
    status = db.Column(db.String(50), default='pending')  # pending, documents_received, under_process, completed, rejected
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bank_details = db.relationship('BankDetails', backref='application', cascade='all, delete-orphan')
    partners = db.relationship('Partner', backref='application', cascade='all, delete-orphan')
    directors = db.relationship('Director', backref='application', cascade='all, delete-orphan')
    documents = db.relationship('UploadedDocument', backref='application', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Application {self.application_id}>'


class BankDetails(db.Model):
    """Stores bank information for applications."""
    __tablename__ = 'bank_details'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    
    account_holder_name = db.Column(db.String(100), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(30), nullable=False)
    ifsc = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BankDetails {self.account_number}>'


class Partner(db.Model):
    """Stores partner details for Partnership and LLP applications."""
    __tablename__ = 'partners'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    aadhaar = db.Column(db.String(20), nullable=False)
    pan = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Partner {self.name}>'


class Director(db.Model):
    """Stores director details for Private Limited Company applications."""
    __tablename__ = 'directors'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    aadhaar = db.Column(db.String(20), nullable=False)
    pan = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Director {self.name}>'


class UploadedDocument(db.Model):
    """Stores information about uploaded documents."""
    __tablename__ = 'uploaded_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    
    document_type = db.Column(db.String(50), nullable=False)  # e.g., 'aadhaar', 'pan', 'photo', etc.
    file_name = db.Column(db.String(255), nullable=False)
    original_file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    file_type = db.Column(db.String(10))  # 'pdf', 'jpg', 'png', etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UploadedDocument {self.document_type}>'


class AdminUser(db.Model):
    """Stores admin login credentials."""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdminUser {self.username}>'
