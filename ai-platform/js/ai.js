// ai.js

let responsesData = {};

document.addEventListener('DOMContentLoaded', () => {
  // Theme Switcher
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      themeBtn.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    });
  }

  // Load responses
  fetch('data/responses.json')
    .then(response => response.json())
    .then(data => { responsesData = data; })
    .catch(err => console.error("Error loading AI responses", err));

  // Chat Input Handling
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const chatContainer = document.getElementById('chatContainer');
  const voiceBtn = document.getElementById('voiceBtn');
  const recordingIndicator = document.getElementById('recordingIndicator');

  if (sendBtn && chatInput) {
    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleSend();
    });
  }

  if (voiceBtn) {
    let isRecording = false;
    voiceBtn.addEventListener('click', () => {
      isRecording = !isRecording;
      if (isRecording) {
        voiceBtn.style.color = '#EF4444';
        voiceBtn.style.background = 'rgba(239, 68, 68, 0.1)';
        recordingIndicator.style.display = 'flex';
      } else {
        voiceBtn.style.color = 'var(--text-light)';
        voiceBtn.style.background = 'none';
        recordingIndicator.style.display = 'none';
        chatInput.value = "Track Bus"; // Dummy voice transcription
      }
    });
  }

  // Quick Chips
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if(chatInput) {
        chatInput.value = chip.textContent;
        handleSend();
      }
    });
  });
});

function handleSend() {
  const input = document.getElementById('chatInput');
  const container = document.getElementById('chatContainer');
  const text = input.value.trim();
  
  if (!text) return;
  
  // Append User Message
  appendMessage(text, 'user');
  input.value = '';

  // Show Typing Indicator
  const typing = document.createElement('div');
  typing.className = 'typing';
  typing.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  container.appendChild(typing);
  container.scrollTop = container.scrollHeight;

  // Process AI Response (Dummy)
  setTimeout(() => {
    container.removeChild(typing);
    let reply = "I'm sorry, I didn't understand that. You can ask me about booking tickets, tracking buses, or checking refund status.";
    
    // Simple exact match logic for demo
    const lowerText = text.toLowerCase();
    for (const key in responsesData) {
      if (lowerText.includes(key)) {
        reply = responsesData[key];
        break;
      }
    }
    
    appendMessage(reply, 'ai');
  }, 1500);
}

function appendMessage(text, sender) {
  const container = document.getElementById('chatContainer');
  const wrapper = document.createElement('div');
  wrapper.className = `message-wrapper ${sender}`;
  
  const msg = document.createElement('div');
  msg.className = `message ${sender}`;
  msg.textContent = text;
  
  wrapper.appendChild(msg);

  if (sender === 'ai') {
    const meta = document.createElement('div');
    meta.className = 'message-meta';
    meta.innerHTML = `
      <div class="msg-actions">
        <button title="Copy">📋</button>
        <button title="Helpful">👍</button>
        <button title="Not Helpful">👎</button>
      </div>
    `;
    wrapper.appendChild(meta);
  }

  container.appendChild(wrapper);
  container.scrollTop = container.scrollHeight;
}
