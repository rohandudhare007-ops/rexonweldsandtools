#!/usr/bin/env python3
"""
Append a small CSS override before </style> in HTML files that contain .footer-credit
to make the footer credit position: relative and visible (prevents layout overlap).
Creates .bak backups for modified files.
"""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
override = '''

/* Footer credit layout override: keep it relative and visible for consistent layout */
.footer-credit {
    position: relative !important;
    opacity: 1 !important;
    transform: none !important;
    background: transparent; /* keep original transparent where desired */
    padding: 20px 40px !important;
    text-align: center;
    color: #ffffff !important;
}

@media (max-width: 968px) {
    .footer-credit {
        position: relative !important;
    }
}
'''

updated = []
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    if '.git' in dirpath:
        continue
    for fname in filenames:
        if not fname.lower().endswith('.html'):
            continue
        fpath = Path(dirpath) / fname
        try:
            text = fpath.read_text(encoding='utf-8')
        except Exception as e:
            errors.append((str(fpath), str(e)))
            continue

        if '.footer-credit' not in text:
            continue

        if '/* Footer credit layout override' in text:
            # already applied
            continue

        # insert override before the last </style>
        idx = text.lower().rfind('</style>')
        if idx != -1:
            new_text = text[:idx] + override + text[idx:]
        else:
            # append at top if no style
            new_text = text + '\n<style>' + override + '</style>'

        try:
            bak = str(fpath) + '.bak2'
            Path(bak).write_text(text, encoding='utf-8')
            fpath.write_text(new_text, encoding='utf-8')
            updated.append(str(fpath))
        except Exception as e:
            errors.append((str(fpath), str(e)))

print('Updated:', len(updated))
for p in updated[:50]:
    print('UPDATED:', p)
print('Errors:', len(errors))
if errors:
    for e in errors[:10]:
        print('ERR', e)
