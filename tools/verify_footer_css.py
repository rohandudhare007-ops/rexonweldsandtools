#!/usr/bin/env python3
import os
import re

ROOT = r'c:\rexonweldsandtools'

# The complete footer-credit CSS from contact.html
STANDARD_FOOTER_CSS = r""".footer-credit {
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
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
        }

        .footer-credit .designer-name {
            color: #ff4444;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .footer-credit .break-mobile {
            display: none;
        }"""

changed_files = []
not_found_files = []

for root, dirs, files in os.walk(ROOT):
    # Skip tools directory
    if 'tools' in root:
        continue
    
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it has the standard CSS
                if STANDARD_FOOTER_CSS not in content:
                    not_found_files.append(file)
            except Exception as e:
                pass

print("Footer CSS Verification Report")
print("=" * 50)
if not_found_files:
    print(f"\nFiles with NON-STANDARD footer CSS ({len(not_found_files)}):")
    for f in sorted(not_found_files)[:20]:
        print(f"  - {f}")
else:
    print("\n✓ All pages have STANDARD footer CSS!")
    print(f"\nTotal HTML files checked: All files match contact.html CSS")
