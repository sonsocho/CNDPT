import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from PIL import Image, ImageTk
import os

class VideoCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compressor")
        self.root.geometry("800x500")  # Điều chỉnh kích thước cửa sổ
        self.root.configure(bg="white")

        self.selected_video = None
        self.compressed_videos = []  # Danh sách lưu các video đã nén

        # Tạo frame chứa các phím chức năng
        self.button_frame = tk.Frame(root, bg="white")
        self.button_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Các phím chức năng đặt theo hàng dọc
        button_width = 15
        button_height = 2
        button_font = ('Arial', 10, 'bold')
        button_bg = "#007BFF"  # Màu nền chung cho tất cả các nút

        self.btn_select_video = tk.Button(self.button_frame, text="Chọn Video", command=self.select_video,
                                          width=button_width, height=button_height, font=button_font,
                                          bg=button_bg, fg="white", relief="flat")
        self.btn_select_video.pack(pady=10)
        self.btn_select_video.bind("<Enter>", self.on_button_hover)
        self.btn_select_video.bind("<Leave>", self.on_button_leave)

        self.btn_compress_video = tk.Button(self.button_frame, text="Nén Video", command=self.compress_video,
                                           width=button_width, height=button_height, font=button_font,
                                           bg=button_bg, fg="white", relief="flat")
        self.btn_compress_video.pack(pady=10)
        self.btn_compress_video.bind("<Enter>", self.on_button_hover)
        self.btn_compress_video.bind("<Leave>", self.on_button_leave)

        self.btn_save_video = tk.Button(self.button_frame, text="Lưu Video Nén", command=self.save_video,
                                        width=button_width, height=button_height, font=button_font,
                                        bg=button_bg, fg="white", relief="flat")
        self.btn_save_video.pack(pady=10)
        self.btn_save_video.bind("<Enter>", self.on_button_hover)
        self.btn_save_video.bind("<Leave>", self.on_button_leave)

        # Tạo frame chứa hai phần thể hiện video và thông số
        self.video_frame = tk.Frame(root, bg="lightgray")
        self.video_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Canvas hiển thị video được chọn
        self.canvas_original = tk.Canvas(self.video_frame, width=320, height=240, bg="gray")
        self.canvas_original.grid(row=0, column=0, padx=10, pady=10)

        # Canvas hiển thị video sau khi nén
        self.canvas_compressed = tk.Canvas(self.video_frame, width=320, height=240, bg="gray")
        self.canvas_compressed.grid(row=0, column=1, padx=10, pady=10)

        # Thông số video được chọn
        self.label_original_info = tk.Label(self.video_frame, text="Thông số video gốc:", bg="lightgray")
        self.label_original_info.grid(row=1, column=0, padx=30, pady=5, sticky="w")

        self.label_original_size = tk.Label(self.video_frame, text="Kích thước: N/A", bg="lightgray")
        self.label_original_size.grid(row=2, column=0, padx=30, pady=5, sticky="w")

        # Thông số video sau khi nén
        self.label_compressed_info = tk.Label(self.video_frame, text="Thông số video sau khi nén:", bg="lightgray")
        self.label_compressed_info.grid(row=1, column=1, padx=30, pady=5, sticky="w")

        self.label_compressed_size = tk.Label(self.video_frame, text="Kích thước: N/A", bg="lightgray")
        self.label_compressed_size.grid(row=2, column=1, padx=30, pady=5, sticky="w")

        # Danh sách video đã nén
        self.listbox_compressed_videos = tk.Listbox(self.video_frame, width=40, height=6)
        self.listbox_compressed_videos.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Căn chỉnh tự động
        self.video_frame.grid_rowconfigure(3, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(1, weight=1)

        # Thiết lập kích thước tự động cho phần chứa video
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(1, weight=1)

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if video_path:
            self.selected_video = video_path
            self.update_canvas(self.canvas_original, video_path)
            self.display_video_info(self.selected_video, "original")

    def update_canvas(self, canvas, video_path):
        clip = VideoFileClip(video_path)
        thumbnail_path = "thumbnail.jpg"
        clip.save_frame(thumbnail_path, t=0)

        image = Image.open(thumbnail_path)
        image = image.resize((320, 240), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo  # Giữ tham chiếu ảnh

    def compress_video(self):
        if not self.selected_video:
            messagebox.showwarning("Warning", "Bạn chưa chọn video nào.")
            return

        try:
            clip = VideoFileClip(self.selected_video)
            output_path = self.selected_video.rsplit(".", 1)[0] + "_compressed.mp4"
            clip.write_videofile(output_path, codec="libx264", bitrate="100k", audio_codec="aac")
            self.update_canvas(self.canvas_compressed, output_path)
            self.display_video_info(output_path, "compressed")
            self.add_to_compressed_list(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể nén video: {str(e)}")

    def add_to_compressed_list(self, video_path):
        self.compressed_videos.append(video_path)
        self.listbox_compressed_videos.insert(tk.END, os.path.basename(video_path))

    def save_video(self):
        selected_index = self.listbox_compressed_videos.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Bạn chưa chọn video nén nào để lưu.")
            return

        compressed_video_path = self.compressed_videos[selected_index[0]]
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], initialfile=os.path.basename(compressed_video_path))
        if save_path:
            try:
                clip = VideoFileClip(compressed_video_path)
                clip.write_videofile(save_path, codec="libx264", bitrate="100k", audio_codec="aac")
                messagebox.showinfo("Success", "Video đã được lưu thành công.")
            except Exception as e:
                messagebox.showerror("Error", f"Không thể lưu video: {str(e)}")

    def display_video_info(self, video_path, video_type):
        size = f"{os.path.getsize(video_path) / (1024 * 1024):.2f} MB"

        if video_type == "original":
            self.label_original_size.config(text=f"Kích thước: {size}")
        elif video_type == "compressed":
            self.label_compressed_size.config(text=f"Kích thước: {size}")

    def on_button_hover(self, event):
        event.widget.config(bg="#0056b3")  # Màu nền khi di chuột qua

    def on_button_leave(self, event):
        # Thay đổi màu nền về màu ban đầu
        event.widget.config(bg="#007BFF")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressorApp(root)
    root.mainloop()
