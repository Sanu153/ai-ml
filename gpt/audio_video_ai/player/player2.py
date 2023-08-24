import tkinter as tk
import cv2
from PIL import Image, ImageTk

class LiveStreamingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Streaming with Scroll")

        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(pady=10)

        self.scroll_frame = tk.Frame(self.root)
        self.scroll_frame.pack(pady=5)

        self.scroll_back_button = tk.Button(self.scroll_frame, text="Scroll Back", command=self.scroll_back)
        self.scroll_back_button.pack(side=tk.LEFT, padx=5)

        self.scroll_forward_button = tk.Button(self.scroll_frame, text="Scroll Forward", command=self.scroll_forward)
        self.scroll_forward_button.pack(side=tk.LEFT, padx=5)

        self.scroll_interval = 20  # Number of frames to skip for scrolling
        self.buffer_size = 100000  # Number of frames to store in the buffer
        self.video_buffer = []

        self.cap = cv2.VideoCapture(1)  # Replace '0' with the camera index if using an external camera

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        self.update_video()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.video_label.config(image=img)
            self.video_label.image = img

            if len(self.video_buffer) >= self.buffer_size:
                self.video_buffer.pop(0)  # Remove the oldest frame from the buffer
            self.video_buffer.append(frame)  # Add the current frame to the buffer

        self.root.after(30, self.update_video)

    def scroll_back(self):
        if len(self.video_buffer) > self.scroll_interval:
            self.video_buffer = self.video_buffer[:-self.scroll_interval]  # Remove frames from the end of the buffer
            self.show_buffer_frame(-1 * self.scroll_interval)

    def scroll_forward(self):
        if len(self.video_buffer) > self.scroll_interval:
            self.show_buffer_frame(self.scroll_interval)

    def show_buffer_frame(self, index):
        if -1 * index < len(self.video_buffer):
            frame = self.video_buffer[index]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.video_label.config(image=img)
            self.video_label.image = img

    def close_app(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamingApp(root)
    root.mainloop()
