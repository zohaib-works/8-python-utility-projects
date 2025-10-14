from flask import Flask, render_template, request, redirect, url_for, flash
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from transformers import pipeline
import re


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# loading model
print("Loading model...")
summerizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
print("Model loaded.")

def get_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-z)-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('yt_url')
        video_id = get_video_id(url)

        if not video_id:
            flash('Invalid YouTube URL', 'error')
            return redirect(url_for('index'))
        
        try:
            # transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=['en']).to_raw_data()
            full_text = ' '.join([entry['text'] for entry in transcript])

            # check if too long
            # if len(full_text) > 1000:
            #     full_text = full_text[:1000]
            summary = summerizer(full_text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
            return render_template('website/result.html', summary=summary, full=full_text)
        except TranscriptsDisabled:
            flash('Transcripts are disabled for this video', 'error')
            return redirect(url_for('index'))

    return render_template('website/index.html')

if __name__ == '__main__':
    app.run(debug=True)