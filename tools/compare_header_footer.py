#!/usr/bin/env python3
import os

contact_file = r'c:\rexonweldsandtools\contact.html'
index_file = r'c:\rexonweldsandtools\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

with open(contact_file, 'r', encoding='utf-8') as f:
    contact_content = f.read()

# Find header section in index
index_header_start = index_content.find('<header class="dark-header-container">')
index_header_end = index_content.find('</header>', index_header_start) + len('</header>')
index_header = index_content[index_header_start:index_header_end]

# Find header section in contact
contact_header_start = contact_content.find('<header class="dark-header-container">')
contact_header_end = contact_content.find('</header>', contact_header_start) + len('</header>')
contact_header = contact_content[contact_header_start:contact_header_end]

# Compare headers
if index_header == contact_header:
    print("✓ HEADER HTML: IDENTICAL")
else:
    print("✗ HEADER HTML: DIFFERENT")
    print(f"Index header length: {len(index_header)}")
    print(f"Contact header length: {len(contact_header)}")

# Find footer section in index
index_footer_start = index_content.find('<footer class="footer-container">')
index_footer_end = index_content.find('</footer>', index_footer_start) + len('</footer>')
index_footer = index_content[index_footer_start:index_footer_end]

# Find footer section in contact
contact_footer_start = contact_content.find('<footer class="footer-container">')
contact_footer_end = contact_content.find('</footer>', contact_footer_start) + len('</footer>')
contact_footer = contact_content[contact_footer_start:contact_footer_end]

# Compare footers
if index_footer == contact_footer:
    print("✓ FOOTER HTML: IDENTICAL")
else:
    print("✗ FOOTER HTML: DIFFERENT")
    print(f"Index footer length: {len(index_footer)}")
    print(f"Contact footer length: {len(contact_footer)}")
    
# Save differences to files for inspection
with open(r'c:\rexonweldsandtools\tools\index_header.txt', 'w') as f:
    f.write(index_header)
    
with open(r'c:\rexonweldsandtools\tools\contact_header.txt', 'w') as f:
    f.write(contact_header)

print("\nHeader and footer sections saved to tools/ directory for comparison")
