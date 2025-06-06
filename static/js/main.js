/* StudyHub Main JavaScript File
 * This is the primary JavaScript file for the StudyHub web application that handles
 * core interactive elements, animations, and user interface enhancements including
 * navigation effects, form validation, and smooth scrolling functionality.
 */

/**
 * StudyHub - Main JavaScript File
 * Handles all interactive elements and animations
 */

// Main Application Initialization
document.addEventListener('DOMContentLoaded', function() {
    // Navigation Bar Scroll Effects
    // Adds visual changes to navbar when user scrolls
    const navbar = document.querySelector('.navbar'); // Get navigation bar element
    const navbarHeight = 80; // Height of the navbar in pixels for scroll threshold
    
    // Add scroll event listener for navbar styling
    window.addEventListener('scroll', function() {
        if (window.scrollY > navbarHeight) { // Check if scrolled past navbar height
            navbar.classList.add('scrolled'); // Add scrolled class for styling
        } else {
            navbar.classList.remove('scrolled'); // Remove scrolled class when at top
        }
    });
    
    // Bootstrap Tooltips Initialization
    // Initialize all Bootstrap tooltips on the page
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); // Get tooltip elements
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl); // Initialize Bootstrap tooltip
    });
    
    // Bootstrap Popovers Initialization
    // Initialize all Bootstrap popovers on the page
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')); // Get popover elements
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl); // Initialize Bootstrap popover
    });
    
    // Mobile Navigation Menu Management
    // Auto-close mobile menu when navigation links are clicked
    const navLinks = document.querySelectorAll('.nav-link'); // Get all navigation links
    const menuToggle = document.getElementById('navbarNav'); // Get mobile menu toggle element
    const bsCollapse = new bootstrap.Collapse(menuToggle, {toggle: false}); // Initialize Bootstrap collapse
    
    navLinks.forEach(function(l) {
        l.addEventListener('click', function() {
            if (window.innerWidth < 992) { // Only for mobile viewport (< 992px Bootstrap lg breakpoint)
                bsCollapse.toggle(); // Toggle mobile menu visibility
            }
        });
    });
    
    // Smooth Scrolling for Internal Anchor Links
    // Enables smooth scrolling behavior for all internal page anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default anchor behavior
            
            const targetId = this.getAttribute('href'); // Get target anchor ID
            if (targetId === '#') return; // Skip if href is just "#"
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 90; // Height of your fixed header
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Back to Top Button Functionality
    // Manages the visibility and behavior of the back-to-top button
    const backToTopButton = document.querySelector('.back-to-top'); // Get back-to-top button element
    if (backToTopButton) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) { // Show button after scrolling 300px
                backToTopButton.classList.add('show'); // Add show class for visibility
            } else {
                backToTopButton.classList.remove('show'); // Remove show class to hide
            }
        });
        
        // Smooth scroll to top when button is clicked
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default behavior
            window.scrollTo({
                top: 0, // Scroll to top of page
                behavior: 'smooth' // Enable smooth scrolling animation
            });
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Initialize AOS (Animate On Scroll) if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }
});

// Debounce function for scroll/resize events
function debounce(func, wait = 10, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Navigation Active State Management
// Highlights active navigation links based on current section in viewport
const sections = document.querySelectorAll('section[id]'); // Get all sections with IDs

function scrollActive() {
    const scrollY = window.pageYOffset; // Get current scroll position

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight; // Get section height
        const sectionTop = current.offsetTop - 100; // Get section top position with offset
        const sectionId = current.getAttribute('id'); // Get section ID
        const navLink = document.querySelector(`.nav-menu a[href*=${sectionId}]`); // Find corresponding nav link

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) { // Check if section is in viewport
            navLink?.classList.add('active'); // Add active class to nav link
            navLink?.setAttribute('aria-current', 'page'); // Set accessibility attribute
        } else {
            navLink?.classList.remove('active'); // Remove active class from nav link
            navLink?.removeAttribute('aria-current'); // Remove accessibility attribute
        }
    });
}

window.addEventListener('scroll', debounce(scrollActive)); // Apply debounced scroll listener

// Lightbox Initialization
// Configure lightbox plugin if available for image galleries
if (typeof lightbox !== 'undefined') {
    lightbox.option({
        'resizeDuration': 200, // Animation duration for resize
        'wrapAround': true, // Enable cycling through images
        'showImageNumberLabel': false, // Hide image counter
        'positionFromTop': 100 // Distance from top of viewport
    });
}

// File Upload Preview Handler
// Displays selected file information and image previews
function handleFileSelect(event) {
    const file = event.target.files[0]; // Get selected file
    if (!file) return; // Exit if no file selected
    
    const preview = document.getElementById('file-preview'); // Get preview image element
    const fileName = document.getElementById('file-name'); // Get filename display element
    
    if (file) {
        // Display file name in designated element
        fileName.textContent = file.name; // Show selected filename
        
        // Display preview for image files only
        if (file.type.startsWith('image/')) { // Check if file is an image
            const reader = new FileReader(); // Create FileReader for image preview
            reader.onload = function(e) {
                preview.src = e.target.result; // Set preview image source
                preview.style.display = 'block'; // Show preview image
            };
            reader.readAsDataURL(file); // Read file as data URL for preview
        } else {
            preview.style.display = 'none'; // Hide preview for non-image files
        }
    }
}

// File Input Event Listener Setup
// Initialize file upload preview functionality if file input exists
const fileInput = document.getElementById('file-upload'); // Get file input element
if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect); // Attach change event listener
}

// Password Visibility Toggle Function
// Toggles password field visibility and updates eye icon accordingly
function togglePassword(inputId) {
    const passwordInput = document.getElementById(inputId); // Get password input by ID
    const icon = document.querySelector(`[onclick="togglePassword('${inputId}')"] i`); // Get associated toggle icon
    
    if (passwordInput.type === 'password') { // If password is currently hidden
        passwordInput.type = 'text'; // Show password as plain text
        icon.classList.remove('fa-eye'); // Remove closed eye icon
        icon.classList.add('fa-eye-slash'); // Add crossed eye icon
    } else { // If password is currently visible
        passwordInput.type = 'password'; // Hide password
        icon.classList.remove('fa-eye-slash'); // Remove crossed eye icon
        icon.classList.add('fa-eye'); // Add closed eye icon
    }
}

// Animated Counter Initialization
// Animates numbers from 0 to target value when elements come into viewport
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('[data-counter]'); // Get all elements with counter data attribute
    
    if (counters.length > 0) { // Only proceed if counters exist on page
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) { // When counter enters viewport
                    const target = entry.target; // Get counter element
                    const targetValue = parseInt(target.getAttribute('data-counter')); // Get target number
                    const duration = 2000; // Animation duration (2 seconds)
                    const step = (targetValue / (duration / 16)); // Calculate step size for 60fps
                    let current = 0; // Starting value
                    
                    const updateCounter = () => {
                        current += step; // Increment current value
                        if (current < targetValue) { // Continue animation if not reached target
                            target.textContent = Math.ceil(current); // Update displayed number
                            requestAnimationFrame(updateCounter); // Schedule next frame
                        } else {
                            target.textContent = targetValue.toLocaleString(); // Final formatted number
                        }
                    };
                    
                    updateCounter(); // Start animation
                    observer.unobserve(target); // Stop observing this element
                }
            });
        }, { threshold: 0.5 }); // Trigger when 50% of element is visible
        
        counters.forEach(counter => {
            observer.observe(counter); // Start observing each counter element
        });
    }
});
