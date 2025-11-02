from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest
from .cipher import encrypt_text, decrypt_text

app = Flask(__name__, static_folder='../static', template_folder='../templates')


@app.route('/')
def index():
    return render_template('index.html')


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
    if text is None:
        raise BadRequest('Missing "text" field')
    try:
        decrypted = decrypt_text(text)
        return jsonify({"decrypted": decrypted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # For local dev; in production, use a WSGI server like gunicorn
    app.run(host='127.0.0.1', port=5000, debug=True)
