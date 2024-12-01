import os
import threading
import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests


def check_ffmpeg():
    """Check if FFMPEG is available."""
    ffmpeg_path = 'C:\\Program Files\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'
    if not os.path.exists(ffmpeg_path):
        messagebox.showerror("FFMPEG Missing", "FFMPEG not found. Please install FFMPEG and set the correct path.")
        return False
    return True


def check_internet_connection():
    """Check for internet connection."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def get_available_qualities(url):
    """Fetch available video qualities for a given URL."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            qualities = sorted({f['height'] for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none'})
            return [f"{q}p" for q in qualities]
    except Exception as e:
        print(f"Error fetching qualities: {e}")
        return []


def format_selector(ctx):
    """Select the best video and audio based on selected quality."""
    formats = ctx.get('formats')[::-1]

    selected_quality = video_quality.get()
    height = int(selected_quality.replace("p", ""))

    best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none' and f['height'] == height)
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext)

    return [{
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }]


def validate_and_update_status(event=None):
    """Validate input URL and update status when the input changes."""
    url = url_entry.get().strip()

    if not url:
        status_label.config(text="URL field is empty. Please enter a URL.", fg="red")
    else:
        status_label.config(text="Checking URL...", fg="orange")
        root.update_idletasks()
        validate_and_update_qualities()


def validate_and_update_qualities():
    """Validate URL and update the dropdown with available qualities."""
    url = url_entry.get().strip()

    if not url.startswith("http") or "youtube.com" not in url and "youtu.be" not in url:
        status_label.config(text="Invalid URL. Please enter a valid YouTube link.", fg="red")
        quality_dropdown['values'] = []
        quality_dropdown.set("")
        return

    qualities = get_available_qualities(url)
    if qualities:
        quality_dropdown['values'] = qualities
        quality_dropdown.set(qualities[-1])  # Default to the lowest quality
        status_label.config(text="Qualities updated. Ready to download.", fg="green")
    else:
        quality_dropdown['values'] = []
        quality_dropdown.set("")
        status_label.config(text="No qualities available for this URL.", fg="red")


def download_video(url, destination_folder, progress_callback=None, completion_callback=None):
    if not check_ffmpeg():
        return

    if not check_internet_connection():
        messagebox.showerror("No Internet", "No internet connection. Please check your connection and try again.")
        return

    os.makedirs(destination_folder, exist_ok=True)

    def my_hook(d):
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total_size > 0:
                progress = downloaded / total_size
                if progress_callback:
                    progress_callback(progress * 100)
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback(100)
            if completion_callback:
                completion_callback()

    ydl_opts = {
        'ffmpeg_location': 'C:\\Program Files\\ffmpeg-master-latest-win64-gpl\\bin',
        'format': format_selector,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [my_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}", flush=True)
        if progress_callback:
            progress_callback(0)
        if completion_callback:
            completion_callback()
        messagebox.showerror("Error", f"Failed to download: {str(e)}")


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)


def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL!")
        return

    destination_folder = folder_var.get()
    if not os.path.isdir(destination_folder):
        messagebox.showerror("Folder Error", "Invalid folder selected. Please choose a valid folder.")
        return

    download_button.config(state=tk.DISABLED)
    download_thread = threading.Thread(
        target=download_video,
        args=(url, destination_folder, update_progress, download_complete)
    )
    download_thread.start()


def update_progress(progress):
    progress_var.set(progress)
    progress_label.config(text=f"Progress: {progress:.2f}%")
    root.update_idletasks()


def download_complete():
    url_entry.delete(0, tk.END)
    download_button.config(state=tk.NORMAL)
    msg = "Download Complete!"
    progress_label.config(text=msg)
    messagebox.showinfo("Download Complete", msg)


# Setup GUI
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Entry
url_label = tk.Label(root, text="Enter Video URL:")
url_label.pack(pady=5, anchor='w', padx=10)  # Anchor to left and add horizontal padding
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5, padx=10)
url_entry.bind("<KeyRelease>", validate_and_update_status)  # Bind event for real-time status update

# Status Label
status_label = tk.Label(root, text="Enter a URL to start.", fg="blue")
status_label.pack(pady=5, padx=10, anchor='w')  # Anchor to left and add horizontal padding

# Folder Selection
folder_label = tk.Label(root, text="Select Download Folder:")
folder_label.pack(pady=5, anchor='w', padx=10)  # Anchor to left and add horizontal padding
folder_var = tk.StringVar(value=os.getcwd())
folder_entry = tk.Entry(root, textvariable=folder_var, width=40)
folder_entry.pack(pady=5, padx=10, fill='x')
folder_button = tk.Button(root, text="Browse", command=select_folder)
folder_button.pack(pady=5, padx=10, fill='x')

# Video Quality Selection
quality_label = tk.Label(root, text="Select Video Quality:")
quality_label.pack(pady=5, anchor='w', padx=10)  # Anchor to left and add horizontal padding
video_quality = tk.StringVar(value="")
quality_dropdown = ttk.Combobox(root, textvariable=video_quality, state="readonly")
quality_dropdown.pack(pady=5, padx=10, fill='x')

# Download Button
download_button = tk.Button(root, text="Download Video", command=start_download)
download_button.pack(pady=20, padx=10, fill='x')

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=10, padx=10)

# Progress Label
progress_label = tk.Label(root, text="Progress: 0%")
progress_label.pack(pady=5, padx=10, anchor='w')

root.mainloop()
