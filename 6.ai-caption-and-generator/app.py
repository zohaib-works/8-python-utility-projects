from flask import Flask, render_template, redirect, request, url_for, send_file, flash
from PIL import Image
import os
import uuid
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch


app = Flask(__name__)
app.secret_key = 'super secret key'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# init processor and model
print("Loading model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
print("Model loaded.")

# make direactiories 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # get file
        image = request.files['image']
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(filepath)


            try:
                raw_image = Image.open(filepath).convert('RGB')
                inputs = processor(raw_image, return_tensors="pt")
                out = model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)

                caption_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{unique_filename}.txt')
                with open(caption_path, 'w') as f:
                    f.write(caption)

                return render_template('website/result.html', caption=caption, image_path=filepath, caption_file=caption_path )
            except Exception as e:
                print("Error details:", e)
                flash(f"Error processing image: {e}")
                return redirect(request.url)
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        return render_template('website/index.html')


@app.route('/download_caption/<filename>')
def download_caption(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)