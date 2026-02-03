#!/usr/bin/env python3
"""
Replace footer CSS and HTML in ALL HTML files with the exact code from product-aps-discover-200dx.html
"""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]

# Read the target footer CSS and HTML from product-aps-discover-200dx.html
target_file = ROOT / "product-aps-discover-200dx.html"
target_text = target_file.read_text(encoding='utf-8')

# Extract FOOTER CSS (from "/* === FOOTER STYLES ===" to "/* === RESPONSIVE STYLES ===")
footer_css_start = target_text.find('/* === FOOTER STYLES === */')
footer_css_end = target_text.find('/* === RESPONSIVE STYLES === */')
footer_css = target_text[footer_css_start:footer_css_end].rstrip()

# Extract RESPONSIVE CSS for footer (from "/* === RESPONSIVE STYLES ===" to "</style>")
responsive_start = target_text.find('/* === RESPONSIVE STYLES === */')
responsive_end = target_text.find('</style>')
responsive_css = target_text[responsive_start:responsive_end].rstrip()

# Combined footer CSS and responsive rules
full_footer_css = footer_css + '\n\n' + responsive_css

# Extract FOOTER HTML (from "<footer class=" to "</footer>")
footer_html_start = target_text.find('<footer class="footer-container">')
footer_html_end = target_text.find('</footer>') + len('</footer>')
footer_html = target_text[footer_html_start:footer_html_end]

print("Footer CSS extracted:", len(full_footer_css), "bytes")
print("Footer HTML extracted:", len(footer_html), "bytes")

# Now update ALL HTML files
updated = 0
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    if '.git' in dirpath or 'scripts' in dirpath:
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

        original = text

        # Replace old footer CSS (from /* === FOOTER STYLES to first </style>)
        # Find where footer CSS starts
        footer_css_idx = text.find('/* === FOOTER STYLES ===')
        if footer_css_idx == -1:
            # Try alternate pattern
            footer_css_idx = text.find('/* ============================= */')
            if footer_css_idx == -1:
                continue

        # Find closing </style>
        style_close_idx = text.find('</style>')
        if style_close_idx == -1:
            continue

        # Replace everything from footer CSS start to </style> with new footer CSS
        text_before = text[:footer_css_idx]
        text_after = text[style_close_idx:]
        text = text_before + full_footer_css + '\n        ' + text_after

        # Replace old footer HTML (from <footer to </footer>)
        footer_start = text.find('<footer')
        footer_end = text.find('</footer>') + len('</footer>')
        
        if footer_start != -1 and footer_end > footer_start:
            text_before = text[:footer_start]
            text_after = text[footer_end:]
            text = text_before + footer_html + '\n\n    ' + text_after

        # Write back
        try:
            bak = str(fpath) + '.bak3'
            Path(bak).write_text(original, encoding='utf-8')
            fpath.write_text(text, encoding='utf-8')
            updated += 1
            print(f"UPDATED: {fpath.name}")
        except Exception as e:
            errors.append((str(fpath), str(e)))

print(f"\n✓ Total files updated: {updated}")
print(f"✗ Errors: {len(errors)}")
if errors:
    for e in errors[:5]:
        print(f"  {e[0]}: {e[1]}")
