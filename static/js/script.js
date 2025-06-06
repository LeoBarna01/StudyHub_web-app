/* StudyHub Application Scripts
 * This file contains core JavaScript functionality for the StudyHub web application
 * including mobile navigation, file upload handling, form submissions, search features,
 * and various utility functions for enhanced user interaction.
 */

// DOM Element References
// Cache frequently used DOM elements for better performance
const mobileMenuBtn = document.querySelector('.mobile-menu-btn'); // Mobile menu toggle button
const navLinks = document.querySelector('.nav-links'); // Navigation links container
const searchForm = document.getElementById('searchForm'); // Main search form
const uploadForm = document.getElementById('uploadForm'); // File upload form
const questionForm = document.getElementById('questionForm'); // Question submission form
const fileInput = document.getElementById('fileInput'); // File input element
const filePreview = document.getElementById('filePreview'); // File preview container
const fileInfo = document.getElementById('fileInfo'); // File information display
const loadingIndicator = document.getElementById('loadingIndicator'); // Loading spinner element
const toastContainer = document.getElementById('toastContainer'); // Toast notification container

// Mobile Navigation Menu Toggle
// Handles opening/closing of mobile navigation menu
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active'); // Toggle navigation visibility
        mobileMenuBtn.classList.toggle('active'); // Toggle button active state
    });
}

// Active Navigation Link Highlighter
// Sets the active state for navigation links based on current page
function setActiveNavLink() {
    const currentPath = window.location.pathname; // Get current page path
    const navLinks = document.querySelectorAll('.nav-links a'); // Get all navigation links
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) { // Check if link matches current path
            link.classList.add('active'); // Add active class to current page link
        } else {
            link.classList.remove('active'); // Remove active class from other links
        }
    });
}

