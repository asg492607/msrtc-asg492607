// js/validation.js

const valRules = {
  mobile: /^[0-9]{10}$/,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
};

function valRequired(input) {
  const isValid = input.value.trim().length > 0;
  updateUI(input, isValid, "Required");
  return isValid;
}

function valRegex(input, type, msg) {
  const isValid = valRules[type].test(input.value.trim());
  updateUI(input, isValid, msg);
  return isValid;
}

function valAge(input) {
  const age = parseInt(input.value);
  const isValid = !isNaN(age) && age >= 1 && age <= 120;
  updateUI(input, isValid, "Age must be 1-120");
  return isValid;
}

function updateUI(input, isValid, msg) {
  let err = input.parentElement.querySelector('.error-text');
  if (isValid) {
    input.classList.remove('is-invalid');
    if (err) err.style.display = 'none';
  } else {
    input.classList.add('is-invalid');
    if (!err) {
      err = document.createElement('div');
      err.className = 'error-text';
      input.parentElement.appendChild(err);
    }
    err.textContent = msg;
    err.style.display = 'block';
  }
}
