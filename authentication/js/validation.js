// validation.js - Centralized validation rules for MSRTC Auth

const ValidationRules = {
  // Mobile: Exactly 10 digits
  mobile: {
    regex: /^[0-9]{10}$/,
    message: "Mobile number must be exactly 10 digits"
  },
  // Email: Standard email format
  email: {
    regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: "Please enter a valid email address"
  },
  // Password: Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
  password: {
    regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
    message: "Password must be min 8 chars with uppercase, lowercase, number, and special character"
  }
};

/**
 * Validates an input element based on a rule type.
 * @param {HTMLInputElement} inputEl 
 * @param {string} ruleType - 'mobile', 'email', 'password'
 * @returns {boolean} isValid
 */
function validateInput(inputEl, ruleType) {
  const rule = ValidationRules[ruleType];
  if (!rule) return true; // No rule defined

  const value = inputEl.value.trim();
  const isValid = rule.regex.test(value);
  
  updateInputUI(inputEl, isValid, rule.message);
  return isValid;
}

/**
 * Validates if two password fields match.
 * @param {HTMLInputElement} passEl 
 * @param {HTMLInputElement} confirmPassEl 
 * @returns {boolean} isValid
 */
function validateConfirmPassword(passEl, confirmPassEl) {
  const isValid = passEl.value === confirmPassEl.value && confirmPassEl.value !== '';
  updateInputUI(confirmPassEl, isValid, "Passwords do not match");
  return isValid;
}

/**
 * Validates if a required field is not empty.
 * @param {HTMLInputElement} inputEl 
 * @returns {boolean} isValid
 */
function validateRequired(inputEl) {
  const isValid = inputEl.value.trim().length > 0;
  updateInputUI(inputEl, isValid, "This field is required");
  return isValid;
}

/**
 * Updates the UI of an input field based on validity.
 */
function updateInputUI(inputEl, isValid, errorMessage) {
  // Find or create error text element
  let errorEl = inputEl.parentElement.querySelector('.error-text');
  
  if (isValid) {
    inputEl.classList.remove('is-invalid');
    inputEl.classList.add('is-valid');
    if (errorEl) {
      errorEl.style.display = 'none';
    }
  } else {
    inputEl.classList.remove('is-valid');
    inputEl.classList.add('is-invalid');
    
    if (!errorEl) {
      errorEl = document.createElement('div');
      errorEl.className = 'error-text';
      inputEl.parentElement.appendChild(errorEl);
    }
    errorEl.textContent = errorMessage;
    errorEl.style.display = 'block';
  }
}

// Export for usage if using modules, but since it's standard JS included via script tags, it's global.
