# **VIU Downloader**

A Python-based tool for downloading content from the **VIU platform**, complete with subtitle support and video merging capabilities. The tool allows users to download HLS streams and seamlessly embed subtitles into the downloaded videos.

---

## **Features**
- 🚀 **VIU Content Downloader**: Fetch and download videos from VIU using HLS stream links.
- 🎥 **Subtitle Support**: Automatically downloads subtitles (e.g., `.srt` files) alongside videos.
- 🛠️ **Video & Subtitle Merging**: Combine video and subtitle files into a single `.mp4` file using `FFmpeg`.
- 🔥 **Customizable Resolutions**: Choose the video resolution that best fits your needs.
- 📂 **Directory Management**: Organizes downloaded files in a structured format.

---

## **Requirements**
- **Python 3.8+**
- **FFmpeg**: [Download FFmpeg](https://ffmpeg.org/download.html)
- **N_m3u8DL-RE**: [Download N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)

### Install Python Dependencies:
```bash
pip install -r requirements.txt
