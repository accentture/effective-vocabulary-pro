import login, { register } from './app-user.js'

function controlLogout(){
    const imageControl = document.querySelector('.image-control')
    const boxUserControl = document.querySelector('.user-control')
    const boxLogout = document.querySelector('.box-logout')

    if(boxUserControl){
        boxUserControl.onmouseout = () => boxLogout.style.visibility = 'hidden'
    }

    if(imageControl){
        imageControl.onclick = () => {
            boxLogout.style.visibility = 'visible'
            
            boxLogout.onmouseout = () => boxLogout.style.visibility = 'hidden'
            boxLogout.onmouseover  = () => boxLogout.style.visibility = 'visible'
            
        }
    }
    
}

window.onload = () => {
    login()
    console.log(register)
    register()
    controlLogout()
    
}