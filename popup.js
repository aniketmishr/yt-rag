document.addEventListener("DOMContentLoaded", async () => {
  const statusDiv = document.getElementById("status");
  const chatContainer = document.getElementById("chat-container");
  const form = document.getElementById("query-form");
  const input = document.getElementById("user-input");

  let videoId = null;
  let chatHistory = [];
  let busy = false;

  // Disable input while loading
  input.disabled = true;
  form.querySelector("button").disabled = true;

  // 🧠 Get current tab URL
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = new URL(tab.url);
  videoId = url.searchParams.get("v");

  if (!videoId) {
  statusDiv.innerHTML = `
    <div class="welcome">
      <img src="icons/icon128.png" alt="App Icon" class="welcome-icon" />
      <h3>🎬 Welcome to <strong>SmartAsk for YouTube</strong>!</h3>
      <p>This extension answers your questions using the transcript of any YouTube video you're watching.</p>
      <p>To get started, open your favorite video and click this extension again.</p>
    </div>
  `;
  form.style.display = "none";
  chatContainer.style.display = "none";
  return;
}

  // 🧠 Step 1: Index the video
  statusDiv.textContent = "Indexing video...";
  try {
    const indexUrl = `http://127.0.0.1:8000/index/${videoId}`;
    const res = await fetch(indexUrl, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Indexing failed");

    statusDiv.textContent = "Video indexed. Ask your questions!";
    input.disabled = false;
    form.querySelector("button").disabled = false;
  } catch (err) {
    statusDiv.textContent = "Failed to index video.";
    form.style.display = "none";
    return;
  }

  // 🧠 Step 2: Handle form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question || busy) return;

    appendChat("You", question);
    input.value = "";
    statusDiv.textContent = "Waiting for answer...";
    busy = true;
    input.disabled = true;
    form.querySelector("button").disabled = true;

    try {
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      const answer = data.answer || "No answer provided.";

      appendChat("Assistant", answer);
      statusDiv.textContent = "Ask another question!";
    } catch (err) {
      appendChat("Assistant", "Something went wrong.");
      statusDiv.textContent = "Try again.";
    }

    input.disabled = false;
    form.querySelector("button").disabled = false;
    busy = false;
  });

  function appendChat(sender, message) {
    chatHistory.push({ sender, message });

    const bubble = document.createElement("div");
    bubble.className = "chat-bubble " + sender.toLowerCase();
    bubble.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
});
