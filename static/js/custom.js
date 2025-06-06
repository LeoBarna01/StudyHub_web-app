/* StudyHub Custom JavaScript
 * This file contains interactive functionality and custom features for the StudyHub
 * web application including scroll indicators, navigation enhancements, form validation,
 * and various UI improvements for better user experience.
 */

/**
 * StudyHub - Custom JavaScript
 * Handles interactive elements and custom functionality
 */

// Scroll Indicator Component Initialization
// Initializes and manages the scroll-down indicator functionality
function initScrollIndicator() {
    const scrollIndicator = document.getElementById('scrollIndicator'); // Get scroll indicator element
    const backToTopButton = document.querySelector('.back-to-top'); // Get back-to-top button element
    
    if (!scrollIndicator) return; // Exit if scroll indicator not found
    
    // Function to check if user is at the bottom of the page
    function isAtBottom() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 100; // 100px threshold for bottom detection
    }
    
    // Function to handle scroll events and update indicator visibility
    function handleScroll() {
        if (isAtBottom() || window.scrollY > 1000) { // Hide if at bottom or scrolled far
            scrollIndicator.classList.add('hidden'); // Add hidden class to fade out
        } else {
            // Only show scroll indicator if we're not at the top and not at the bottom
            scrollIndicator.classList.remove('hidden'); // Remove hidden class to show
        }
    }
    
    // Add click event to scroll down smoothly
    scrollIndicator.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default link behavior
        window.scrollBy({
            top: window.innerHeight * 0.8, // Scroll 80% of viewport height
            behavior: 'smooth' // Smooth scrolling animation
        });
    });
    
    // Initial check for scroll position
    handleScroll();
    
    // Throttle scroll events for better performance
    let isScrolling; // Timeout variable for throttling
    window.addEventListener('scroll', function() {
        window.clearTimeout(isScrolling); // Clear previous timeout
        isScrolling = setTimeout(handleScroll, 50); // Set new timeout with 50ms delay
    });
}

// DOM Content Loaded Event Handler
document.addEventListener('DOMContentLoaded', function() {
    // Initialize scroll indicator functionality
    initScrollIndicator();
    
        // Bootstrap Tooltips Initialization
    // Initialize tooltips for all elements with data-bs-toggle="tooltip"
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); // Get all tooltip triggers
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl); // Initialize Bootstrap tooltip for each element
    });

    // Bootstrap Popovers Initialization  
    // Initialize popovers for all elements with data-bs-toggle="popover"
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')); // Get all popover triggers
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl); // Initialize Bootstrap popover for each element
    });

    // Back to Top Button Functionality
    // Manages visibility and behavior of the back-to-top button
    var backToTopButton = document.querySelector('.back-to-top'); // Get back-to-top button element
    if (backToTopButton) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) { // Show after scrolling 300px
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
                behavior: 'smooth' // Smooth scrolling animation
            });
        });
    }

    // Mobile Navigation Menu Handling
    // Auto-close mobile menu when navigation links are clicked
    var navLinks = document.querySelectorAll('.nav-link'); // Get all navigation links
    var menuToggle = document.getElementById('navbarNav'); // Get mobile menu toggle element
    if (menuToggle) {
        var bsCollapse = new bootstrap.Collapse(menuToggle, {toggle: false}); // Initialize Bootstrap collapse
        
        navLinks.forEach(function(l) {
            l.addEventListener('click', function() {
                if (window.innerWidth < 992) { // Only for mobile viewport (< 992px)
                    bsCollapse.toggle(); // Toggle mobile menu visibility
                }
            });
        });
    }

    // Smooth Scrolling for Anchor Links
    // Enables smooth scrolling for internal page anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href'); // Get target anchor href
            if (targetId === '#') return; // Skip if href is just "#"
            
            const targetElement = document.querySelector(targetId); // Find target element
            if (targetElement) {
                e.preventDefault(); // Prevent default anchor behavior
                const headerOffset = 90; // Height of your fixed header for offset calculation
                const elementPosition = targetElement.getBoundingClientRect().top; // Get element position
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset; // Calculate scroll position
                
                window.scrollTo({
                    top: offsetPosition, // Scroll to calculated position
                    behavior: 'smooth' // Smooth scrolling animation
                });
            }
        });
    });

    // Form Validation Enhancement
    // Adds Bootstrap validation styling to forms
    var forms = document.querySelectorAll('.needs-validation'); // Get all forms requiring validation
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) { // Check if form is valid
                event.preventDefault(); // Prevent form submission
                event.stopPropagation(); // Stop event propagation
            }
            
            form.classList.add('was-validated'); // Add Bootstrap validation classes
        }, false);
    });

    // AOS (Animate On Scroll) Library Initialization
    // Initialize AOS animations if library is available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800, // Animation duration in milliseconds
            easing: 'ease-in-out', // Animation easing function
            once: true, // Animation occurs only once
            mirror: false // Don't animate elements out while scrolling past them
        });
    }
});

