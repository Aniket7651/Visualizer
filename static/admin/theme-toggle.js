

document.addEventListener('DOMContentLoaded', () => {
    const toggle_btn = document.getElementById('theme-btn');
    const body = document.body;
    
    function setTheme(theme) {
        if(theme === 'dark') {
            body.classList.add('dark-theme');
            toggle_btn.innerHTML = "<i class='material-icons' style='color: white;'>wb_sunny</i>";
        } else {
            body.classList.remove('dark-theme');
            toggle_btn.innerHTML = "<i class='fa fa-moon-o' style='font-size: 20px; color: #5743c8;'></i>";
        }
    }

    const saveTheme = localStorage.getItem('theme');
    setTheme(saveTheme || 'light');

    toggle_btn.addEventListener('click', (event) => {
        event.stopPropagation();
        const newTheme = body.classList.contains('dark-theme') ? 'light': 'dark';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    })


})