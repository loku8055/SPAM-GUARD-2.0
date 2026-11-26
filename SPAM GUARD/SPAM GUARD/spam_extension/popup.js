document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const messageInput = document.getElementById('messageInput');
  const resultBox = document.getElementById('resultBox');
  const verdict = document.getElementById('verdict');
  const confidence = document.getElementById('confidence');
  const errorBox = document.getElementById('errorBox');
  const loading = document.getElementById('loading');
  const autoScanToggle = document.getElementById('autoScanToggle');
  const extThemeToggle = document.getElementById('extThemeToggle');
  const sunIcon = extThemeToggle.querySelector('.sun-icon');
  const moonIcon = extThemeToggle.querySelector('.moon-icon');
  const root = document.documentElement;

  // Load user setting for Theme
  chrome.storage.local.get(['themeMode'], (result) => {
    const theme = result.themeMode || 'dark';
    if (theme === 'light') {
      root.classList.add('light-mode');
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    }
  });

  // Toggle theme
  extThemeToggle.addEventListener('click', () => {
    root.classList.toggle('light-mode');
    const isLight = root.classList.contains('light-mode');
    chrome.storage.local.set({ themeMode: isLight ? 'light' : 'dark' });
    
    if (isLight) {
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    } else {
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
    }
  });

  // Load user setting for Auto-Scan
  chrome.storage.local.get(['autoScanEnabled'], (result) => {
    autoScanToggle.checked = result.autoScanEnabled || false;
  });

  // Save user setting for Auto-Scan on change
  autoScanToggle.addEventListener('change', (e) => {
    chrome.storage.local.set({ autoScanEnabled: e.target.checked });
  });

  analyzeBtn.addEventListener('click', async () => {
    const text = messageInput.value.trim();
    
    // Hide previous results
    resultBox.classList.add('hidden');
    errorBox.classList.add('hidden');
    
    if (!text) {
      errorBox.textContent = "Please enter content to analyze.";
      errorBox.classList.remove('hidden');
      return;
    }

    // UI Loading state
    analyzeBtn.disabled = true;
    loading.classList.remove('hidden');

    try {
      // NOTE: Using port 8001 as specified during project setup
      const response = await fetch("http://127.0.0.1:8000/api/detect/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        // Show success result
        resultBox.className = `result-box ${data.is_spam ? 'spam' : 'ham'}`;
        verdict.textContent = data.is_spam ? "SPAM" : "CLEAN";
        confidence.textContent = `Probability: ${data.confidence}% Intelligence Score`;
        resultBox.classList.remove('hidden');
      } else {
        // Show API error
        errorBox.textContent = data.message || "An error occurred during analysis.";
        errorBox.classList.remove('hidden');
      }
    } catch (err) {
      // Show Network error
      errorBox.textContent = "Could not connect to SpamGuard AI. Verify server is running on http://127.0.0.1:8000.";
      errorBox.classList.remove('hidden');
    } finally {
      // Reset UI state
      analyzeBtn.disabled = false;
      loading.classList.add('hidden');
    }
  });
});
