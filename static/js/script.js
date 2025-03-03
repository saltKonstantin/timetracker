// TimeTracker JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 1s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 1000);
        }, 5000);
    });

    // Add quick navigation to date
    const dateInput = document.createElement('input');
    dateInput.type = 'date';
    dateInput.className = 'form-control d-inline-block me-2';
    dateInput.style.width = 'auto';
    dateInput.value = new Date().toISOString().split('T')[0];
    
    const goButton = document.createElement('button');
    goButton.className = 'btn btn-sm btn-outline-primary';
    goButton.textContent = 'Go';
    goButton.addEventListener('click', function() {
        window.location.href = '/?date=' + dateInput.value;
    });
    
    // Find the button group to append to
    const btnGroup = document.querySelector('.btn-group');
    if (btnGroup) {
        const dateNav = document.createElement('div');
        dateNav.className = 'date-navigation mt-2';
        dateNav.appendChild(dateInput);
        dateNav.appendChild(goButton);
        btnGroup.parentNode.appendChild(dateNav);
    }
});