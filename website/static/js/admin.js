let menu = document.querySelector('aside');
let menuIcon = document.querySelector('header span');

menuIcon.onclick = () => {
    console.log(menu.style.display)
    styles = getComputedStyle(menu)
    if (styles.getPropertyValue('display') === 'block'){
        menu.style.display = 'none'
    } else {
        menu.style.display = 'block'
    }
}