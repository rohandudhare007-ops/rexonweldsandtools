#!/usr/bin/env python3
"""
Sync header and footer CSS from index.html to contact.html completely
"""
import re

index_file = r'c:\rexonweldsandtools\index.html'
contact_file = r'c:\rexonweldsandtools\contact.html'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

with open(contact_file, 'r', encoding='utf-8') as f:
    contact_content = f.read()

# 1. Replace entire <style> section
print("Replacing CSS...")
index_style_start = index_content.find('<style>')
index_style_end = index_content.find('</style>', index_style_start) + len('</style>')
index_full_style = index_content[index_style_start:index_style_end]

contact_style_start = contact_content.find('<style>')
contact_style_end = contact_content.find('</style>', contact_style_start) + len('</style>')
contact_full_style = contact_content[contact_style_start:contact_style_end]

# Replace contact CSS with index CSS
updated_contact = contact_content.replace(contact_full_style, index_full_style)

# 2. Replace header HTML
print("Replacing header HTML...")
index_header_start = index_content.find('<header class="dark-header-container">')
index_header_end = index_content.find('</header>', index_header_start) + len('</header>')
index_header = index_content[index_header_start:index_header_end]

contact_header_start = updated_contact.find('<header class="dark-header-container">')
contact_header_end = updated_contact.find('</header>', contact_header_start) + len('</header>')
contact_header = updated_contact[contact_header_start:contact_header_end]

updated_contact = updated_contact.replace(contact_header, index_header)

# 3. Replace footer HTML
print("Replacing footer HTML...")
index_footer_start = index_content.find('<footer class="footer-container">')
index_footer_end = index_content.find('</footer>', index_footer_start) + len('</footer>')
index_footer = index_content[index_footer_start:index_footer_end]

contact_footer_start = updated_contact.find('<footer class="footer-container">')
contact_footer_end = updated_contact.find('</footer>', contact_footer_start) + len('</footer>')
contact_footer = updated_contact[contact_footer_start:contact_footer_end]

updated_contact = updated_contact.replace(contact_footer, index_footer)

# 4. Write back to file
with open(contact_file, 'w', encoding='utf-8') as f:
    f.write(updated_contact)

print("✓ Successfully updated contact.html with CSS and HTML from index.html")
print(f"  - CSS section replaced")
print(f"  - Header HTML replaced")
print(f"  - Footer HTML replaced")
