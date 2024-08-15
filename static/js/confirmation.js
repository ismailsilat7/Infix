
function sendPostRequest() {
    const form = document.createElement("form");
    form.setAttribute("method", "post");
    const actionElement = document.querySelector(".action"); 

    if (actionElement && actionElement.textContent.trim() === "Delete") {
        form.setAttribute("action", "/delete-confirmation");
    } 
    else if (actionElement && actionElement.textContent.trim() === "Reset") {
        form.setAttribute("action", "/reset-confirmation");
    }

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "key");
    hiddenField.setAttribute("value", "value");
    form.appendChild(hiddenField);

    document.body.appendChild(form);
    form.submit();
}
