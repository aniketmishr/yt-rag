
# YouTube RAG Assistant

<p align="center">
  <img src="icons\icon128.PNG" alt="YouTube RAG Assistant Logo" width="100"/>
</p>

**YouTube RAG Assistant** is a Chrome extension that lets you **chat with any YouTube video**. It uses **Retrieval-Augmented Generation (RAG)** to understand the transcript of the video and answer your questions or summarize the content — right inside your browser.

---

## 🔧 Tech Stack

* **Frontend**: HTML, CSS, JavaScript (Chrome Extension)
* **Backend**: FastAPI + LangChain (Python)
* **AI**: Gemini API (via LangChain)
* **Transcription & Embedding**: YouTube transcripts are retrieved, embedded, and queried using a vector store.

---

## 🚀 Features

* Chat with any YouTube video (except Shorts)
* Summarize video content
* Ask follow-up or in-depth questions about the video
* Fast, context-aware responses powered by LangChain + RAG

---

## 🧠 What is RAG?

RAG (Retrieval-Augmented Generation) is an architecture that improves large language models by allowing them to “look up” relevant external information before answering. In this app, the transcript of the YouTube video is embedded and stored. When you ask a question, the most relevant parts of the transcript are retrieved and passed to the language model for a more accurate response.

Read more in my blog post: [RAG Explained Simply]()

---

## 🛠️ How to Run the App Locally

### 1. Clone the repository

```bash
git clone https://github.com/aniketmishr/yt-rag
cd backend  
```

### 2. Set up the backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

This will start your FastAPI server at `http://localhost:8000`

### 3. Set up the Chrome Extension

1. Open **Google Chrome**.
2. Go to `chrome://extensions/`.
3. Enable **Developer Mode** (top-right toggle).
4. Click **"Load unpacked"**.
5. Select the extension's folder (where your manifest.json is located).

---

## ✅ Usage

1. Open any YouTube video (non-Shorts).
2. Click the **YouTube RAG Assistant** icon in your extensions bar.
3. Start chatting — ask for a summary or dive into specific topics discussed in the video.

---

## 📌 Notes

* Make sure the video has captions or a transcript available.
* Backend must be running locally for the extension to function (unless deployed).

---
