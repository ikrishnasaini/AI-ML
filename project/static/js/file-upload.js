// ========================
// FILE UPLOAD HANDLER
// ========================

class FileUploadHandler {
    constructor() {
        this.uploadAreas = document.querySelectorAll('.upload-area');
        this.uploadedFiles = {};
        
        this.init();
    }

    init() {
        this.uploadAreas.forEach(area => {
            this.setupUploadArea(area);
        });
    }

    setupUploadArea(area) {
        const fileInput = area.querySelector('.file-input');
        const docType = area.getAttribute('data-doc-type');

        // Click to upload
        area.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag and drop
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.handleFileSelect(fileInput, docType);
            }
        });

        // File input change
        fileInput.addEventListener('change', () => {
            this.handleFileSelect(fileInput, docType);
        });

        // Remove file button
        const uploadedFileDiv = area.nextElementSibling;
        if (uploadedFileDiv) {
            const removeBtn = uploadedFileDiv.querySelector('.remove-file');
            if (removeBtn) {
                removeBtn.addEventListener('click', () => {
                    this.removeFile(fileInput, docType);
                });
            }
        }
    }

    handleFileSelect(fileInput, docType) {
        const file = fileInput.files[0];
        
        if (!file) return;

        // Validate file
        if (!this.validateFile(file)) {
            alert('Invalid file. Please check size and format.');
            fileInput.value = '';
            return;
        }

        // Store file info
        this.uploadedFiles[docType] = {
            file: file,
            name: file.name,
            size: file.size
        };

        // Update UI
        const uploadArea = fileInput.parentElement;
        const uploadedFileDiv = uploadArea.nextElementSibling;

        uploadArea.classList.add('d-none');
        uploadedFileDiv.classList.remove('d-none');

        const fileName = uploadedFileDiv.querySelector('.file-name');
        fileName.textContent = file.name;

        // Show file size
        const sizeText = this.formatFileSize(file.size);
        fileName.innerHTML += ` <small class="text-muted">(${sizeText})</small>`;
    }

    removeFile(fileInput, docType) {
        fileInput.value = '';
        delete this.uploadedFiles[docType];

        const uploadArea = fileInput.parentElement;
        const uploadedFileDiv = uploadArea.nextElementSibling;

        uploadArea.classList.remove('d-none');
        uploadedFileDiv.classList.add('d-none');
    }

    validateFile(file) {
        // Check file size (16MB max)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            return false;
        }

        // Check file type
        const allowedExtensions = ['jpg', 'jpeg', 'png', 'pdf'];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        return allowedExtensions.includes(fileExtension);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
}

// Initialize file upload handler when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new FileUploadHandler();
});
