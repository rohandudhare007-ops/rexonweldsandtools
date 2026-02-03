#!/usr/bin/env python3
"""
Sync header and footer CSS from index.html to contact.html
"""
import re

index_file = r'c:\rexonweldsandtools\index.html'
contact_file = r'c:\rexonweldsandtools\contact.html'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

with open(contact_file, 'r', encoding='utf-8') as f:
    contact_content = f.read()

# Extract CSS sections
# Find the main style block
style_start = index_content.find('<style>')
style_end = index_content.find('</style>', style_start) + len('</style>')
index_styles = index_content[style_start:style_end]

contact_style_start = contact_content.find('<style>')
contact_style_end = contact_content.find('</style>', contact_style_start) + len('</style>')
contact_styles = contact_content[contact_style_start:contact_style_end]

print("Index.html CSS length:", len(index_styles))
print("Contact.html CSS length:", len(contact_styles))

# Extract header HTML
index_header_start = index_content.find('<header class="dark-header-container">')
index_header_end = index_content.find('</header>', index_header_start) + len('</header>')
index_header_html = index_content[index_header_start:index_header_end]

contact_header_start = contact_content.find('<header class="dark-header-container">')
contact_header_end = contact_content.find('</header>', contact_header_start) + len('</header>')
contact_header_html = contact_content[contact_header_start:contact_header_end]

print("\nHeader HTML lengths:")
print("Index:", len(index_header_html))
print("Contact:", len(contact_header_html))
print("\nHeaders match:", index_header_html == contact_header_html)

# Extract footer HTML
index_footer_start = index_content.find('<footer class="footer-container">')
index_footer_end = index_content.find('</footer>', index_footer_start) + len('</footer>')
index_footer_html = index_content[index_footer_start:index_footer_end]

contact_footer_start = contact_content.find('<footer class="footer-container">')
contact_footer_end = contact_content.find('</footer>', contact_footer_start) + len('</footer>')
contact_footer_html = contact_content[contact_footer_start:contact_footer_end]

print("\nFooter HTML lengths:")
print("Index:", len(index_footer_html))
print("Contact:", len(contact_footer_html))

# Save samples for viewing
print("\nSaving samples...")
with open(r'c:\rexonweldsandtools\tools\index_footer_sample.txt', 'w') as f:
    f.write(index_footer_html[:500])
    
with open(r'c:\rexonweldsandtools\tools\contact_footer_sample.txt', 'w') as f:
    f.write(contact_footer_html[:500])
