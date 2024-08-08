import whisper
import textwrap
import os
import glob
import re
import yt_dlp
import warnings

warnings.filterwarnings("ignore")

text = ""
youtube_video_name = ""

# Create necessary directories if they don't exist
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)

output_directory = "output"
temp_directory = "temp"

# Find .webm and .wav files in the current and temp directories
main_path = os.getcwd()
webm_files = glob.glob(os.path.join(main_path, "*.webm"))
wav_files = glob.glob(os.path.join(main_path, temp_directory, "*.wav"))

# Transcribe audio function
def transcribe_audio(file_path_mp3, youtube_video_name):
    model = whisper.load_model("base")
    result = model.transcribe(file_path_mp3, fp16=False)
    del model

    # Extract text from the result
    if isinstance(result, dict) and "text" in result:
        result = result["text"]
    else:
        result = str(result)

    # Reformat the output text into paragraphs
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result)
    paragraphs = []
    paragraph = []

    for sentence in sentences:
        paragraph.append(sentence)
        if len(paragraph) == 4:
            paragraphs.append(" ".join(paragraph))
            paragraph = []

    if paragraph:
        paragraphs.append(" ".join(paragraph))

    formatted = "\n\n".join(paragraphs)

    # Word-wrap the text without modifying existing newlines
    wrapped = "\n\n".join(
        ["  " + textwrap.fill(p, width=80) for p in formatted.split("\n\n")]
    )

    # Add an extra newline between paragraphs
    wrapped_with_extra_newline = "\n\n".join([wrapped, ""])

    # Sanitize YouTube name output
    video_name = re.sub(r"[\W_]+", " ", youtube_video_name)

    # Establish output directory and file name
    file_name = f"{video_name}.txt"
    file_path = os.path.join(output_directory, file_name)

    # Write the output to a file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(wrapped_with_extra_newline)

if __name__ == "__main__":
    try:
        youtube_url = input("YouTube video URL: ")

        # Extract video information
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(youtube_url, download=False)
        youtube_video_name = info["title"]

        # Download audio from the YouTube video
        ydl_opts = {
            "format": "bestaudio",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(temp_directory, "temp.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        file_path_mp3 = os.path.join(temp_directory, "temp.wav")

        # Transcribe the audio
        transcribe_audio(file_path_mp3, youtube_video_name)

        # Cleanup leftover files
        for webm_file in webm_files:
            os.remove(webm_file)
        for wav_file in wav_files:
            os.remove(wav_file)

        print("Transcription completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
