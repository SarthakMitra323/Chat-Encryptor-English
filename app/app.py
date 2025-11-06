from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest
from .cipher import encrypt_text, decrypt_text

app = Flask(__name__, static_folder='../static', template_folder='../templates')


@app.route('/')
def index():
    # Look first in root index.html (moved for Vercel), fall back to templates folder.
    try:
        return render_template('index.html')
    except Exception:
        # If template not found (during local dev after moving index to root), serve static file.
        from flask import send_file
        import os
        root_index = os.path.join(os.path.dirname(__file__), '..', 'index.html')
        if os.path.exists(root_index):
            return send_file(root_index)
        raise


@app.post('/api/encrypt')
def api_encrypt():
    if not request.is_json:
        raise BadRequest('Expected JSON body')
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if text is None:
        raise BadRequest('Missing "text" field')
    try:
        encrypted = encrypt_text(text)
        return jsonify({"encrypted": encrypted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post('/api/decrypt')
def api_decrypt():
    if not request.is_json:
        raise BadRequest('Expected JSON body')
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    password = data.get('password')
    if text is None:
        raise BadRequest('Missing "text" field')
    # Password check (backend enforced)
    try:
        # Accept both string and int representations
        if str(password) != '1801':
            return jsonify({"error": "Invalid password"}), 401
    except Exception:
        return jsonify({"error": "Invalid password"}), 401
    try:
        decrypted = decrypt_text(text)
        return jsonify({"decrypted": decrypted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # For local dev; in production, use a WSGI server like gunicorn
    app.run(host='127.0.0.1', port=5000, debug=True)
