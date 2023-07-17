

const targetDiv = document.getElementsByClassName("message");
const btn = document.getElementsById("hide-btn");
btn.onclick = function () {
if (targetDiv.style.display == "none") {
    targetDiv.style.display = "block";
} else {
    targetDiv.style.display = "none";
}
};