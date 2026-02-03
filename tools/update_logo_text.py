import re
import os
from pathlib import Path

ROOT = r"c:\rexonweldsandtools"
LOGO_PATTERN = re.compile(
    r'<span class="logo-text">.*?</span>',
    re.DOTALL
)
STANDARD_LOGO = '<span class="logo-text"> WELDS & TOOL CO</span>'

changed_files = []
total_changed = 0

# Walk through all HTML files
for root, dirs, files in os.walk(ROOT):
    for file in files:
        # Skip backup files
        if file.endswith('.bak') or file.endswith('.bak2') or file.endswith('.bak3'):
            continue
        
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all logo-text spans
                matches = LOGO_PATTERN.findall(content)
                
                if matches:
                    # Check if it needs updating
                    needs_update = False
                    for match in matches:
                        if match != STANDARD_LOGO:
                            needs_update = True
                            break
                    
                    if needs_update:
                        # Replace all logo-text spans with standard
                        new_content = LOGO_PATTERN.sub(STANDARD_LOGO, content)
                        
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
