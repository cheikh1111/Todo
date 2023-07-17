// This will used to hide flashed messages

document.addEventListener('DOMContentLoaded', function () {
  // Get all the span elements with the class name .hide
  var hideSpans = document.querySelectorAll('.hide-btn');

  // Add a click event listener to each span element
  hideSpans.forEach(function (hideSpan) {
      hideSpan.addEventListener('click', function () {
          // Find the parent div element of the clicked span
          var parentDiv = this.closest('.message');

          // Hide the parent div by adding a CSS class
          parentDiv.classList.add('hidden');
      });
  });
});


// This will be used to show and hide password in login/register routes

const button = document.querySelectorAll('.hide-btn');
button.addEventListener('click',function(){
  if (password.type = 'text') {
    password.type = 'password'
  } 
  else{
    password.type = 'text';
  };

});