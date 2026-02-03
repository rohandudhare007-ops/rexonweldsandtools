import re
import os
from pathlib import Path

ROOT = r"c:\rexonweldsandtools"

# Updated standard CSS for .main-nav-wrapper - WITH sticky positioning
STANDARD_CSS = """.main-nav-wrapper {
            background: #ffffff;
            border-bottom: none;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-radius: 50px;
            margin: -15px 60px 0 60px;
        }"""

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
                
                # Find .main-nav-wrapper WITHOUT sticky position
                if '.main-nav-wrapper' in content and 'position: sticky' not in content:
                    # Replace the .main-nav-wrapper rule to add sticky positioning
                    new_content = re.sub(
                        r'\.main-nav-wrapper\s*\{[^}]*background\s*:\s*#ffffff[^}]*\}',
                        STANDARD_CSS,
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
