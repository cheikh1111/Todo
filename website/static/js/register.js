document.addEventListener('DOMContentLoaded', () => {
    let passwordDivs = document.getElementsByClassName('password');
    
    for (passwordDiv of passwordDivs) {
        let passwordInput = passwordDiv.querySelector('input');
        let viewSpan = passwordDiv.querySelector('span')

        viewSpan.addEventListener('click' ,() => {
            if (passwordInput.type === 'text') {
                passwordInput.type = 'password';
                viewSpan.innerText = 'show'
            } else {
                passwordInput.type = 'text';
                viewSpan.innerText= 'hide'
            }
        });



    passwordInput.addEventListener('focus',() => {
        passwordDiv.style.border = '2px solid rgb(17,17,17)'
    });


    passwordInput.addEventListener('blur',() => {
        passwordDiv.style.border = '2px solid rgb(100, 95, 95)'
    });

}})