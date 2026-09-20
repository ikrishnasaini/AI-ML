// ========================
// FORM HANDLER CLASS
// ========================

class FormHandler {
    constructor(formId, submitUrl) {
        this.form = document.getElementById(formId);
        this.submitUrl = submitUrl;
        this.currentStep = 1;
        this.totalSteps = 5;
        
        this.init();
    }

    init() {
        if (!this.form) return;

        // Check if multi-step form exists
        const stepSections = this.form.querySelectorAll('.step-section');
        if (stepSections.length > 0) {
            this.totalSteps = stepSections.length;
            this.initMultiStep();
        }

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    initMultiStep() {
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (this.validateStep(this.currentStep)) {
                    this.nextStep();
                }
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.prevStep();
            });
        }

        this.updateStepUI();
    }

 validateStep(step) {
    const section = document.querySelector(`[data-step="${step}"]`);
    if (!section) return true;

    let isValid = true;

    const inputs = section.querySelectorAll("input, textarea, select");

    inputs.forEach(input => {

        // Hidden fields ko skip karo
        if (input.offsetParent === null) {
            return;
        }

        // File input validation
        if (input.type === "file") {
            if (input.hasAttribute("required") && input.files.length === 0) {
                input.classList.add("is-invalid");
                isValid = false;
            } else {
                input.classList.remove("is-invalid");
            }
            return;
        }

        // Required fields validation
        if (input.hasAttribute("required")) {

            if (!input.checkValidity()) {
                input.classList.add("is-invalid");
                isValid = false;
            } else {
                input.classList.remove("is-invalid");
            }

        }

    });

    return isValid;
}

    nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateStepUI();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepUI();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    updateStepUI() {
        // Hide all steps
        document.querySelectorAll('.step-section').forEach(section => {
            section.classList.add('d-none');
        });

        // Show current step
        const currentSection = document.querySelector(`[data-step="${this.currentStep}"]`);
        if (currentSection) {
            currentSection.classList.remove('d-none');
        }

        // Update progress bar
        const progressPercent = (this.currentStep / this.totalSteps) * 100;
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = progressPercent + '%';
        }

        // Update step counter
        const stepCounter = document.getElementById('currentStep');
        if (stepCounter) {
            stepCounter.textContent = this.currentStep;
        }

        // Update button visibility
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (prevBtn) {
            prevBtn.style.display = this.currentStep === 1 ? 'none' : 'block';
        }

        if (nextBtn) {
            nextBtn.style.display = this.currentStep === this.totalSteps ? 'none' : 'block';
        }

        if (submitBtn) {
            submitBtn.style.display = this.currentStep === this.totalSteps ? 'block' : 'none';
        }
        this.toggleRequiredFields();
    }

    

    toggleRequiredFields() {

    document.querySelectorAll('.step-section').forEach(section => {

        const isVisible = !section.classList.contains('d-none');

        section.querySelectorAll('input, textarea, select').forEach(field => {

            if (isVisible) {

                if (field.dataset.required === "true") {
                    field.setAttribute("required", "");
                }

            } else {

                if (field.hasAttribute("required")) {
                    field.dataset.required = "true";
                    field.removeAttribute("required");
                }

            }

        });

    });

}
    

    

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateStep(this.currentStep)) {
            return;
        }

        // Show loading modal
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        loadingModal.show();

        try {
            const formData = new FormData(this.form);

            const response = await fetch(this.submitUrl, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to success page
                window.location.href = `/success/${data.application_id}`;
            } else {
                loadingModal.hide();
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            loadingModal.hide();
            alert(`Error submitting form: ${error.message}`);
        }
    }
}

// ========================
// INPUT VALIDATION
// ========================

document.addEventListener('DOMContentLoaded', function() {
    // Add real-time validation feedback
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });

        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
});
