import tkinter as tk
from tkinter import scrolledtext
import threading
import sounddevice as sd
import numpy as np
import whisper
import queue
import os
import datetime
import pyperclip  # For clipboard functionality

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        master.title("Microphone to Text App")
        
        self.canvas = tk.Canvas(master, width=300, height=100, bg='black')
        self.canvas.pack(pady=10)
        
        self.status_label = tk.Label(master, text="Ready to record")
        self.status_label.pack(pady=10)
        
        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_button.pack(pady=5)
        
        self.clear_button = tk.Button(master, text="Clear Text", command=self.clear_text)
        self.clear_button.pack(pady=5)
        
        self.transcription_text = scrolledtext.ScrolledText(master, width=60, height=20, wrap=tk.WORD)
        self.transcription_text.pack(pady=10)
        
        self.recording = False
        self.audio_queue = queue.Queue()
        self.model = whisper.load_model("large")
        self.samplerate = 16000  # Whisper expects 16kHz
        self.channels = 1
        self.audio_data = []
        self.audio_buffer = np.array([])
        self.buffer_size = 1600  # About 0.1 seconds of audio for visualization
        self.latest_transcription = ""
        self.scope_line = None

    def start_recording(self):
        self.status_label.config(text="Recording...")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.copy_button.config(state=tk.DISABLED)
        self.recording = True
        self.audio_data = []
        self.audio_buffer = np.array([])
        self.canvas.delete('all')
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()
        self.update_scope()

    def record_audio(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_queue.put(indata.copy())
            current_data = indata.flatten().astype(np.float32)
            self.audio_buffer = np.concatenate((self.audio_buffer, current_data))[-self.buffer_size:]

        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback):
            while self.recording:
                self.audio_data.append(self.audio_queue.get())

    def stop_recording(self):
        self.recording = False
        self.recording_thread.join()
        self.status_label.config(text="Transcribing...")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.audio_buffer = np.array([])
        self.canvas.delete('all')
        
        # Process the audio
        audio_array = np.concatenate(self.audio_data, axis=0).flatten().astype(np.float32)
        
        # Transcribe
        threading.Thread(target=self.transcribe_audio, args=(audio_array,)).start()

    def transcribe_audio(self, audio_array):
        result = self.model.transcribe(audio_array, language="en")
        transcription = result["text"]
        
        self.master.after(0, self.update_transcription, transcription)

    def update_transcription(self, text):
        self.transcription_text.insert(tk.END, text + "\n\n")
        self.status_label.config(text="Ready to record")
        self.latest_transcription = text
        self.copy_button.config(state=tk.NORMAL)
        
        # Automatically save to file
        self.save_to_file(text)

    def save_to_file(self, text):
        directory = "textwhisper"
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(directory, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved transcription to {filename}")

    def copy_to_clipboard(self):
        pyperclip.copy(self.latest_transcription)
        self.status_label.config(text="Copied to clipboard!")

    def clear_text(self):
        self.transcription_text.delete('1.0', tk.END)
        self.latest_transcription = ""
        self.copy_button.config(state=tk.DISABLED)

    def update_scope(self):
        if self.recording:
            if len(self.audio_buffer) > 0:
                height = 100
                mid = height / 2
                width = 300
                num_points = len(self.audio_buffer)
                if num_points > 0:
                    step = width / (num_points - 1) if num_points > 1 else width
                    points = []
                    for i, val in enumerate(self.audio_buffer):
                        x = i * step
                        # Scale val (-1 to 1) to height
                        y = mid - (val * mid)
                        points.append(x)
                        points.append(y)
                    if self.scope_line:
                        self.canvas.delete(self.scope_line)
                    self.scope_line = self.canvas.create_line(points, fill='green', width=2)
            self.master.after(100, self.update_scope)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()
