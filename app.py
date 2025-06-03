from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Proses upload dan perbaikan kualitas citra
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # Simpan file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Buka gambar menggunakan Pillow
        img = Image.open(filepath)

        # Perbaiki kualitas citra
        img = improve_image_quality(img)

        # Simpan gambar hasil perbaikan
        processed_filename = 'processed_' + file.filename
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        img.save(processed_filepath)

        return render_template('index.html', original_filename=file.filename, processed_filename=processed_filename)

def improve_image_quality(img):
    # Konversi ke grayscale
    img = img.convert('L')

    # Tingkatkan kontras
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Tingkatkan kontras 1.5x

    # Konversi ke format OpenCV
    img = cv2.cvtColor(np.array(img), cv2.COLOR_GRAY2BGR)

    # Reduksi noise menggunakan Gaussian Blur
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Konversi kembali ke format Pillow
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    # Tambahkan penajaman (sharpening)
    img = img.filter(ImageFilter.SHARPEN)

    return img

if __name__ == '__main__':
    app.run(debug=True)
