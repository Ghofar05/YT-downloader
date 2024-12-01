



# YouTube Video Downloader Script

This script creates a YouTube video downloader using `yt_dlp`, `tkinter`, and other Python libraries. Below is a brief explanation of its features and functionality:

## Features
1. **FFMPEG Check**  
   Ensures FFMPEG is installed and available at the specified path for video merging.

2. **Internet Connection Validation**  
   Checks for an active internet connection to proceed with video downloads.

3. **URL Validation**  
   Validates the provided YouTube URL and ensures it is correctly formatted.

4. **Fetch Video Qualities**  
   Retrieves available video qualities (e.g., `720p`, `1080p`) using `yt_dlp`.

5. **Custom Format Selection**  
   Downloads both video and audio streams based on user-selected quality and merges them into a single file.

6. **Progress Updates**  
   Provides real-time updates on download progress using a progress bar and a percentage label.

7. **GUI with `tkinter`**  
   User-friendly graphical interface for URL input, folder selection, video quality choice, and download initiation.

## Usage Instructions
1. Ensure **FFMPEG** is installed and the correct path is set in the `check_ffmpeg` function.
2. Run the script. A GUI window will appear.
3. Enter a valid YouTube URL.
4. Choose a folder for download or use the default directory.
5. Select the desired video quality from the dropdown list.
6. Click "Download Video" to start the process.

## Key Components
### **Functions**
- `check_ffmpeg()`  
  Validates FFMPEG installation.
- `check_internet_connection()`  
  Checks for internet connectivity.
- `get_available_qualities(url)`  
  Retrieves a list of video qualities for the given URL.
- `format_selector(ctx)`  
  Selects the best audio and video formats for merging.
- `download_video(url, destination_folder, progress_callback, completion_callback)`  
  Handles video and audio download and merging.
- `validate_and_update_status()`  
  Updates the status label dynamically based on URL validation.

### **GUI Elements**
- **URL Input Field**: Allows users to enter the YouTube video URL.
- **Folder Selection**: Enables users to choose where to save the downloaded video.
- **Quality Dropdown**: Lists available video resolutions for selection.
- **Progress Bar**: Displays download progress in real-time.

## Requirements
- Python 3.x
- Libraries:  
  Install required libraries using `pip install yt_dlp requests tkinter`.

## Notes
- Update the FFMPEG path as needed in the script.
- The script supports YouTube URLs but can be extended for other platforms supported by `yt_dlp`.