chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scan_text") {
    fetch("http://127.0.0.1:8000/api/detect/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: request.text })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        if (data.is_spam) {
           // Create Notification
           chrome.notifications.create({
             type: 'basic',
             iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==', // 1x1 red pixel fallback
             title: '🛡️ SpamGuard Alert',
             message: `Warning! Spam detected in your Gmail with ${data.confidence}% confidence.`,
             priority: 2
           });
        }
        sendResponse(data);
      } else {
        sendResponse({ error: true });
      }
    })
    .catch(err => {
      console.error("SpamGuard API Error:", err);
      sendResponse({ error: true });
    });
    return true; // Keep message channel open for async fetch
  }
});
