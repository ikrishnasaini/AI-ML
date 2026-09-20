# KGS & Company - Digital Client Portal

A production-quality web application for a Chartered Accountant firm providing secure document submission for CA services.

## 🚀 Features

### Client Portal
- **Udyam Registration** - Complete business registration with document upload
- **GST Registration** - Support for multiple business types:
  - Proprietorship
  - Partnership Firm
  - Limited Liability Partnership (LLP)
  - Private Limited Company

### Admin Panel
- Secure admin login
- Dashboard with statistics
- Application management with search and filters
- Document preview and download
- Status tracking and updates

### Security & Quality
- Secure file upload with validation
- Encrypted document storage
- Responsive design (Desktop, Tablet, Mobile)
- Professional CA firm branding
- 16MB file size limit
- Support for JPG, PNG, PDF formats

## 📋 Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend**: Python Flask
- **Database**: SQLite (easy migration to MySQL)
- **Authentication**: Admin login only (clients don't require login)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python app.py
```
The database will be created automatically on first run.

### Step 3: Run the Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

## 🔐 Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin@123`

**Important**: Change these credentials in production!

## 📁 Project Structure

```
kgs-portal/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── models/
│   ├── __init__.py
│   └── schemas.py              # Database models
│
├── routes/                     # (For future Blueprint organization)
│
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Home page
│   ├── udyam.html              # Udyam registration form
│   ├── gst_selection.html      # GST business type selection
│   ├── gst_proprietorship.html
│   ├── gst_partnership.html
│   ├── gst_llp.html
│   ├── gst_private_limited.html
│   ├── success.html            # Success page
│   ├── admin_login.html        # Admin login
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── admin_applications.html # Applications list
│   ├── admin_application_detail.html  # Application details
│   ├── 404.html                # Error page
│   └── 500.html                # Error page
│
├── static/
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   ├── js/
│   │   ├── main.js             # Utility functions
│   │   ├── form-handler.js     # Form validation & submission
│   │   └── file-upload.js      # File upload handling
│   └── images/                 # Images (if needed)
│
├── uploads/                    # Uploaded documents (auto-created)
│
└── database/                   # Database files (auto-created)
```

## 🎯 Usage Guide

### For Clients

1. **Visit Home Page**: Navigate to `http://localhost:5000/`
2. **Select Service**: Choose either Udyam or GST registration
3. **Fill Form**: Enter required personal and business details
4. **Upload Documents**: Drag & drop or click to upload required documents
5. **Submit**: Submit application and receive Application ID
6. **Confirmation**: Download or print confirmation

### For Admin

1. **Login**: Go to `http://localhost:5000/admin/login`
2. **View Dashboard**: See statistics and key metrics
3. **Manage Applications**: 
   - Search by Application ID, Name, Mobile, PAN, or Aadhaar
   - Filter by Service Type or Status
   - View complete application details
   - Download individual documents
   - Update application status

## 📝 Database Models

### Application
- Stores main application information
- Service type and business details
- Client contact information
- Application status tracking

### BankDetails
- Account holder information
- Bank and IFSC details

### Partner (for Partnership/LLP)
- Partner name, contact, and identity

### Director (for Private Limited)
- Director name, contact, and identity

### UploadedDocument
- Document metadata and file path
- Document type and file information

### AdminUser
- Admin authentication
- User management

## 🔒 Security Features

- Password hashing for admin login
- Secure file upload validation
- Unique filenames to prevent conflicts
- File size and type restrictions
- Session management
- CSRF protection ready (use in production)

## 🎨 Design Features

### Color Scheme
- **Navy Blue** (#1a3a52) - Professional
- **Gold** (#d4af37) - Premium accent
- **Light Gray** (#f5f5f5) - Clean backgrounds
- **White** - Clean layouts

### Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Smooth animations
- Touch-friendly interface
- Professional CA firm branding

## 📊 Database Initialization

The application automatically creates the database on first run. To reset:

1. Delete `kgs_portal.db` file
2. Delete the `migrations/` folder (if exists)
3. Run `python app.py` again

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Important Production Changes**:
1. Change `SECRET_KEY` in `app.py`
2. Set `debug=False`
3. Change admin credentials
4. Use environment variables for sensitive data
5. Use HTTPS/SSL certificate
6. Use MySQL instead of SQLite for better scalability

## 📬 Future Enhancements

- [ ] Email notifications
- [ ] WhatsApp integration
- [ ] SMS notifications
- [ ] Document preview/viewer
- [ ] Bulk download as ZIP
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] QR code generation for client links
- [ ] Payment integration
- [ ] Automated document verification

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### File Upload Issues
- Check upload folder permissions
- Ensure file size < 16MB
- Verify file format (JPG, PNG, PDF)

### Database Issues
- Delete `kgs_portal.db` and restart
- Check database folder permissions

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask/SQLAlchemy documentation
3. Check file permissions in `uploads/` directory

## 📄 License

This project is created for KGS & Company. All rights reserved.

## 👨‍💼 About KGS & Company

KGS & Company is a professional Chartered Accountant firm providing expert CA services and business registration assistance.

---

**Version**: 1.0.0  
**Last Updated**: 2026  
**Status**: Production Ready
