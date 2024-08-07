// trusted logos
var copy = document.querySelector(".logos-slide").cloneNode(true)
document.querySelector('.logos').appendChild(copy)

// navbar hidden in intro
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

// intro buttons
document.querySelector('.log-in-btn').addEventListener('click', function() {
  window.location.href = '/login';
});
document.querySelector('.get-started-btn').addEventListener('click', function() {
  window.location.href = '/signup';
});