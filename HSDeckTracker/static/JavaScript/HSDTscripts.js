var modal = document.getElementById("deleteModal");
var btn = document.getElementById("deleteBtn");
var btnBack = document.getElementById("modalBackBtn");
var span = document.getElementsByClassName("close")[0];

// Button to open Delete Modal
btn.onclick = function() {
    modal.style.display = "block";
}

// Button to close Delete Modal
span.onclick = function() {
    modal.style.display = "none";
}

// Modal closes when clicking off of it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}