// automatically hide flasg messages
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach((message) => {
        message.classList.remove('show');  
        message.classList.add('fade');    
        setTimeout(() => message.remove(), 500);  
    });
}, 3000); // sets the screen to automatically hide after 3 seconds
