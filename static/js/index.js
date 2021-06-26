// modal
const signinButton = document.querySelector('#signin');
const signupButton = document.querySelector('#signup');
const modalsigninBg = document.querySelector('#signinbg');
const modalsignupBg = document.querySelector('#signupbg');
const closeButtonSignin = document.querySelector('#closesignin')
const closeButtonSignup = document.querySelector('#closesignup')
const modalsignin = document.querySelector('#modalsignin');
const modalsignup = document.querySelector('#modalsignup');

//dropdown

signinButton.addEventListener('click', () => {
  modalsignin.classList.add('is-active');
})

signupButton.addEventListener('click', () => {
  modalsignup.classList.add('is-active');
})

modalsigninBg.addEventListener('click', () => {
  modalsignin.classList.remove('is-active');
})

closeButtonSignin.addEventListener('click', () => {
	modalsignin.classList.remove('is-active');
})

modalsignupBg.addEventListener('click', () => {
  modalsignup.classList.remove('is-active');
})

closeButtonSignup.addEventListener('click', () => {
	modalsignup.classList.remove('is-active');
})
