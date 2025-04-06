import subprocess
import requests
import os, time
import shutil
from modules.logging import setup_logging
from modules.viu import RED, WHITE, GREEN, YELLOW, RESET, CYAN

logging = setup_logging()
logs_dir = "logs"

def ensure_logs_directory():
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"{GREEN}[INFO]{RESET} Created logs directory: {CYAN}{logs_dir}{RESET}")
    else:
        print(f"{YELLOW}[INFO]{RESET} Logs directory already exists: {CYAN}{logs_dir}{RESET}")
        
def cleanup_logs_dir():
    if os.path.exists(logs_dir):
        for filename in os.listdir(logs_dir):
            file_path = os.path.join(logs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"{RED}[ERROR]{RESET} Failed to delete {file_path}: {e}")
        print(f"{GREEN}[INFO]{RESET} Logs directory cleaned up: {logs_dir}")
    else:
        print(f"{YELLOW}[INFO]{RESET} Logs directory does not exist: {logs_dir}")
        
def download_file(url, output_file):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    else:
        print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {WHITE}{output_file} {RED}| DOWNLOAD FAILED {RESET}")

def download_hls(m3u8_url, output_file):
    print(f"{YELLOW}[VIU-DOWNLOADER]{RED}: {WHITE}{m3u8_url}{RESET}\n")
    base_filename = output_file
    command = f'N_m3u8DL-RE.exe "{m3u8_url}" --save-name "{base_filename}" --save-dir "{logs_dir}" --thread-count 3 -mt -M format=mp4 --select-video "BEST" --select-audio "BEST"'
    try:
        exit_code = os.system(command)
        if exit_code == 0:
            downloaded_path = os.path.join(logs_dir, f"{base_filename}.mp4")
            print(f"{GREEN}[SUCCESS]{RESET} HLS video downloaded: {downloaded_path}")
            return downloaded_path
        else:
            print(f"{RED}[ERROR]{RESET} Failed to download HLS video: {m3u8_url}")
            return None
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Error during download: {e}")
        return None

def find_and_merge_files():
    """
    Find .mp4 and .srt files in the logs directory, merge them, and save the merged files in the same directory.
    """
    if not os.path.exists(logs_dir):
        print(f"{RED}[ERROR]{RESET} Logs directory does not exist: {logs_dir}")
        return

    # Get list of .mp4 and .srt files
    mp4_files = [f for f in os.listdir(logs_dir) if f.endswith(".mp4")]
    srt_files = [f for f in os.listdir(logs_dir) if f.endswith(".srt")]

    if not mp4_files:
        print(f"{YELLOW}[INFO]{RESET} No .mp4 files found in {logs_dir}")
        return

    if not srt_files:
        print(f"{YELLOW}[INFO]{RESET} No .srt files found in {logs_dir}")
        return

    # Match .mp4 files with .srt files based on the base filename
    for mp4_file in mp4_files:
        base_name = os.path.splitext(mp4_file)[0]
        matching_srt = next((srt for srt in srt_files if os.path.splitext(srt)[0] == base_name), None)
        if matching_srt:
            video_path = os.path.join(logs_dir, mp4_file)
            subtitle_path = os.path.join(logs_dir, matching_srt)
            output_file = os.path.join(logs_dir, f"{base_name}_with_subs.mp4")

            merge_video_and_subtitle(video_path, subtitle_path, output_file)
        else:
            print(f"{YELLOW}[INFO]{RESET} No matching subtitle for video: {mp4_file}")

def merge_video_and_subtitle(video_file, subtitle_file, output_file):
    """
    Merge a video file and subtitle file into a single output file.

    Args:
        video_file (str): Path to the video file.
        subtitle_file (str): Path to the subtitle file.
        output_file (str): Path for the merged output file.
    """
    if not os.path.exists(video_file):
        print(f"{RED}[ERROR]{RESET} Video file not found: {video_file}")
        return
    if not os.path.exists(subtitle_file):
        print(f"{RED}[ERROR]{RESET} Subtitle file not found: {subtitle_file}")
        return

    command = [
        "ffmpeg",
        "-i", video_file,
        "-y",
        "-vf", f"subtitles={subtitle_file}:force_style='Fontsize=24,PrimaryColour=&Hffffff&'",
        "-c:a", "copy",
        "-c:v", "libx264",
        output_file
    ]

    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f"{GREEN}[SUCCESS]{RESET} Video and subtitle merged successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR]{RESET} Error during merging: {e.stderr.decode('utf-8')}")
        

def create_m3u_playlist(content_name, manifest_url, append=False):
    playlist_path = "viu.m3u"
    mode = "a" if append else "w"
    with open(playlist_path, mode, encoding="utf-8") as f:
        if not append:
            f.write("#EXTM3U\n\n")

        f.write(f'#EXTINF:-1, group-title="VIU", {content_name}\n')
        f.write(f"{manifest_url}\n\n")

    return playlist_path
    
