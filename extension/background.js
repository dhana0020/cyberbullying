// background.js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "analyzeText") {
    fetch("http://127.0.0.1:5000/monitor", {   // Use your real backend endpoint
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "u123",                      // dummy user id (replace if needed)
        message: msg.data,                    // the text typed
        timestamp: new Date().toISOString()   // current time
      })
    })
    .then(res => res.json())
    .then(result => {
      console.log("Backend result:", result);

      // result looks like { "status": "processed", "risk_score": 0.82, "flagged": true }
      if (result.flagged) {
        chrome.scripting.executeScript({
          target: { tabId: sender.tab.id },
          func: (text, score) => {
            alert("⚠ Cyberbullying Detected!\nText: " + text + "\nRisk Score: " + score);
          },
          args: [msg.data, result.risk_score]
        });
      }
    })
    .catch(err => console.error("API error:", err));
  }
});
