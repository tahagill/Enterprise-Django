/**
 * AJAX Form Submission Handler
 * Handles form submissions via AJAX for better UX
 */

document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * Handle AJAX form submission
     */
    function setupAjaxForm(formId, options = {}) {
        const form = document.getElementById(formId);
        if (!form) return;

        const {
            successMessage = 'Form submitted successfully!',
            successCallback = null,
            errorCallback = null,
            beforeSubmit = null
        } = options;

        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Call beforeSubmit callback if provided
            if (beforeSubmit && typeof beforeSubmit === 'function') {
                if (!beforeSubmit(form)) {
                    return; // Cancel submission if beforeSubmit returns false
                }
            }

            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const originalButtonText = submitButton ? submitButton.innerHTML : '';

            // Disable submit button and show loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...';
            }

            // Get CSRF token
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send AJAX request
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Re-enable submit button
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalButtonText;
                }

                if (data.success) {
                    // Show success message
                    showAlert('success', data.message || successMessage);
                    
                    // Reset form
                    form.reset();

                    // Call success callback if provided
                    if (successCallback && typeof successCallback === 'function') {
                        successCallback(data);
                    }

                    // Redirect if redirect_url is provided
                    if (data.redirect_url) {
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500);
                    }
                } else {
                    // Show error messages
                    if (data.errors) {
                        displayFormErrors(form, data.errors);
                    } else {
                        showAlert('danger', data.message || 'An error occurred. Please try again.');
                    }

                    // Call error callback if provided
                    if (errorCallback && typeof errorCallback === 'function') {
                        errorCallback(data);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Re-enable submit button
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalButtonText;
                }

                showAlert('danger', 'An error occurred. Please try again.');

                // Call error callback if provided
                if (errorCallback && typeof errorCallback === 'function') {
                    errorCallback(error);
                }
            });
        });
    }

    /**
     * Display form field errors
     */
    function displayFormErrors(form, errors) {
        // Clear previous errors
        form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

        // Display field errors
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.classList.add('is-invalid');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback d-block';
                errorDiv.textContent = errors[fieldName].join(', ');
                
                field.parentNode.appendChild(errorDiv);
            }
        });

        // Display non-field errors
        if (errors.__all__) {
            showAlert('danger', errors.__all__.join(', '));
        }
    }

    /**
     * Show Bootstrap alert
     */
    function showAlert(type, message) {
        const alertContainer = document.getElementById('alert-container') || createAlertContainer();
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertContainer.appendChild(alert);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);

        // Scroll to alert
        alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Create alert container if it doesn't exist
     */
    function createAlertContainer() {
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.style.position = 'fixed';
        container.style.top = '70px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.maxWidth = '400px';
        document.body.appendChild(container);
        return container;
    }

    // Make setupAjaxForm globally available
    window.setupAjaxForm = setupAjaxForm;
});
