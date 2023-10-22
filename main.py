from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from app.pdf_merger import merge_pdfs
import os

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MERGED_FOLDER'] = 'merged'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['MERGED_FOLDER']):
    os.makedirs(app.config['MERGED_FOLDER'])

@app.route('/')
def index():
    """
    Render the main index page.

    Returns:
        rendered HTML template
    """
    return render_template('app.html')

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs_route():
    """
    Merge PDFs based on user input.

    Returns:
        redirect to download page if successful, or error message if no PDFs provided
    """
    uploaded_files = request.files.getlist('file')
    name = request.form['name']

    pdf_files = []

    for file in uploaded_files:
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_files.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if pdf_files:
        output_name = os.path.join(app.config['MERGED_FOLDER'], name + '.pdf')
        merge_pdfs(pdf_files, output_name)
        return redirect(url_for('download', filename=name + '.pdf'))

    return "No PDF files provided."

@app.route('/download/<filename>')
def download(filename):
    """
    Serve the merged PDF for download.

    Args:
        filename (str): The name of the merged PDF file.

    Returns:
        PDF file as an attachment for download
    """
    return send_from_directory(app.config['MERGED_FOLDER'], filename, as_attachment=True)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files (CSS, JS, etc.).

    Args:
        filename (str): The name of the static file to serve.

    Returns:
        requested static file
    """
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
