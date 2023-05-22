from flask import Flask, render_template, request, send_from_directory, send_file
import yt_dlp
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'


def download_video(url, download_video=True, download_audio=False):
    ydl_opts = {
        'outtmpl': f"{app.config['UPLOAD_FOLDER']}/%(title)s.%(ext)s",
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'writeautomaticsub': True,
    }
    if not download_video:
        ydl_opts['writesubtitles'] = True
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_video_option = request.form.get('download_video')
    download_audio_option = request.form.get('download_audio')
    try:
        if download_video_option == 'on' and download_audio_option == 'on':
            download_video(url, download_video=True, download_audio=False)
        elif download_video_option == 'on':
            download_video(url, download_video=True, download_audio=True)
        elif download_audio_option == 'on':
            download_video(url, download_video=False, download_audio=True)
        else:
            return render_template('error.html')
        
        video_filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        video_filename = video_filenames[-1]  # Get the latest video file
        return render_template('success.html', video_filename=video_filename)
    except yt_dlp.utils.DownloadError:
        return render_template('error.html')


@app.route('/videos/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
