# import os
# import yt_dlp
# import shutil
#
# # Create directories if they do not exist
# if not os.path.exists("temp"):
#     os.makedirs("temp")
#
# if not os.path.exists("output"):
#     os.makedirs("output")
#
# output_directory = "output"
# temp_directory = "temp"
#
# def download_youtube_video(youtube_url, output_dir):
#     ydl_opts = {
#         'format': 'bestvideo+bestaudio/best',
#         'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
#         'cachedir': temp_directory,  # set cache dir to temp dir
#         'postprocessors': [
#             {
#                 'key': 'FFmpegVideoConvertor',  # Converts to mp4
#                 'preferedformat': 'mp4',  # Note the typo in 'preferedformat'
#             }
#         ],
#     }
#
#     # Ensure ffmpeg is found and correctly used by yt-dlp
#     if not shutil.which("ffmpeg"):
#         raise EnvironmentError("ffmpeg not found. Please install ffmpeg and add it to your PATH.")
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([youtube_url])
#
# if __name__ == "__main__":
#     youtube_url = input("YouTube video URL: ")
#     download_youtube_video(youtube_url, output_directory)
#
#     print(f"Video downloaded successfully to {output_directory}")

import os
import yt_dlp
import shutil
import time

# Create directories if they do not exist
if not os.path.exists("temp"):
    os.makedirs("temp")

if not os.path.exists("output"):
    os.makedirs("output")

output_directory = "output"
temp_directory = "temp"

def download_youtube_video(youtube_url, output_dir):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'cachedir': temp_directory,  # set cache dir to temp dir
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',  # Converts to mp4
                'preferedformat': 'mp4',  # Correct typo
            }
        ],
    }

    # Ensure ffmpeg is found and correctly used by yt-dlp
    if not shutil.which("ffmpeg"):
        raise EnvironmentError("ffmpeg not found. Please install ffmpeg and add it to your PATH.")

    # Print a loader message
    print("Downloading video, please wait...", end="", flush=True)

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Print a success message
    print("\rVideo downloaded successfully to", output_dir)

if __name__ == "__main__":
    youtube_url = input("YouTube video URL: ")
    download_youtube_video(youtube_url, output_directory)

