let autoScanEnabled = false;

// Load user permission from storage
chrome.storage.local.get(['autoScanEnabled'], (result) => {
  autoScanEnabled = result.autoScanEnabled || false;
  if (autoScanEnabled) {
    scanExisting();
  }
});

// Listen for toggle changes from popup
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (changes.autoScanEnabled) {
    autoScanEnabled = changes.autoScanEnabled.newValue;
    if (autoScanEnabled) {
      scanExisting();
    }
  }
});

function scanExisting() {
  // Gmail message body selectors
  const emails = document.querySelectorAll('.a3s:not([data-spam-prompted]), .ii.gt:not([data-spam-prompted])');
  emails.forEach(promptEmail);
}

function promptEmail(emailElement) {
  if (!autoScanEnabled) return;
  if (emailElement.dataset.spamPrompted) return;
  
  const text = emailElement.innerText.trim();
  if (text.length < 15) return; // Ignore tiny UI snippets

  // Mark as prompted to prevent infinite loops
  emailElement.dataset.spamPrompted = "true";

  // Create Prompt UI
  const promptBox = document.createElement('div');
  promptBox.className = "spamguard-prompt";
  
  const textSpan = document.createElement('div');
  textSpan.className = "sg-prompt-text";
  textSpan.innerHTML = `🛡️ <strong>SpamGuard:</strong> New email detected. Would you like to analyze it for spam?`;
  
  const scanBtn = document.createElement('button');
  scanBtn.className = "sg-btn-scan";
  scanBtn.innerText = "Scan Email";

  const ignoreBtn = document.createElement('button');
  ignoreBtn.className = "sg-btn-ignore";
  ignoreBtn.innerText = "Ignore";

  promptBox.appendChild(textSpan);
  promptBox.appendChild(ignoreBtn);
  promptBox.appendChild(scanBtn);

  // Attempt to place it at the top of the specific email message block
  const container = emailElement.closest('.h7') || emailElement.closest('.nH.hx') || emailElement; 
  
  // Prevent duplicate prompts in the exact same container!
  if (container.dataset.hasSpamPrompt === "true") return;
  container.dataset.hasSpamPrompt = "true";

  container.insertBefore(promptBox, container.firstChild);

  // Ignore Logic
  ignoreBtn.addEventListener('click', () => {
    promptBox.remove();
  });

  // Scan Logic
  scanBtn.addEventListener('click', () => {
    scanBtn.innerText = "Analyzing...";
    scanBtn.disabled = true;
    ignoreBtn.style.display = "none";

    // Send to background to process via API
    chrome.runtime.sendMessage({ action: "scan_text", text: text }, (response) => {
      if (chrome.runtime.lastError) {
        textSpan.innerHTML = `❌ Error: Could not connect to SpamGuard backend. Make sure the server is running.`;
        scanBtn.remove();
        return;
      }

      if (response && response.status === "success") {
        promptBox.innerHTML = ""; // Clear buttons
        
        if (response.is_spam) {
          promptBox.className = "spamguard-warning";
          promptBox.innerHTML = `🚫 <strong>SpamGuard Protection:</strong> This email was flagged as SPAM (${response.confidence}% confidence). Proceed with caution.`;
          // Highlight the email background lightly
          emailElement.style.backgroundColor = "rgba(239, 68, 68, 0.05)";
        } else {
          promptBox.className = "spamguard-success";
          promptBox.innerHTML = `✅ <strong>SpamGuard:</strong> This email looks clean (${response.confidence}% confidence).`;
        }
      } else {
        textSpan.innerHTML = `❌ Error: Failed to analyze.`;
        scanBtn.remove();
      }
    });
  });
}

// Observe Gmail DOM for newly opened emails
const observer = new MutationObserver((mutations) => {
  if (!autoScanEnabled) return;
  
  let shouldScan = false;
  for (const mutation of mutations) {
    if (mutation.addedNodes.length > 0) {
      shouldScan = true;
      break;
    }
  }
  
  // If nodes were added, scan the DOM for new unscanned emails
  if (shouldScan) {
    scanExisting();
  }
});

// Start observing the body for changes
observer.observe(document.body, { childList: true, subtree: true });
