from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/website/index.html')


@app.route('/resize', methods=['POST'])
def resize():
    if request.method == 'POST':
        image_file = request.files['image']
        width = int(request.form['width'])
        height = int(request.form['height'])
        quality = int(request.form['quality'])

        # Perform image resizing logic here
        if not image_file:
            return "No image file provided"
        
        image = Image.open(image_file)

        if width and height:
            image = image.resize((width, height), Image.Resampling.LANCZOS)

        # buffer 
        buffer = BytesIO()
        format = 'JPEG' if image.mode != 'PNG' else 'PNG'
        quality = quality if quality else 85
                
        image.save(buffer, format=format, quality=quality, optimize=True)
        buffer.seek(0)
        return send_file(buffer, mimetype='image/jpeg', as_attachment=True, download_name=f'opt.{image_file.filename}')


if __name__ == '__main__':
    app.run(debug=True)