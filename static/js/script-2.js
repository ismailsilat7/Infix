// eye icon toggle 
const pwdInput = document.getElementById('pwd')
const confirmpwdInput = document.getElementById('confirm-pwd')
const toggleBtnOne = document.getElementById('toggle-one')
const toggleBtnTwo = document.getElementById('toggle-two')

toggleBtnOne.addEventListener('click', ()=> {
  if (pwdInput.type === 'password') {
    pwdInput.type = 'text'
    toggleBtnOne.className = 'ri-eye-line'
  } else {
    pwdInput.type = 'password'
    toggleBtnOne.className = 'ri-eye-close-line'
  }
})

toggleBtnTwo.addEventListener('click', () => {
  if (confirmpwdInput.type === 'password') {
    confirmpwdInput.type = 'text'
    toggleBtnTwo.className = 'ri-eye-line'
  } else {
    confirmpwdInput.type = 'password'
    toggleBtnTwo.className = 'ri-eye-close-line'
  }
})


// handling disabled pwd 

pwdInput.addEventListener('input', () => {
  if (pwdInput.value.length > 0) {
    confirmpwdInput.disabled = false

  } else {
    confirmpwdInput.disabled = true
    confirmpwdInput.value = ""
  }
})