export default function login(){
    const loginButton = document.querySelector('.button-start-sesion')

    if(loginButton){
        loginButton.addEventListener('click', function(){
            
            const formLogin = document.querySelector('.form-login')
            formLogin.submit()
        })
    }
    return
}

export function register(){
    console.log('feo')
    const registerButton = document.querySelector('.box-button-submit')
    console.log(registerButton)
    
    if(registerButton){
        registerButton.onclick = function(){
            const formRegister = document.querySelector('.form-register')
            console.log(formRegister)
            formRegister.submit()
        }
    }

}
