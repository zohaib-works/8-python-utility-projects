from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)



class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(300), nullable=False)
    short_url = db.Column(db.String(10), nullable=False)



with app.app_context():
    db.create_all()

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = "".join(random.choices(characters, k=length))
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        # check if exist show the same short url
        url = URL.query.filter_by(long_url=long_url).first()
        if not url:
            short_url = generate_short_url()
            url = URL(long_url=long_url, short_url=short_url)
            db.session.add(url)
            db.session.commit()
        else:
            short_url = url.short_url
        return render_template('website/result.html', short_url=request.host_url + short_url)
    return render_template('website/index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    if url:
        return redirect(url.long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)