// Utility Functions
// Debounce function for scroll/resize events to improve performance
function debounce(func, wait, immediate) {
    var timeout; // Timeout variable for debouncing
    return function() {
        var context = this, args = arguments; // Preserve context and arguments
        var later = function() {
            timeout = null; // Clear timeout
            if (!immediate) func.apply(context, args); // Execute function if not immediate
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Add active class to current nav link
var sections = document.querySelectorAll('section[id]');

function scrollActive() {
    var scrollY = window.pageYOffset;

    sections.forEach(function(current) {
        var sectionHeight = current.offsetHeight;
        var sectionTop = current.offsetTop - 100;
        var sectionId = current.getAttribute('id');
        var navLink = document.querySelector('.nav-menu a[href*=' + sectionId + ']');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            if (navLink) {
                navLink.classList.add('active');
                navLink.setAttribute('aria-current', 'page');
            }
        } else if (navLink) {
            navLink.classList.remove('active');
            navLink.removeAttribute('aria-current');
        }
    });
}

window.addEventListener('scroll', debounce(scrollActive, 10));

// Handle file upload preview
function handleFileSelect(event) {
    var file = event.target.files[0];
    if (!file) return;
    
    var preview = document.getElementById('file-preview');
    var fileName = document.getElementById('file-name');
    
    if (file) {
        // Display file name
        if (fileName) {
            fileName.textContent = file.name;
        }
        
        // Display preview if it's an image
        if (file.type.startsWith('image/') && preview) {
            var reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else if (preview) {
            preview.style.display = 'none';
        }
    }
}

// Initialize file input preview if exists
var fileInput = document.getElementById('file-upload');
if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
}

// Handle password visibility toggle
function togglePassword(inputId) {
    var passwordInput = document.getElementById(inputId);
    var icon = document.querySelector('[onclick="togglePassword(\'' + inputId + '\')"] i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Handle avatar image loading errors
function handleAvatarError(img) {
    img.onerror = null;
    img.classList.add('d-none');
    const fallback = img.nextElementSibling;
    if (fallback && fallback.classList.contains('avatar-fallback')) {
        fallback.classList.remove('d-none');
    }
    return true;
}

// Initialize any counters with data attributes
document.addEventListener('DOMContentLoaded', function() {
    var counters = document.querySelectorAll('[data-counter]');
    
    if (counters.length > 0) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var target = entry.target;
                    var targetValue = parseInt(target.getAttribute('data-counter'));
                    var duration = 2000; // 2 seconds
                    var step = (targetValue / (duration / 16)); // 60fps
                    var current = 0;
                    
                    var updateCounter = function() {
                        current += step;
                        if (current < targetValue) {
                            target.textContent = Math.ceil(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            target.textContent = targetValue.toLocaleString();
                        }
                    };
                    
                    updateCounter();
                    observer.unobserve(target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(function(counter) {
            observer.observe(counter);
        });
    }
});
