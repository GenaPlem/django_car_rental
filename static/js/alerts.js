document.addEventListener('DOMContentLoaded', function() {
    const alert = document.getElementById('alertBox');
    setTimeout(() => {
        alert.classList.add('hide');
        setTimeout(() => {
            alert.remove();
        }, 600);
        }, 5000);
});