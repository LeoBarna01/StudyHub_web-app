/**
 * StudyHub - Custom JavaScript
 * Handles interactive elements and custom functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Back to top button
    var backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Mobile menu close on click
    var navLinks = document.querySelectorAll('.nav-link');
    var menuToggle = document.getElementById('navbarNav');
    if (menuToggle) {
        var bsCollapse = new bootstrap.Collapse(menuToggle, {toggle: false});
        
        navLinks.forEach(function(l) {
            l.addEventListener('click', function() {
                if (window.innerWidth < 992) { // Only for mobile
                    bsCollapse.toggle();
                }
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
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

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
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
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
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