// File Upload Preview Functionality
// Provides visual preview of selected files before upload
if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0]; // Get selected file
        if (file) {
            fileInfo.textContent = `Selected file: ${file.name} (${formatFileSize(file.size)})`; // Display file info
            
            // Show preview for images and PDFs based on file type
            if (file.type.startsWith('image/')) { // Handle image files
                const reader = new FileReader(); // Create file reader for image preview
                reader.onload = (e) => {
                    filePreview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="img-preview">`; // Display image preview
                    filePreview.style.display = 'block'; // Show preview container
                };
                reader.readAsDataURL(file); // Read file as data URL
            } else if (file.type === 'application/pdf') { // Handle PDF files
                filePreview.innerHTML = `
                    <div class="pdf-preview">
                        <i class="fas fa-file-pdf"></i>
                        <p>PDF Document</p>
                    </div>`; // Display PDF preview with icon
                filePreview.style.display = 'block'; // Show preview container
            } else { // Handle other file types
                filePreview.innerHTML = `
                    <div class="file-preview">
                        <i class="fas fa-file"></i>
                        <p>${file.name}</p>
                    </div>`; // Display generic file preview
                filePreview.style.display = 'block'; // Show preview container
            }
        }
    });
}

// File Size Formatting Utility
// Converts bytes to human-readable file size format
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'; // Handle zero bytes case
    const k = 1024; // Kilobyte conversion factor
    const sizes = ['Bytes', 'KB', 'MB', 'GB']; // Size unit labels
    const i = Math.floor(Math.log(bytes) / Math.log(k)); // Calculate appropriate unit index
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]; // Format and return readable size
}

// AJAX Form Submission Handler
// Handles asynchronous form submissions with loading states and feedback
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission
        
        const formData = new FormData(uploadForm); // Create form data object
        const submitBtn = uploadForm.querySelector('button[type="submit"]'); // Get submit button
        const originalBtnText = submitBtn.innerHTML; // Store original button text
        
        try {
            // Show loading state during upload
            submitBtn.disabled = true; // Disable button to prevent multiple submissions
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...'; // Show loading spinner
            
            const response = await fetch('/upload', {
                method: 'POST', // POST request for file upload
                body: formData // Send form data
            });
            
            const result = await response.json(); // Parse JSON response
            
            if (response.ok) { // Check if upload was successful
                showToast('File uploaded successfully!', 'success'); // Show success message
                uploadForm.reset(); // Clear form fields
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

// Question Form Submission Handler
// Handles form submission for user questions with validation
if (questionForm) {
    questionForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission
        
        const formData = new FormData(questionForm); // Create form data object
        const submitBtn = questionForm.querySelector('button[type="submit"]'); // Get submit button
        const originalBtnText = submitBtn.innerHTML; // Store original button text
        
        try {
            // Show loading state during submission
            submitBtn.disabled = true; // Disable button to prevent multiple submissions
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...'; // Show loading spinner
            
            const response = await fetch('/questions', {
                method: 'POST', // POST request for question submission
                body: formData // Send form data
            });
            
            const result = await response.json(); // Parse JSON response
            
            if (response.ok) { // Check if submission was successful
                showToast('Question submitted successfully!', 'success'); // Show success message
                questionForm.reset(); // Clear form fields
            } else {
                throw new Error(result.error || 'Submission failed'); // Handle error response
            }
        } catch (error) {
            console.error('Question submission error:', error); // Log error to console
            showToast(error.message || 'An error occurred during submission', 'error'); // Show error message
        } finally {
            // Restore button state regardless of outcome
            submitBtn.disabled = false; // Re-enable submit button
            submitBtn.innerHTML = originalBtnText; // Restore original button text
        }
    });
}

// Search Form Submission Handler
// Handles search form submission with loading states and result display
if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission
        
        const formData = new FormData(searchForm); // Create form data object
        const searchQuery = formData.get('query'); // Get search query from form
        const searchType = formData.get('type'); // Get search type filter
        
        try {
            // Show loading state during search
            const searchResults = document.getElementById('searchResults'); // Get search results container
            if (searchResults) {
                searchResults.innerHTML = '<div class="loading">Searching...</div>'; // Show loading message
            }
            
            // Make API call to search endpoint
            const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}&type=${searchType}`);
            const results = await response.json(); // Parse JSON response
            
            // Simulate API call delay for demonstration
            await new Promise(resolve => setTimeout(resolve, 1000)); // Add delay for UX
            
            // Display search results in the results container
            if (searchResults) {
                searchResults.innerHTML = `
                    <div class="search-meta">
                        <p>Showing results for: <strong>${searchQuery}</strong></p>
                        <p class="text-muted">5 documents found</p>
                    </div>
                    <div class="document-grid">
                        ${generateMockDocuments()}
                    </div>
                `; // Display search results and metadata
            }
        } catch (error) {
            console.error('Search error:', error); // Log error to console
            showToast('An error occurred during search', 'error'); // Show error notification
        }
    });
}

