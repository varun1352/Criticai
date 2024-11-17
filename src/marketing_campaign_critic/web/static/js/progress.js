document.addEventListener('DOMContentLoaded', () => {
    const formSteps = document.querySelectorAll('.form-step');
    const nextButtons = document.querySelectorAll('.next-button');
    const backButtons = document.querySelectorAll('.back-button');
    const progressBar = document.querySelector('.progress-bar .progress');
    const form = document.getElementById('campaignForm');
    let currentStep = 0;

    function updateStep() {
        formSteps.forEach((step, index) => {
            step.classList.toggle('active', index === currentStep);
        });
        progressBar.style.width = `${(currentStep / (formSteps.length - 1)) * 100}%`;
    }

    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Temporarily disabling validation for testing
            if (currentStep < formSteps.length - 1) {
                currentStep++;
                updateStep();
            } else {
                console.log('All steps completed. Submitting the form...');
                if (form) form.submit();
            }
        });
    });

    backButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateStep();
            }
        });
    });

    updateStep();
});

// Toggle dropdowns
document.querySelectorAll('.dropdown-header').forEach((header) => {
    header.addEventListener('click', function () {
        const target = document.getElementById(this.getAttribute('data-target'));
        const isOpen = target && target.style.display === 'block';

        // Close all dropdowns
        document.querySelectorAll('.dropdown-content').forEach((content) => {
            content.style.display = 'none';
        });

        // Toggle the clicked dropdown
        if (!isOpen && target) {
            target.style.display = 'block';
        }

        // Update arrow direction
        document.querySelectorAll('.dropdown-header').forEach((hdr) => {
            hdr.classList.remove('active');
        });

        if (!isOpen) {
            this.classList.add('active');
        }
    });
});

// Collapsible Section Toggle
document.querySelectorAll('.collapsible-header').forEach((header) => {
    header.addEventListener('click', function () {
        const content = this.nextElementSibling;
        const isActive = content && content.style.display === 'block';

        // Close all collapsible sections
        document.querySelectorAll('.collapsible-content').forEach((section) => {
            section.style.display = 'none';
        });

        // Toggle current section
        if (content) {
            content.style.display = isActive ? 'none' : 'block';
        }

        // Update header active state
        document.querySelectorAll('.collapsible-header').forEach((hdr) => {
            hdr.classList.remove('active');
        });

        if (!isActive) {
            this.classList.add('active');
        }
    });
});
