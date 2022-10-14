const passwordShowBtn = document.querySelector(".form__password-show-btn"),
  passwordShowIcon = document.querySelector(".form__password-show-icon"),
  passwordInput = document.querySelector(".form__password");

passwordShowBtn.addEventListener("click", (_e) => {
  let passwordShowIconName = passwordShowIcon.getAttribute("name");

  if (passwordShowIconName == "eye-off-outline") {
    passwordShowIcon.setAttribute("name", "eye-outline");
    passwordInput.setAttribute("type", "text");
  } else {
    passwordShowIcon.setAttribute("name", "eye-off-outline");
    passwordInput.setAttribute("type", "password");
  }
});
