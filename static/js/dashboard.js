const infixLogo = document.querySelector('.logo-dash');
infixLogo.addEventListener('click', () => {
  window.location.href = '/'
})

// Set the exam date (e.g., December 1, 2024, at 9:00 AM)
var examDate = new Date("September 29, 2024 00:00:00").getTime();

// Update the countdown every second
var countdownFunction = setInterval(function() {
    var now = new Date().getTime();
    var timeDifference = examDate - now;

    // Calculate days, hours, minutes, and seconds
    var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    // Display the result in the respective countdown elements
    document.getElementById("days").innerHTML = days;
    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;

    // If the countdown is over, stop the timer and display "Exam time!"
    if (timeDifference < 0) {
        clearInterval(countdownFunction);
        document.getElementById("days").innerHTML = "0";
        document.getElementById("hours").innerHTML = "0";
        document.getElementById("minutes").innerHTML = "0";
        document.getElementById("seconds").innerHTML = "0";
    }
}, 1000);