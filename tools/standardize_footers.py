import re
import os
from pathlib import Path

ROOT = r"c:\rexonweldsandtools"

# Standard footer from contact.html
STANDARD_FOOTER = """            <!-- FOOTER CREDIT -->
            <div class="footer-credit">
                <p>All Rights Reserved | <span class="break-mobile"></span>Designed & Developed By <span class="designer-name">Rohan Dudhare</span></p>
            </div>"""

changed_files = []
total_changed = 0

# Walk through all HTML files
for root, dirs, files in os.walk(ROOT):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find and replace footer-credit section
                # Pattern: from <!-- FOOTER CREDIT --> to </div> (closing the footer-credit div)
                pattern = r'            <!-- FOOTER CREDIT -->.*?<div class="footer-credit">.*?</div>'
                
                if re.search(pattern, content, re.DOTALL):
                    new_content = re.sub(
                        pattern,
                        STANDARD_FOOTER,
                        content,
                        flags=re.DOTALL
                    )
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        changed_files.append(filepath)
                        total_changed += 1
                        print(f"✓ Updated: {filepath}")
            
            except Exception as e:
                print(f"✗ Error processing {filepath}: {e}")

print(f"\nChanged files:")
for file in changed_files:
    print(f"  - {file}")
print(f"\nTotal changed: {total_changed}")
