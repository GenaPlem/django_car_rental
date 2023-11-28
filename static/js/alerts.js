// Waits for DOM content to load before showing the 'alertBox' for 5 seconds.
document.addEventListener('DOMContentLoaded', function () {
    const alert = document.getElementById('alertBox');
    setTimeout(() => {
        alert.classList.add('hide');
        setTimeout(() => {
            alert.remove();
        }, 600);
    }, 5000);
});