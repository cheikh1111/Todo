document.addEventListener('DOMContentLoaded' ,() => {
    let passwordDiv = document.querySelector('.password');
    let passwordInput = passwordDiv.querySelector('input');
    let viewSpan = passwordDiv.querySelector('span')


    viewSpan.onclick= () => {
        if (passwordInput.type === 'text') {
            passwordInput.type = 'password';
            viewSpan.innerText = 'show'
        } else {
            passwordInput.type = 'text';
            viewSpan.innerText= 'hide'
        }
    };



    passwordInput.addEventListener('focus',() => {
        passwordDiv.style.border = '2px solid rgb(17,17,17)'
    });


    passwordInput.addEventListener('blur',() => {
        passwordDiv.style.border = '2px solid rgb(100, 95, 95)'
    });
});