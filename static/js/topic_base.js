// Toggle the display of categories
function toggleCategory(category) {
    const formattedCategory = category.replace(/ /g, "_");
    const categoryElement = document.getElementById(formattedCategory);

    if (categoryElement.style.display === "none") {
        categoryElement.style.display = "block";
    } else {
        categoryElement.style.display = "none";
    }
}

// Populate the Table of Contents (ToC) dynamically
const tocContainer = document.getElementById('toc-main');
document.querySelectorAll('.toc-item').forEach((item, index) => {{
    const link = document.createElement('a');
    link.href = `#${item.id}`;
    link.textContent = item.querySelector('h2, h3').textContent;
    tocContainer.appendChild(link);
}});

window.onscroll = function() { toggleNavbar() };

function toggleNavbar() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.style.top = "-100px"; // Adjust the value based on the navbar height to hide it
    } else {
        navbar.style.top = "0";
    }
}



function submitBookmarkRequest() {
    document.getElementById('bookmark-request').submit();
}

