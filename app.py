from flask import Flask, render_template, request, send_from_directory, send_file
import yt_dlp
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'


def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        'outtmpl': f"{app.config['UPLOAD_FOLDER']}/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        download_video(url)
        video_filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        video_filename = video_filenames[-1]  # Get the latest video file
        return render_template('success.html', video_filename=video_filename)
    except yt_dlp.utils.DownloadError:
        return render_template('error.html')


@app.route('/uploads/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
