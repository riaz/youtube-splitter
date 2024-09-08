import argparse
import os
import sys
from yt_dlp import YoutubeDL
import ffmpeg

def download_youtube_video(url, output_filename):
    """
    Download a YouTube video using yt-dlp.
    """
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False

def split_video(input_file):
    """
    Split the downloaded video into separate video and audio files.
    """
    try:
        # Extract video without audio
        video_output = f"{os.path.splitext(input_file)[0]}_video.mp4"
        (
            ffmpeg
            .input(input_file)
            .output(video_output, vcodec='libx264', an=None)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        # Extract audio
        audio_output = f"{os.path.splitext(input_file)[0]}_audio.mp3"
        (
            ffmpeg
            .input(input_file)
            .output(audio_output, acodec='libmp3lame', vn=None)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

        # Remove the original file
        os.remove(input_file)

        return video_output, audio_output
    except ffmpeg.Error as e:
        print(f"Error splitting video: {e.stderr.decode()}")
        return None, None

def main():
    parser = argparse.ArgumentParser(description="Download a YouTube video and split it into separate video and audio files.")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    print("Starting YouTube video download and split process...")

    # Generate a safe filename
    output_filename = "youtube_video.mp4"

    # Download the video
    print("Downloading video...")
    if not download_youtube_video(args.url, output_filename):
        sys.exit(1)

    print("Video downloaded successfully.")

    # Split the video
    print("Splitting video into separate video and audio files...")
    video_output, audio_output = split_video(output_filename)

    if video_output and audio_output:
        print(f"Video split successfully.")
        print(f"Video file: {video_output}")
        print(f"Audio file: {audio_output}")
    else:
        print("Failed to split the video.")
        sys.exit(1)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
