document.addEventListener('DOMContentLoaded', (event) => {
    const alertButtons = document.querySelectorAll('.alert #close');
    alertButtons.forEach(button => {
        button.addEventListener('click', () => {
        button.parentElement.style.display = 'none';
        });
    });
});