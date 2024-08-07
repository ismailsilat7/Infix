var copy = document.querySelector(".logos-slide").cloneNode(true)
document.querySelector('.logos').appendChild(copy)

function checkSection() {
  var navbar = document.getElementById('navbar');
  var introSection = document.getElementById('intro-section');
  var introRect = introSection.getBoundingClientRect();
  if (introRect.top <= window.innerHeight && introRect.bottom >= 0) {
    navbar.style.display = 'none';
  } else {
    navbar.style.display = 'block';
  }
}
window.addEventListener('load', checkSection);
window.addEventListener('scroll', checkSection);