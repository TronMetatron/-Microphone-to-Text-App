# 🎙️ Microphone to Text App

**Microphone to Text App** is a simple desktop application built with **Python** and **Tkinter** that records audio from your microphone, transcribes it into text using [OpenAI Whisper](https://github.com/openai/whisper), and provides convenient options to save and copy the transcription.

The app is ideal for quick note-taking, meeting transcription, or speech-to-text workflows — all from your local machine.

---

## ✨ Features
- 🎤 **Live Microphone Recording** – Capture audio directly from your system microphone.
- 📝 **Accurate Transcription** – Uses the Whisper **large** model for high-accuracy speech-to-text.
- 💾 **Automatic Saving** – Transcriptions are saved as timestamped `.txt` files in a `textwhisper` folder.
- 📋 **Clipboard Copy** – Instantly copy transcribed text to your clipboard.
- 🖥 **Simple GUI** – User-friendly interface powered by Tkinter.

---

## 📦 Requirements

You will need:
- Python **3.9+**
- [OpenAI Whisper](https://github.com/openai/whisper)
- [sounddevice](https://pypi.org/project/sounddevice/)
- [numpy](https://numpy.org/)
- [pyperclip](https://pypi.org/project/pyperclip/)
- Tkinter (included in most Python installations)

---

## 🔧 Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/microphone-to-text-app.git
   cd microphone-to-text-app
