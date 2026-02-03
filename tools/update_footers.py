import re
import os

ROOT = r"c:\rexonweldsandtools"
STANDARD = '<p>All Rights Reserved | <span class="break-mobile"></span>Designed & Developed By <span class="designer-name">Rohan Dudhare</span></p>'

changed = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for name in filenames:
        if not name.lower().endswith('.html'):
            continue
        if name.lower().endswith(('.bak','.bak2','.bak3')):
            continue
        path = os.path.join(dirpath, name)
        rel = os.path.relpath(path, ROOT)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            s = f.read()

        # find footer-credit div
        m = re.search(r'(?:<div[^>]*class="footer-credit"[^>]*>)([\s\S]*?)(?:</div>)', s, flags=re.IGNORECASE)
        if m:
            inner = m.group(1)
            # check if STANDARD present
            if STANDARD in inner:
                continue
            # replace or insert <p> inside inner
            if re.search(r'<p[^>]*>.*All Rights Reserved.*?</p>', inner, flags=re.IGNORECASE|re.DOTALL):
                new_inner = re.sub(r'<p[^>]*>.*?All Rights Reserved.*?</p>', STANDARD, inner, flags=re.IGNORECASE|re.DOTALL)
            else:
                # insert before end
                new_inner = inner + '\n' + STANDARD + '\n'
            new_s = s[:m.start(1)] + new_inner + s[m.end(1):]
            if new_s != s:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_s)
                changed.append(rel)
        else:
            # try to append footer-credit before closing </footer> if exists
            if '</footer>' in s.lower():
                insert = '\n    <div class="footer-credit">\n        ' + STANDARD + '\n    </div>\n'
                # naive insert before last </footer>
                idx = s.lower().rfind('</footer>')
                new_s = s[:idx] + insert + s[idx:]
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_s)
                changed.append(rel)

print('Changed files:')
for c in changed:
    print(c)
print('Total changed:', len(changed))
