document.addEventListener("DOMContentLoaded", function() {
    const errorCodeElement = document.querySelector(".error-code p");

    let isRed = false;
    let interval = 1000
    setInterval(() => {
        if (isRed) {
            errorCodeElement.style.color = "";
            interval = 1000
        } else {
            errorCodeElement.style.color = "red";
            interval = 3000
        }
        isRed = !isRed;
    }, interval);
});