import re
import os
from pathlib import Path

ROOT = r"c:\rexonweldsandtools"

# Updated standard CSS for .main-nav-wrapper - without position: sticky and top: 0
STANDARD_CSS = """.main-nav-wrapper {
            background: #ffffff;
            border-bottom: none;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-radius: 50px;
            margin: -15px 60px 0 60px;
        }"""

# Pattern to find .main-nav-wrapper {...} - works with various indentations
pattern = re.compile(
    r'\.main-nav-wrapper\s*\{[^}]*position\s*:\s*sticky[^}]*\}',
    re.DOTALL | re.IGNORECASE
)

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
                
                # Find .main-nav-wrapper with sticky position
                if 'position: sticky' in content and '.main-nav-wrapper' in content:
                    # Replace the entire .main-nav-wrapper rule that has position: sticky
                    new_content = re.sub(
                        r'\.main-nav-wrapper\s*\{[^}]*position\s*:\s*sticky;[^}]*top\s*:\s*0;[^}]*\}',
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
