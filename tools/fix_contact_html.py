#!/usr/bin/env python3
"""
Fix contact.html by removing duplicate CSS and ensuring proper structure
"""

index_file = r'c:\rexonweldsandtools\index.html'
contact_file = r'c:\rexonweldsandtools\contact.html'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Read contact file to preserve unique content (like the contact form, inquiry sections)
with open(contact_file, 'r', encoding='utf-8') as f:
    contact_content = f.read()

# Extract unique content from contact.html that isn't in index (contact form, inquiries, etc)
# Find where unique contact content starts (after the main nav)
contact_unique_start = contact_content.find('<!-- INQUIRY SECTION -->')
if contact_unique_start == -1:
    contact_unique_start = contact_content.find('<!-- CONTACT SECTION -->')
if contact_unique_start == -1:
    contact_unique_start = contact_content.find('<!-- HERO SECTION -->')

# Find the footer start
contact_footer_start = contact_content.find('<footer class="footer-container">')

# Extract the unique middle content from contact
unique_contact_middle = contact_content[contact_unique_start:contact_footer_start]

# Extract index.html's head section up to closing tag
index_head_start = index_content.find('<!DOCTYPE')
index_head_end = index_content.find('</head>') + len('</head>')
index_head = index_content[index_head_start:index_head_end]

# Extract index.html header and nav
index_header_start = index_content.find('<header class="dark-header-container">')
index_header_end = index_content.find('</div>\n    </div>\n\n    <div class="main-nav-wrapper">', index_header_start)
index_header = index_content[index_header_start:index_header_end + len('</div>')]

# Extract index.html nav wrapper
index_nav_start = index_content.find('    <div class="main-nav-wrapper">')
index_nav_end = index_content.find('    </div>\n\n    <section', index_nav_start)
index_nav = index_content[index_nav_start:index_nav_end + len('    </div>')]

# Extract index.html footer
index_footer_start = index_content.find('<footer class="footer-container">')
index_footer_end = index_content.find('</html>', index_footer_start)
index_footer = index_content[index_footer_start:index_footer_end]

# Get the entire style section from index (clean CSS)
style_start = index_content.find('<style>')
style_end = index_content.find('</style>', style_start) + len('</style>')
index_styles = index_content[style_start:style_end]

# Reconstruct contact.html with clean structure
fixed_contact = f"""{index_head}
<body>
{index_header}

{index_nav}

{unique_contact_middle}
{index_footer}
</body>
</html>
"""

# Write fixed content
with open(contact_file, 'w', encoding='utf-8') as f:
    f.write(fixed_contact)

print("✓ Fixed contact.html")
print("  - Removed duplicate CSS")
print("  - Cleaned up HTML structure")
print("  - Preserved unique contact content")
