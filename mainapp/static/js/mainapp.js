import login from './app-user.js'

function controlLogout(){
    const imageControl = document.querySelector('.image-control')
    const boxUserControl = document.querySelector('.user-control')
    const boxLogout = document.querySelector('.box-logout')

    boxUserControl.onmouseout = () => boxLogout.style.visibility = 'hidden'

    imageControl.onclick = () => {
        boxLogout.style.visibility = 'visible'
        
        boxLogout.onmouseout = () => boxLogout.style.visibility = 'hidden'
        boxLogout.onmouseover  = () => boxLogout.style.visibility = 'visible'
        
    }
}

window.onload = () => {
    login()
    controlLogout()
    
}