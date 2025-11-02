const $ = (sel) => document.querySelector(sel);

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

function setLoading(btn, loading) {
  if (!btn) return;
  btn.disabled = loading;
  if (loading) {
    btn.dataset.label = btn.textContent;
    btn.textContent = 'Working…';
  } else if (btn.dataset.label) {
    btn.textContent = btn.dataset.label;
    delete btn.dataset.label;
  }
}

function setOutput(id, text) {
  const el = $(id);
  if (el) el.textContent = text || '';
}

async function handleEncrypt() {
  const input = $('#encrypt-input').value;
  const btn = $('#encrypt-btn');
  setLoading(btn, true);
  setOutput('#encrypt-output', '');
  try {
    const data = await postJSON('/api/encrypt', { text: input });
    setOutput('#encrypt-output', data.encrypted || '');
  } catch (err) {
    console.error(err);
    setOutput('#encrypt-output', 'Error: ' + err.message);
  } finally {
    setLoading(btn, false);
  }
}

async function handleDecrypt() {
  const input = $('#decrypt-input').value;
  const btn = $('#decrypt-btn');
  setLoading(btn, true);
  setOutput('#decrypt-output', '');
  try {
    const data = await postJSON('/api/decrypt', { text: input });
    setOutput('#decrypt-output', data.decrypted || '');
  } catch (err) {
    console.error(err);
    setOutput('#decrypt-output', 'Error: ' + err.message);
  } finally {
    setLoading(btn, false);
  }
}

async function copyFromOutput(outSel) {
  const text = $(outSel)?.textContent || '';
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
  } catch (e) {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  }
}

function init() {
  $('#encrypt-btn')?.addEventListener('click', handleEncrypt);
  $('#decrypt-btn')?.addEventListener('click', handleDecrypt);
  $('#copy-encrypted')?.addEventListener('click', () => copyFromOutput('#encrypt-output'));
  $('#copy-decrypted')?.addEventListener('click', () => copyFromOutput('#decrypt-output'));
}

document.addEventListener('DOMContentLoaded', init);
