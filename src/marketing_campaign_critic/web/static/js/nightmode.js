document.addEventListener('DOMContentLoaded', () => {
    // Check for saved dark mode preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }

    // Toggle night mode
    const toggleButton = document.getElementById('night-mode-toggle');
    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });
});

function toggleMenu() {
    const navList = document.querySelector('.nav-list');
    navList.classList.toggle('active'); /* Toggle the "active" class */
}
