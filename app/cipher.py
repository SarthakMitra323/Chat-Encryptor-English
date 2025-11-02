import random
import re
from typing import List

# Custom reversible cipher per spec
# Encryption:
# 1) Replace vowels with symbols (case-sensitive, preserves case)
# 2) Reverse every 3rd word (per line)
# 3) Shift LETTERS ONLY by +3 (wrap within A-Z/a-z); digits/punct unchanged
# 4) Insert one random salt symbol between words (space <salt> space)
#
# Decryption reverses the steps in reverse order
#
# Notes:
# - Newlines are treated as hard separators and preserved.
# - Multiple spaces are normalized to single spaces during encryption.
# - Digits and punctuation are never shifted; only letters are.

VOWEL_MAP = {
    'a': '⟨', 'e': '⟩', 'i': '⦃', 'o': '⦄', 'u': '⫰',
    'A': '⫱', 'E': '⫲', 'I': '⫳', 'O': '⫴', 'U': '⫵',
}
INV_VOWEL_MAP = {v: k for k, v in VOWEL_MAP.items()}

# Choose uncommon separator symbols unlikely in normal text
# To avoid collision, use vertical bar '|' exclusively
SALT_CHARS: List[str] = ['|']
SALT_CLASS = ''.join(re.escape(c) for c in SALT_CHARS)
SALT_PATTERN = re.compile(rf"\s([{SALT_CLASS}])\s")


def _substitute_vowels(text: str, encrypt: bool) -> str:
    if encrypt:
        return ''.join(VOWEL_MAP.get(ch, ch) for ch in text)
    # decrypt path: map symbols back to vowels where applicable
    return ''.join(INV_VOWEL_MAP.get(ch, ch) for ch in text)


def _reverse_every_nth_word_line(line: str, n: int = 3) -> str:
    # Normalize spaces to single spaces
    # Split into "tokens" on spaces (each token may contain alphanumeric+symbols).
    # Reverse every nth token.
    tokens = line.split()
    for idx in range(n - 1, len(tokens), n):  # 0-based index of every nth token
        tokens[idx] = tokens[idx][::-1]
    return ' '.join(tokens)


def _reverse_every_nth_word(text: str, n: int = 3) -> str:
    # Apply per-line to preserve newlines
    lines = text.split('\n')
    return '\n'.join(_reverse_every_nth_word_line(line, n) for line in lines)


def _shift_letters(text: str, shift: int) -> str:
    # Shift only letters (A-Z, a-z) by the given amount, wrapping within the alphabet.
    # Leave digits, newlines, and punctuation unchanged.
    out_chars = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            new_code = ((ord(ch) - ord('A') + shift) % 26) + ord('A')
            out_chars.append(chr(new_code))
        elif 'a' <= ch <= 'z':
            new_code = ((ord(ch) - ord('a') + shift) % 26) + ord('a')
            out_chars.append(chr(new_code))
        else:
            out_chars.append(ch)
    return ''.join(out_chars)


def _insert_salts(text: str) -> str:
    # Insert one random symbol between words for each gap on each line
    rng = random.SystemRandom()
    lines = text.split('\n')
    salted_lines = []
    for line in lines:
        words = line.split()
        if not words:
            salted_lines.append('')
            continue
        pieces = [words[0]]
        for w in words[1:]:
            salt = rng.choice(SALT_CHARS)
            pieces.append(f" {salt} ")
            pieces.append(w)
        salted_lines.append(''.join(pieces))
    return '\n'.join(salted_lines)


def _remove_salts(text: str) -> str:
    # Replace occurrences of " space <SALT> space " with a single space.
    # Repeat until no more matches to handle adjacent or repeated salts (unlikely).
    prev = None
    cur = text
    while prev != cur:
        prev = cur
        cur = SALT_PATTERN.sub(' ', cur)
    return cur


def encrypt_text(text: str) -> str:
    if not text:
        return ''
    step1 = _substitute_vowels(text, encrypt=True)
    step2 = _reverse_every_nth_word(step1, n=3)
    step3 = _shift_letters(step2, shift=3)
    step4 = _insert_salts(step3)
    return step4


def decrypt_text(text: str) -> str:
    if not text:
        return ''
    step1 = _remove_salts(text)
    step2 = _shift_letters(step1, shift=-3)
    step3 = _reverse_every_nth_word(step2, n=3)
    step4 = _substitute_vowels(step3, encrypt=False)
    return step4


__all__ = [
    'encrypt_text',
    'decrypt_text',
]