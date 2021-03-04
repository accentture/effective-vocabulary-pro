export default function login(){
    const loginButton = document.querySelector('.button-start-sesion')

    if(loginButton){
        console.log(loginButton)
        loginButton.addEventListener('click', function(){

            const formLogin = document.querySelector('.form-login')
            formLogin.submit()
        })
    }
    return
}