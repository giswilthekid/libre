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

//upload file

document.addEventListener('DOMContentLoaded', () => {
  // 1. Display file name when select file
  let fileInputs = document.querySelectorAll('.file.has-name')
  for (let fileInput of fileInputs) {
    let input = fileInput.querySelector('.file-input')
    let name = fileInput.querySelector('.file-name')
    input.addEventListener('change', () => {
      let files = input.files
      if (files.length === 0) {
        name.innerText = 'No file selected'
      } else {
        name.innerText = files[0].name
      }
    })
  }

  // 2. Remove file name when form reset
  let forms = document.getElementsByTagName('form')
  for (let form of forms) {
    form.addEventListener('reset', () => {
      console.log('a')
      let names = form.querySelectorAll('.file-name')
      for (let name of names) {
        name.innerText = 'No file selected'
      }
    })
  }
})