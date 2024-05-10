from flask import Flask, request, render_template, jsonify
import yt_dlp
import logging
from googleapiclient.discovery import build
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.api import FacebookAdsApi
app = Flask(__name__)
api_key = 'AIzaSyBB-qktCLrl641YJLW0COkzCwqSrtMXN-s'
access_token ='1512958009564697|unYBxLdFJDKk4x6C7TTW2Hb0JLw'

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/orther")
def order():
    return render_template("orther.html")
def search_video(video_url):
    videos = []
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_response = youtube.search().list(part='snippet', q=video_url).execute()
    for item in video_response['items']:
        if item['id']['kind'] == 'youtube#video':
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            })
    return videos

def download_video(video_url, download_format):
    message = ''
    errorType = 0
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
        }],
    }
    if download_format == 'mp3':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['postprocessors'][0]['preferredcodec'] = 'mp3'
    elif download_format == 'mp4':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['postprocessors'][0]['preferredcodec'] = 'mp4'  
    elif download_format == 'webm':
        ydl_opts['format'] = 'webm/best'
        ydl_opts['postprocessors'][0]['preferredcodec'] = 'opus'  
    elif download_format == 'ogg':
        ydl_opts['format'] = 'vorbis/best'
        ydl_opts['postprocessors'][0]['preferredcodec'] = 'vorbis'  
    elif download_format == 'wav':
        ydl_opts['format'] = 'wav/best'
        ydl_opts['postprocessors'][0]['preferredcodec'] = 'wav' 

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            message = 'Downloaded successfully!'
        except yt_dlp.utils.DownloadError:
            errorType = 1
            message = 'Invalid video URL!'
            logging.error('Invalid Video URL: %s', video_url)
        except Exception as e:
            errorType = 1
            message = 'An error occurred!'
            logging.exception('An Error Occurred: %s', str(e))

    return message, errorType

@app.route("/search", methods=["POST"])
def search():
    video_url = request.form.get('video_url', '')
    videos = search_video(video_url)
    return jsonify({'videos': videos})

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    video_url = data.get('video_url', '')
    download_format = data.get('format', '')
    message, errorType = download_video(video_url, download_format)
    return jsonify({'message': message, 'errorType': errorType})

@app.route("/downloadOther", methods=["POST"])
def download_orther():
    video_url = request.form.get('video_url', '')
    download_format = request.form.get('download_format', '')
    message, errorType = download_video(video_url, download_format)
    return render_template('orther.html', message=message, errorType=errorType)
if __name__ == "__main__":
    app.run(debug=True)