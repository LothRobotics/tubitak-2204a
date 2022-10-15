const passwordShowBtns = document.querySelectorAll(".form__password-show-btn"),
passwordShowIcons = document.querySelectorAll(".form__password-show-icon"),
passwordInputs = document.querySelectorAll(".form__password"),
passwordBoxes = document.querySelectorAll('.form__password-box')

passwordShowBtns.forEach((passwordShowBtn, index) => {
  passwordShowBtn. addEventListener("click", (_e) => {

    let passwordShowIcon = passwordShowIcons[index],
    passwordInput = passwordInputs[index]

    let passwordShowIconName = passwordShowIcon.getAttribute("name");
  
    if (passwordShowIconName == "eye-off-outline") {
      passwordShowIcon.setAttribute("name", "eye-outline");
      passwordInput.setAttribute("type", "text");
    } else {
      passwordShowIcon.setAttribute("name", "eye-off-outline");
      passwordInput.setAttribute("type", "password");
    }
  });
})

function formatPhoneNumber(value) {
  if (!value) return value;
  const phoneNumber = value.replace(/[^\d]/g, '');
  const phoneNumberLength = phoneNumber.length;
  if (phoneNumberLength < 4) return phoneNumber;
  if (phoneNumberLength < 7) {
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
  }
  return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(
    3,
    6
  )}-${phoneNumber.slice(6, 10)}`;
}

function phoneNumberFormatter() {
  let inputField = document.querySelector('.form__phonenumber');
  let formattedInputValue = formatPhoneNumber(inputField.value);

  inputField.value = formattedInputValue;
}