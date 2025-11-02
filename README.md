# 🔐 Chat Encryptor

A minimal, elegant web app to encrypt and decrypt English messages using a custom reversible cipher.

## Tech
- Frontend: HTML, CSS, JavaScript (Fetch API)
- Backend: Python (Flask)
- Storage: None (stateless)

## Cipher (high-level)
Encryption steps:
1) Replace vowels: a→@, e→3, i→!, o→0, u→∪ (case-insensitive)
2) Reverse every 3rd word (per line)
3) Shift code points by +3 (keeps newlines)
4) Insert a single random salt symbol between words: " space <salt> space "

Decryption reverses the above in reverse order.

Notes:
- Multiple spaces are normalized to single spaces during encryption.
- Newlines are preserved; salts are inserted only within each line.

## Run locally (Windows PowerShell)
1) Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Start the Flask server:

```powershell
python -m app.app
```

3) Open the app: http://127.0.0.1:5000/

## Project Structure
- `app/` – Flask app and cipher logic
  - `app.py` – Flask routes (UI + APIs)
  - `cipher.py` – Encryption/decryption logic
- `templates/index.html` – UI
- `static/css/styles.css` – Styles
- `static/js/app.js` – Frontend logic

## API
- `POST /api/encrypt` – body: `{ "text": "..." }` → `{ "encrypted": "..." }`
- `POST /api/decrypt` – body: `{ "text": "..." }` → `{ "decrypted": "..." }`

## License
MIT