// Mock Document Generator
// Creates sample document data for search results demonstration
function generateMockDocuments() {
    // Sample document data for testing and demonstration
    const mockDocs = [
        {
            title: 'Introduction to Computer Science', // Document title
            author: 'Prof. John Smith', // Document author
            course: 'CS101', // Associated course code
            type: 'Lecture Notes', // Document type/category
            date: '2023-10-15', // Publication date
            pages: 24 // Number of pages
        },
        {
            title: 'Algorithms and Data Structures', // Document title
            author: 'Dr. Sarah Johnson', // Document author
            course: 'CS201', // Associated course code
            type: 'Textbook', // Document type/category
            date: '2023-09-28', // Publication date
            pages: 156 // Number of pages
        },
        {
            title: 'Web Development Fundamentals', // Document title
            author: 'Prof. Michael Brown', // Document author
            course: 'WEB101', // Associated course code
            type: 'Slides', // Document type/category
            date: '2023-11-02', // Publication date
            pages: 42 // Number of pages
        },
        {
            title: 'Database Systems', // Document title
            author: 'Dr. Emily Davis', // Document author
            course: 'CS301', // Associated course code
            type: 'Study Guide', // Document type/category
            date: '2023-10-10', // Publication date
            pages: 87 // Number of pages
        },
        {
            title: 'Artificial Intelligence Basics', // Document title
            author: 'Prof. Robert Wilson', // Document author
            course: 'CS401', // Associated course code
            type: 'Research Paper', // Document type/category
            date: '2023-09-15', // Publication date
            pages: 12 // Number of pages
        }
    ];
    
    // Generate HTML for each document card
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
    `).join(''); // Join all document cards into a single HTML string
}

// Toast Notification System
// Displays temporary notification messages to users with different types and auto-dismissal
function showToast(message, type = 'info') {
    const toast = document.createElement('div'); // Create toast container element
    toast.className = `toast ${type}`; // Set CSS classes for styling and type
    toast.innerHTML = `
        <div class="toast-icon">
            ${getToastIcon(type)}
        </div>
        <div class="toast-message">${message}</div>
        <button class="toast-close">&times;</button>
    `; // Build toast HTML structure with icon, message, and close button
    
    toastContainer.appendChild(toast); // Add toast to container in DOM
    
    // Auto-remove toast after delay with smooth animations
    setTimeout(() => {
        toast.classList.add('show'); // Show toast with CSS animation
        setTimeout(() => {
            toast.classList.remove('show'); // Start hide animation
            setTimeout(() => toast.remove(), 300); // Remove from DOM after animation
        }, 3000); // Display duration (3 seconds)
    }, 100); // Small delay for smooth appearance
    
    // Manual close button functionality
    const closeBtn = toast.querySelector('.toast-close'); // Get close button element
    closeBtn.addEventListener('click', () => {
        toast.classList.remove('show'); // Start hide animation
        setTimeout(() => toast.remove(), 300); // Remove from DOM after animation
    });
}

// Toast Icon Provider
// Returns appropriate FontAwesome icon HTML based on toast type
function getToastIcon(type) {
    const icons = {
        success: '<i class="fas fa-check-circle"></i>', // Success checkmark icon
        error: '<i class="fas fa-exclamation-circle"></i>', // Error exclamation icon
        warning: '<i class="fas fa-exclamation-triangle"></i>', // Warning triangle icon
        info: '<i class="fas fa-info-circle"></i>' // Information circle icon
    };
    return icons[type] || icons.info; // Return icon for type or default to info
}

// Bootstrap Tooltip Initialization
// Initializes Bootstrap tooltips for elements with data-bs-toggle="tooltip" attribute
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); // Get all tooltip trigger elements
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl); // Initialize tooltip for each element
    });
}

// Document Ready Event Handler
// Executes initialization functions when DOM content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink(); // Set active navigation link based on current page
    initTooltips(); // Initialize Bootstrap tooltips
    
    // Initialize additional Bootstrap components if library is available
    if (typeof bootstrap !== 'undefined') {
        // Initialize Bootstrap tooltips globally for all tooltip triggers
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); // Get tooltip elements
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl)); // Create tooltip instances
    }
});

// Smooth Scrolling for Anchor Links
// Provides smooth scrolling behavior for internal page navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default anchor link behavior
        
        const targetId = this.getAttribute('href'); // Get target element ID from href
        if (targetId === '#') return; // Skip empty anchor links
        
        const targetElement = document.querySelector(targetId); // Find target element
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // Account for fixed header height (80px)
                behavior: 'smooth' // Enable smooth scrolling animation
            });
        }
    });
});

// Document Card Interaction Handler
// Handles clicks on document cards for navigation and preview functionality
document.addEventListener('click', (e) => {
    const card = e.target.closest('.document-card'); // Find closest document card element
    if (card && !e.target.closest('.document-actions')) { // Check if click is on card but not on action buttons
        // Navigate to document detail page or show preview modal
        console.log('Document selected:', card.querySelector('h4').textContent); // Log selected document title
        // Future implementation: navigate to document detail page
        // window.location.href = `/document/${card.dataset.id}`;
    }
});