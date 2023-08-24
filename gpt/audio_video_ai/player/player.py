import os
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Video Player")

        self.video_path = None
        self.video_playing = False
        self.video_pause = True

        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_video, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.prev_button = tk.Button(self.root, text="Previous Frame", command=self.previous_frame, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(self.root, text="Next Frame", command=self.next_frame, state=tk.DISABLED)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.frame_index = 0

    def play_video(self):
        if self.video_pause:
            self.cap = cv2.VideoCapture('2.mp4')
            # self.cap = cv2.VideoCapture(1)
            self.video_playing = True
            self.video_pause = False
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.play()
        else:
            self.video_playing = True
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.play()

    def play(self):
        if self.video_playing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_label.config(image=img)
                self.video_label.image = img
                self.frame_index += 1
                self.root.after(30, self.play)
            else:
                self.video_playing = False
                self.cap.release()
                self.video_label.config(image="")
                self.play_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)

    def pause_video(self):
        self.video_playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def stop_video(self):
        self.video_playing = False
        self.video_pause = True
        self.video_stopped = True
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.cap.release()
    
    def previous_frame(self):
        if self.video_playing:
            self.frame_index -= 25  # Go back to the previous frame (subtract 2 to account for the frame increment in play())
            if self.frame_index < 0:
                self.frame_index = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)

    def next_frame(self):
        if self.video_playing:
            self.frame_index += 25
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)

    def close_app(self):
        self.video_playing = False
        if hasattr(self, 'cap'):
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    player.video_label = tk.Label(player.video_frame)
    player.video_label.pack()
    root.mainloop()
