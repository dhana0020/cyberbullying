// content.js
document.addEventListener("input", async (e) => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") {
    const text = e.target.value;

    if (text.length > 5) { // Only check if long enough
      chrome.runtime.sendMessage({ action: "analyzeText", data: text });
    }
  }
});
// content.js
document.addEventListener("input", async (e) => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") {
    const text = e.target.value;

    if (text.length > 5) {
      console.log("📤 Sending text to background:", text);  // 👈 Debug log
      chrome.runtime.sendMessage({ action: "analyzeText", data: text });
    }
  }
});
