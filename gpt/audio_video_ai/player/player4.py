import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
import queue

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

        self.scroll_interval = 25  # Number of frames to skip for scrolling
        self.buffer_size = 300000  # Number of frames to store in the buffer
        self.video_buffer = queue.Queue(maxsize=self.buffer_size)
        self.frame_index = 0

        self.cap = cv2.VideoCapture(1)  # Replace '0' with the camera index if using an external camera

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        self.thread = threading.Thread(target=self.update_video)
        self.thread.daemon = True
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def update_video(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.video_buffer.full():
                    self.video_buffer.get()  # Remove the oldest frame from the buffer
                self.video_buffer.put(frame)  # Add the current frame to the buffer

                if self.frame_index == 0:
                    self.show_live_frame(frame)
                else:
                    self.show_buffer_frame(self.frame_index)

            self.root.update()  # Update the GUI to display the video frames

    def show_live_frame(self, frame):
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video_label.config(image=img)
        self.video_label.image = img

    def show_buffer_frame(self, index):
        if not self.video_buffer.empty():
            frame = self.video_buffer.queue[index % self.video_buffer.qsize()]
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.video_label.config(image=img)
            self.video_label.image = img

    def scroll_back(self):
        if self.frame_index < self.buffer_size - self.scroll_interval:
            self.frame_index += self.scroll_interval
            self.show_buffer_frame(self.frame_index)

    def scroll_forward(self):
        if self.frame_index >= self.scroll_interval:
            self.frame_index -= self.scroll_interval
            self.show_buffer_frame(self.frame_index)

    def close_app(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamingApp(root)
    root.mainloop()
