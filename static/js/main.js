// PixelPath - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize file uploads
    initializeFileUploads();
    
    // Initialize transmit form
    const transmitForm = document.getElementById('transmit-form');
    if (transmitForm) {
        transmitForm.addEventListener('submit', handleTransmitForm);
    }
    
    // Initialize receive form
    const receiveForm = document.getElementById('receive-form');
    if (receiveForm) {
        receiveForm.addEventListener('submit', handleReceiveForm);
    }
    
    // Initialize copy buttons
    initializeCopyButtons();
});

function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const filePreview = document.getElementById(`${input.id}-preview`);
            if (filePreview) {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        filePreview.src = e.target.result;
                        filePreview.style.display = 'block';
                        
                        // Show the filename
                        const filenameElement = document.getElementById(`${input.id}-name`);
                        if (filenameElement) {
                            filenameElement.textContent = input.files[0].name;
                            filenameElement.style.display = 'block';
                        }
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                }
            }
        });
    });
}

function handleTransmitForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loader
    toggleLoader(true);
    
    // Hide any previous results
    const resultSection = document.getElementById('transmit-result');
    if (resultSection) {
        resultSection.classList.remove('active');
    }
    
    // Validate form
    const keyword = formData.get('keyword');
    const primeNumber = formData.get('prime_number');
    const randomNumber = formData.get('random_number');
    const secretMessage = formData.get('secret_message');
    const image = formData.get('image');
    
    if (!keyword || !primeNumber || !randomNumber || !secretMessage || !image.name) {
        showError('Please fill in all fields and upload an image');
        toggleLoader(false);
        return;
    }
    
    // Send data to server
    fetch('/process_transmit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message and results
            displayTransmitResults(data.password, data.output_file);
            
            // Add this to display the visualization
            if (data.visualization_url) {
                // Create a section for the visualization
                const visualizationSection = document.createElement('div');
                visualizationSection.className = 'visualization-section';
                visualizationSection.innerHTML = `
                    <h3>Path Visualization</h3>
                    <p>This animation shows how the algorithm traversed the image to hide your message:</p>
                    <img src="${data.visualization_url}" alt="Path Visualization" style="max-width: 100%; margin-top: 10px;">
                `;
                
                // Append to the results container
                document.getElementById('results').appendChild(visualizationSection);
            }
        } else {
            showError(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        showError(error.message);
    })
    .finally(() => {
        toggleLoader(false);
    });
}

function handleReceiveForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loader
    toggleLoader(true);
    
    // Hide any previous results
    const resultSection = document.getElementById('receive-result');
    if (resultSection) {
        resultSection.classList.remove('active');
    }
    
    // Validate form
    const password = formData.get('password');
    const image = formData.get('image');
    
    if (!password || !image.name) {
        showError('Please enter the password and upload an image');
        toggleLoader(false);
        return;
    }
    
    // Send data to server
    fetch('/process_receive', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server error');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Show success message and results
            displayReceiveResults(data.message);
        } else {
            showError(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        showError(error.message);
    })
    .finally(() => {
        toggleLoader(false);
    });
}

function displayTransmitResults(password, outputFile) {
    const resultSection = document.getElementById('transmit-result');
    if (!resultSection) return;
    
    // Set password
    const passwordElement = document.getElementById('generated-password');
    if (passwordElement) {
        passwordElement.textContent = password;
    }
    
    // Set download link
    const downloadLink = document.getElementById('download-link');
    if (downloadLink) {
        downloadLink.href = `/download/${outputFile}`;
    }
    
    // Set Python file download link
    const pythonDownloadLink = document.getElementById('python-download-link');
    if (pythonDownloadLink) {
        pythonDownloadLink.href = '/encoder.py';
    }
    
    // Show the result section
    resultSection.classList.add('active');
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function displayReceiveResults(message) {
    const resultSection = document.getElementById('receive-result');
    if (!resultSection) return;
    
    // Set decoded message
    const messageElement = document.getElementById('decoded-message');
    if (messageElement) {
        messageElement.textContent = message;
    }
    
    // Show the result section
    resultSection.classList.add('active');
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function initializeCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.dataset.copy;
            const textElement = document.getElementById(textToCopy);
            
            if (textElement) {
                const text = textElement.textContent;
                navigator.clipboard.writeText(text).then(() => {
                    // Show copied confirmation
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i>';
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                });
            }
        });
    });
}

function toggleLoader(show) {
    const loaders = document.querySelectorAll('.loader');
    loaders.forEach(loader => {
        if (show) {
            loader.classList.add('active');
        } else {
            loader.classList.remove('active');
        }
    });
}

function showError(message) {
    // Create an error toast
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.innerHTML = `
        <div class="error-toast-content">
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        
        // Remove from DOM after animation
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Add styles for error toast
const style = document.createElement('style');
style.textContent = `
    .error-toast {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background-color: var(--error);
        color: white;
        padding: 12px 20px;
        border-radius: var(--border-radius);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        opacity: 0;
        transition: transform 0.3s ease, opacity 0.3s ease;
    }
    
    .error-toast.show {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
    
    .error-toast-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }
`;
document.head.appendChild(style);