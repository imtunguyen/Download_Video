import os
import json



def extract_format_data(format_data):
    allowed_extensions = ["mp3", "mp4"]
    allowed_formats = ["bestvideo+bestaudio"]

    extension = format_data.get("ext")
    format_name = format_data.get("format")
    url = format_data.get("url")

    # Kiểm tra nếu cả âm thanh và video đều có sẵn
    if 'audio' in format_name and 'video' in format_name:
        return {
            "extension": extension,
            "format_name": format_name,
            "url": url
        }
    
    return None



def extract_video_data_from_url(url):
    command = f'yt-dlp "{url}" -j --no-playlist'
    output = os.popen(command).read()
    video_data = json.loads(output)
    title = video_data["title"]
    formats = video_data["formats"]
    thumbnail = video_data["thumbnail"]
    formats = [extract_format_data(format_data) for format_data in formats]
    return {
        "title": title,
        "formats": formats,
        "thumbnail": thumbnail
    }
