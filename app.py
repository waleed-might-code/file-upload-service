import os
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
MAX_FILENAME_LENGTH = 100
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_safe_filename(original_filename):
    safe_name = secure_filename(original_filename)
    name_parts = safe_name.rsplit('.', 1)
    if len(name_parts) == 2:
        name, ext = name_parts
    else:
        name = safe_name
        ext = ''
    
    if len(safe_name) > MAX_FILENAME_LENGTH:
        name_hash = hashlib.md5(original_filename.encode()).hexdigest()[:8]
        name = f"{name[:20]}_{name_hash}"
        safe_name = f"{name}.{ext}" if ext else name
    
    counter = 1
    final_name = safe_name
    while os.path.exists(os.path.join(UPLOAD_FOLDER, final_name)):
        if ext:
            final_name = f"{name}_{counter}.{ext}"
        else:
            final_name = f"{name}_{counter}"
        counter += 1
    
    return final_name

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = generate_safe_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        base_url = request.host_url.rstrip('/')
        file_url = f"{base_url}/files/{filename}"
        
        return jsonify({
            'success': True,
            'filename': filename,
            'original_filename': file.filename,
            'url': file_url,
            'size': os.path.getsize(filepath)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'file-upload-service'}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'File Upload Service',
        'endpoints': {
            'upload': {
                'method': 'POST',
                'path': '/upload',
                'description': 'Upload a file (multipart/form-data with file field)',
                'max_size': '100MB'
            },
            'download': {
                'method': 'GET',
                'path': '/files/<filename>',
                'description': 'Download/view uploaded file'
            }
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
