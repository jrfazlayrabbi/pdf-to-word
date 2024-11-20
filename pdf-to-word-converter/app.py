from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_pdf_to_word(pdf_path, word_path):
    cv = Converter(pdf_path)
    cv.convert(word_path, start=0, end=None)
    cv.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return 'No file part', 400

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return 'No selected file', 400

    if pdf_file and pdf_file.filename.endswith('.pdf'):
        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        word_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '.docx'))

        pdf_file.save(pdf_path)
        convert_pdf_to_word(pdf_path, word_path)

        return send_file(word_path, as_attachment=True)

    return 'Invalid file format', 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
