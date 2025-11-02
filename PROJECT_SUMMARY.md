# Chat Encryptor – Project Summary

## What I Built
A complete, elegant **Chat Encryptor** web app with:
- **Frontend:** HTML, CSS (glassmorphism theme), vanilla JS (Fetch API)
- **Backend:** Python Flask (API for encrypt/decrypt)
- **Cipher:** Custom reversible algorithm per spec

---

## Cipher Algorithm (Final)
### Encryption Steps (applied in order):
1. **Vowel substitution (case-sensitive):**
   - Lowercase: a→⟨, e→⟩, i→⦃, o→⦄, u→⫰
   - Uppercase: A→⫱, E→⫲, I→⫳, O→⫴, U→⫵
   - (Unicode symbols chosen to avoid collision with normal input)

2. **Reverse every 3rd token (per line):**
   - Split on spaces, reverse tokens at positions 3, 6, 9, …
   - Preserves newlines; normalizes multiple spaces to single spaces

3. **Shift letters by +3 (Caesar cipher within A-Z/a-z):**
   - Only shifts letters; digits/punctuation/newlines unchanged
   - Wraps within alphabet (e.g., 'z' → 'c')

4. **Insert random salt between words:**
   - Insert " | " (space-pipe-space) between consecutive tokens on each line
   - Uses SystemRandom for randomness

### Decryption Steps (reverses in reverse order):
1. Remove salts (" | " → " ")
2. Shift letters by -3
3. Reverse every 3rd token (per line)
4. Reverse vowel substitution (symbols → vowels)

### Key Properties
- ✅ Fully reversible (round-trip tested)
- ✅ Handles multi-line text, punctuation, digits
- ✅ Whitespace normalization (trailing/leading spaces)
- ✅ No collisions between cipher symbols and normal input

---

## Project Structure
```
Chat Encryptor/
├── app/
│   ├── __init__.py
│   ├── app.py            # Flask routes (UI + /api/encrypt + /api/decrypt)
│   └── cipher.py         # Encryption/decryption logic
├── static/
│   ├── css/
│   │   └── styles.css    # Glassmorphism gradient theme, Poppins font
│   └── js/
│       └── app.js        # Frontend fetch logic + copy-to-clipboard
├── templates/
│   └── index.html        # Two-panel UI (encrypt/decrypt)
├── tests/
│   ├── __init__.py
│   └── test_cipher_roundtrip.py  # Round-trip test suite
├── requirements.txt      # Flask==3.0.3, Werkzeug==3.0.3
├── README.md
└── .venv/                # Python virtual environment (auto-created)
```

---

## How to Run Locally (Windows)
### 1) Setup (first-time):
```powershell
cd "D:\CODING NEW\Chat Encryptor"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Start server:
```powershell
& "D:/CODING NEW/Chat Encryptor/.venv/Scripts/python.exe" -m app.app
```

### 3) Open browser:
Navigate to: http://127.0.0.1:5000

---

## API Endpoints
- **POST /api/encrypt**
  - Body: `{ "text": "your message" }`
  - Response: `{ "encrypted": "..." }`
  
- **POST /api/decrypt**
  - Body: `{ "text": "encrypted text" }`
  - Response: `{ "decrypted": "..." }`

---

## Features Implemented
✅ Custom reversible cipher (vowel subst + word reverse + shift + salts)  
✅ Two-panel UI (encryption left, decryption right)  
✅ Responsive design (stacked on mobile)  
✅ Copy-to-clipboard buttons  
✅ Glassmorphism gradient theme with Poppins font  
✅ Smooth animations and hover effects  
✅ Error handling (backend + frontend)  
✅ Comprehensive round-trip tests (5 samples, all pass)  

---

## Testing
Run the cipher round-trip tests:
```powershell
& "D:/CODING NEW/Chat Encryptor/.venv/Scripts/python.exe" -m tests.test_cipher_roundtrip
```
**Expected output:** `ROUNDTRIP_ALL_OK = True`

---

## Notes
- **Stateless:** No database or session storage required
- **Dev server:** Current setup uses Flask's built-in server (debug mode)
- **Production:** For production, use a WSGI server like gunicorn
- **Cipher collision avoidance:** Vowel symbols are rare Unicode chars (⟨⟩⦃⦄⫰⫱⫲⫳⫴⫵) to avoid overlap with normal input

---

## What's Next?
- Add more cipher options (user-selectable algorithms)
- Export/import encrypted messages as files
- Add dark/light theme toggle
- Deploy to a cloud platform (Heroku, Render, etc.)

---

**Made with ❤️ using Python**
