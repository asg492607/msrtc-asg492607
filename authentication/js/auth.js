// auth.js - Core UI interactions for authentication module

document.addEventListener('DOMContentLoaded', () => {
  initPasswordToggles();
  initOTPInputs();
  initForms();
  
  // If we are on OTP page, start timer
  if (document.getElementById('otpTimer')) {
    startOTPTimer();
  }
});

/**
 * Toast Notification System
 */
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✅' : '❌'}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  // Remove toast after animation (3.3s total)
  setTimeout(() => {
    toast.remove();
  }, 3500);
}

/**
 * Password Show/Hide Toggle
 */
function initPasswordToggles() {
  const toggles = document.querySelectorAll('.toggle-password');
  toggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const input = this.parentElement.querySelector('input');
      if (input.type === 'password') {
        input.type = 'text';
        this.textContent = '👁️';
      } else {
        input.type = 'password';
        this.textContent = '👁️‍🗨️';
      }
    });
  });
}

/**
 * Loading Spinner Simulation
 */
function simulateLoading(btn, callback) {
  btn.classList.add('loading');
  btn.disabled = true;
  
  setTimeout(() => {
    btn.classList.remove('loading');
    btn.disabled = false;
    callback();
  }, 1000);
}

/**
 * OTP Inputs Auto-Focus and Next
 */
function initOTPInputs() {
  const otpInputs = document.querySelectorAll('.otp-input');
  if (otpInputs.length === 0) return;

  // Auto focus first input
  otpInputs[0].focus();

  otpInputs.forEach((input, index) => {
    input.addEventListener('input', function() {
      // Ensure only numbers are entered
      this.value = this.value.replace(/[^0-9]/g, '');
      
      if (this.value.length === 1) {
        if (index < otpInputs.length - 1) {
          otpInputs[index + 1].focus();
        }
      }
    });

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Backspace' && this.value === '') {
        if (index > 0) {
          otpInputs[index - 1].focus();
        }
      }
    });
  });
}

/**
 * OTP Timer
 */
let otpInterval;
function startOTPTimer() {
  const timerSpan = document.getElementById('otpTimer');
  let timeLeft = 59; // 59 seconds

  clearInterval(otpInterval);
  
  otpInterval = setInterval(() => {
    if (timeLeft <= 0) {
      clearInterval(otpInterval);
      timerSpan.textContent = '00:00';
      timerSpan.parentElement.innerHTML = 'Didn\'t receive code? <a href="#" onclick="resendOTP(event)">Resend OTP</a>';
    } else {
      const seconds = timeLeft < 10 ? '0' + timeLeft : timeLeft;
      timerSpan.textContent = `00:${seconds}`;
      timeLeft--;
    }
  }, 1000);
}

function resendOTP(e) {
  e.preventDefault();
  showToast("OTP Resent successfully", "success");
  
  const timerContainer = e.target.parentElement;
  timerContainer.innerHTML = 'Resend OTP in <span id="otpTimer">00:59</span>';
  startOTPTimer();
}

/**
 * Form Submission Handling & Dummy Routing
 */
function initForms() {
  // Login Form
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const mobileInput = document.getElementById('loginMobile');
      const passInput = document.getElementById('loginPassword');
      
      const isMobileValid = validateInput(mobileInput, 'mobile');
      const isPassValid = validateRequired(passInput);

      if (isMobileValid && isPassValid) {
        const btn = loginForm.querySelector('.btn-primary');
        simulateLoading(btn, () => {
          showToast("Login Successful! Redirecting...", "success");
          setTimeout(() => window.location.href = 'otp-verification.html', 1000);
        });
      } else {
        showToast("Please check your credentials", "error");
      }
    });
  }

  // Signup Form
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const name = document.getElementById('regName');
      const mobile = document.getElementById('regMobile');
      const email = document.getElementById('regEmail');
      const pass = document.getElementById('regPassword');
      const confirmPass = document.getElementById('regConfirm');
      const terms = document.getElementById('terms');

      let isValid = true;
      if (!validateRequired(name)) isValid = false;
      if (!validateInput(mobile, 'mobile')) isValid = false;
      if (!validateInput(email, 'email')) isValid = false;
      if (!validateInput(pass, 'password')) isValid = false;
      if (!validateConfirmPassword(pass, confirmPass)) isValid = false;

      if (!terms.checked) {
        showToast("Please accept Terms & Conditions", "error");
        isValid = false;
      }

      if (isValid) {
        const btn = signupForm.querySelector('.btn-primary');
        simulateLoading(btn, () => {
          showToast("Account Created! Sending OTP...", "success");
          setTimeout(() => window.location.href = 'otp-verification.html', 1000);
        });
      }
    });
  }

  // Forgot Password Form
  const forgotForm = document.getElementById('forgotForm');
  if (forgotForm) {
    forgotForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const mobileInput = document.getElementById('forgotMobile');
      
      if (validateInput(mobileInput, 'mobile')) {
        const btn = forgotForm.querySelector('.btn-primary');
        simulateLoading(btn, () => {
          showToast("OTP sent for password reset", "success");
          setTimeout(() => window.location.href = 'otp-verification.html?mode=reset', 1000);
        });
      }
    });
  }

  // OTP Verification Form
  const otpForm = document.getElementById('otpForm');
  if (otpForm) {
    otpForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Check if all inputs are filled
      const inputs = document.querySelectorAll('.otp-input');
      let otpCode = '';
      let isComplete = true;
      
      inputs.forEach(input => {
        if (!input.value) {
          isComplete = false;
          input.classList.add('is-invalid');
        } else {
          input.classList.remove('is-invalid');
          otpCode += input.value;
        }
      });

      if (isComplete && otpCode.length === 6) {
        const btn = otpForm.querySelector('.btn-primary');
        simulateLoading(btn, () => {
          // Check query param for redirect target
          const urlParams = new URLSearchParams(window.location.search);
          const mode = urlParams.get('mode');
          
          if (mode === 'reset') {
            showToast("OTP Verified! Proceed to reset password", "success");
            setTimeout(() => window.location.href = 'reset-password.html', 1000);
          } else {
            showToast("OTP Verified! Welcome to MSRTC", "success");
            setTimeout(() => window.location.href = '../dashboard.html', 1000);
          }
        });
      } else {
        showToast("Please enter complete 6-digit OTP", "error");
      }
    });
  }

  // Reset Password Form
  const resetForm = document.getElementById('resetForm');
  if (resetForm) {
    resetForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const pass = document.getElementById('resetPass');
      const confirmPass = document.getElementById('resetConfirm');

      let isValid = true;
      if (!validateInput(pass, 'password')) isValid = false;
      if (!validateConfirmPassword(pass, confirmPass)) isValid = false;

      if (isValid) {
        const btn = resetForm.querySelector('.btn-primary');
        simulateLoading(btn, () => {
          showToast("Password Reset Successful! Login now.", "success");
          setTimeout(() => window.location.href = 'login.html', 1500);
        });
      }
    });
  }
}

// Global UI helper for dummy OTP login click
window.triggerOTPLogin = function(e) {
  e.preventDefault();
  const mobileInput = document.getElementById('loginMobile');
  if (validateInput(mobileInput, 'mobile')) {
    const btn = e.target;
    btn.innerHTML = `<div class="spinner"></div> Sending OTP...`;
    setTimeout(() => {
      window.location.href = 'otp-verification.html';
    }, 1000);
  } else {
    showToast("Please enter a valid mobile number for OTP login", "error");
  }
}
