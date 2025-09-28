document.getElementById("checkBtn").addEventListener("click", () => {
  let text = document.getElementById("inputText").value;
  
  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerText = 
      "Risk Score: " + data.score + "\nBullying: " + data.is_bullying;
  });
});
