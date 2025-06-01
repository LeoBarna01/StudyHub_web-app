// DOM Elements
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');
const searchForm = document.getElementById('searchForm');
const uploadForm = document.getElementById('uploadForm');
const questionForm = document.getElementById('questionForm');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const fileInfo = document.getElementById('fileInfo');
const loadingIndicator = document.getElementById('loadingIndicator');
const toastContainer = document.getElementById('toastContainer');

// Mobile Menu Toggle
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
    });
}

// Set active navigation link
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// File Upload Preview
if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileInfo.textContent = `Selected file: ${file.name} (${formatFileSize(file.size)})`;
            
            // Show preview for images and PDFs
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    filePreview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="img-preview">`;
                    filePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else if (file.type === 'application/pdf') {
                filePreview.innerHTML = `
                    <div class="pdf-preview">
                        <i class="fas fa-file-pdf"></i>
                        <p>PDF Document</p>
                    </div>`;
                filePreview.style.display = 'block';
            } else {
                filePreview.innerHTML = `
                    <div class="file-preview">
                        <i class="fas fa-file"></i>
                        <p>${file.name}</p>
                    </div>`;
                filePreview.style.display = 'block';
            }
        }
    });
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form Submission with AJAX
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        const submitBtn = uploadForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        
        try {
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showToast('File uploaded successfully!', 'success');
                uploadForm.reset();
                filePreview.style.display = 'none';
                fileInfo.textContent = 'No file selected';
            } else {
                throw new Error(result.error || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            showToast(error.message || 'An error occurred during upload', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
}

// Search Form Submission
if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(searchForm);
        const searchQuery = formData.get('query');
        const searchType = formData.get('type');
        
        try {
            // Show loading state
            const searchResults = document.getElementById('searchResults');
            if (searchResults) {
                searchResults.innerHTML = '<div class="loading">Searching...</div>';
            }
            
            // In a real app, this would be an API call
            // const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}&type=${searchType}`);
            // const results = await response.json();
            
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Display results (simulated)
            if (searchResults) {
                searchResults.innerHTML = `
                    <div class="search-meta">
                        <p>Showing results for: <strong>${searchQuery}</strong></p>
                        <p class="text-muted">5 documents found</p>
                    </div>
                    <div class="document-grid">
                        ${generateMockDocuments()}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Search error:', error);
            showToast('An error occurred during search', 'error');
        }
    });
}

// Generate mock documents for search results
function generateMockDocuments() {
    const mockDocs = [
        {
            title: 'Introduction to Computer Science',
            author: 'Prof. John Smith',
            course: 'CS101',
            type: 'Lecture Notes',
            date: '2023-10-15',
            pages: 24
        },
        {
            title: 'Algorithms and Data Structures',
            author: 'Dr. Sarah Johnson',
            course: 'CS201',
            type: 'Textbook',
            date: '2023-09-28',
            pages: 156
        },
        {
            title: 'Web Development Fundamentals',
            author: 'Prof. Michael Brown',
            course: 'WEB101',
            type: 'Slides',
            date: '2023-11-02',
            pages: 42
        },
        {
            title: 'Database Systems',
            author: 'Dr. Emily Davis',
            course: 'CS301',
            type: 'Study Guide',
            date: '2023-10-10',
            pages: 87
        },
        {
            title: 'Artificial Intelligence Basics',
            author: 'Prof. Robert Wilson',
            course: 'CS401',
            type: 'Research Paper',
            date: '2023-09-15',
            pages: 12
        }
    ];
    
    return mockDocs.map(doc => `
        <div class="document-card">
            <div class="document-icon">
                <i class="fas fa-file-alt"></i>
            </div>
            <div class="document-details">
                <h4>${doc.title}</h4>
                <p class="document-meta">
                    <span><i class="fas fa-user"></i> ${doc.author}</span>
                    <span><i class="fas fa-book"></i> ${doc.course}</span>
                    <span><i class="fas fa-tag"></i> ${doc.type}</span>
                </p>
                <p class="document-info">
                    <span><i class="far fa-calendar"></i> ${doc.date}</span>
                    <span><i class="far fa-file"></i> ${doc.pages} pages</span>
                </p>
                <div class="document-actions">
                    <button class="btn btn-outline btn-sm"><i class="far fa-eye"></i> Preview</button>
                    <button class="btn btn-primary btn-sm"><i class="fas fa-download"></i> Download</button>
                    <button class="btn btn-icon" title="Save for later"><i class="far fa-bookmark"></i></button>
                </div>
            </div>
        </div>
    `).join('');
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">
            ${getToastIcon(type)}
        </div>
        <div class="toast-message">${message}</div>
        <button class="toast-close">&times;</button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-remove toast after delay
    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }, 100);
    
    // Close button
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    });
}

// Get icon for toast based on type
function getToastIcon(type) {
    const icons = {
        success: '<i class="fas fa-check-circle"></i>',
        error: '<i class="fas fa-exclamation-circle"></i>',
        warning: '<i class="fas fa-exclamation-triangle"></i>',
        info: '<i class="fas fa-info-circle"></i>'
    };
    return icons[type] || icons.info;
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Document ready
document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
    initTooltips();
    
    // Initialize any other components
    if (typeof bootstrap !== 'undefined') {
        // Initialize Bootstrap components if available
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // Account for fixed header
                behavior: 'smooth'
            });
        }
    });
});

// Handle document cards interaction
document.addEventListener('click', (e) => {
    const card = e.target.closest('.document-card');
    if (card && !e.target.closest('.document-actions')) {
        // Navigate to document detail page or show preview
        console.log('Document selected:', card.querySelector('h4').textContent);
        // window.location.href = `/document/${card.dataset.id}`;
    }
});