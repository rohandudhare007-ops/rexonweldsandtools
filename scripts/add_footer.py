#!/usr/bin/env python3
"""
Script: add_footer.py
Scans workspace for .html files and inserts the provided CSS block into the <head>
(and into an existing <style> if present) and inserts the footer credit HTML before
</footer> (or adds a <footer> if none exists). Skips files that already contain
"footer-credit" to avoid duplicates. Creates a .bak backup for each modified file.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

css_block = '''
/* ============================= */
/* FOOTER CREDIT STYLES */
/* ============================= */
.footer-credit {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    background: transparent;
    padding: 20px 40px;
    text-align: center;
    z-index: 10;
    opacity: 0;
    transform: translateY(15px);
    transition: opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), 
                transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.footer-container.in-view .footer-credit {
    opacity: 1;
    transform: translateY(0);
}

.footer-credit p {
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0.3px;
    color: #ffffff;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
}

.footer-credit .designer-name {
    color: #822727;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Add line break for mobile */
.footer-credit .break-mobile {
    display: none;
}

/* Responsive Styles for Footer Credit */
@media (max-width: 968px) {
    /* KEEP IT ABSOLUTE - DON'T CHANGE TO RELATIVE */
    .footer-credit {
        position: absolute;
        background: transparent;
        padding: 20px 25px;
    }
    
    /* Make text white for better contrast on image */
    .footer-credit p {
        color: #ffffff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }
    
    .footer-credit .designer-name {
        color: #ff4444;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }
}

@media (max-width: 768px) {
    .footer-credit {
        padding: 18px 20px;
    }

    .footer-credit p {
        font-size: 13px;
        line-height: 1.8;
    }
}

@media (max-width: 640px) {
    .footer-credit {
        padding: 16px 18px;
    }

    .footer-credit p {
        font-size: 12px;
    }
}

@media (max-width: 480px) {
    .footer-credit {
        padding: 14px 15px;
    }

    .footer-credit p {
        font-size: 11px;
        line-height: 2;
    }
    
    /* Show line break on small screens */
    .footer-credit .break-mobile {
        display: block;
    }
}
'''

html_block = '''<!-- FOOTER CREDIT -->
        <div class="footer-credit">
            <p>All Rights Reserved | Designed & Developed By <span class="designer-name">Rohan Dudhare</span></p>
        </div>
'''

updated = []
skipped = []
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # skip .git and scripts folder to avoid editing unrelated files
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

        if 'footer-credit' in text:
            skipped.append(str(fpath))
            continue

        original = text

        # Insert CSS into existing <style> before the last </style> within <head>, or create a new <style> before </head>
        lowered = text.lower()
        head_close = lowered.find('</head>')
        if head_close != -1:
            # find last </style> before head_close
            style_pos = lowered.rfind('</style>', 0, head_close)
            if style_pos != -1:
                insert_pos = style_pos
                text = text[:insert_pos] + css_block + text[insert_pos:]
            else:
                # no style in head, create one before </head>
                insert_pos = head_close
                text = text[:insert_pos] + '\n<style>\n' + css_block + '\n</style>\n' + text[insert_pos:]
        else:
            # no head close found, append CSS at start
            text = css_block + '\n' + text

        # Insert footer HTML before the last </footer> if exists, else before </body>, else append at end
        lowered = text.lower()
        footer_close_pos = lowered.rfind('</footer>')
        if footer_close_pos != -1:
            text = text[:footer_close_pos] + '\n        ' + html_block + text[footer_close_pos:]
        else:
            body_close = lowered.rfind('</body>')
            if body_close != -1:
                text = text[:body_close] + '\n<footer>\n        ' + html_block + '\n</footer>\n' + text[body_close:]
            else:
                text = text + '\n<footer>\n        ' + html_block + '\n</footer>\n'

        # backup original and write updated
        try:
            bak = str(fpath) + '.bak'
            Path(bak).write_text(original, encoding='utf-8')
            fpath.write_text(text, encoding='utf-8')
            updated.append(str(fpath))
        except Exception as e:
            errors.append((str(fpath), str(e)))

# summary
print('--- Summary ---')
print(f'Total HTML files processed: {len(updated) + len(skipped) + len(errors)}')
print(f'Updated: {len(updated)}')
print(f'Skipped (already contained footer-credit): {len(skipped)}')
print(f'Errors: {len(errors)}')
if errors:
    for e in errors[:10]:
        print('ERR', e)

# print a short sample of updated files
for p in updated[:50]:
    print('UPDATED:', p)
for p in skipped[:50]:
    print('SKIPPED:', p)

print('Backups created with .bak extension for modified files.')
