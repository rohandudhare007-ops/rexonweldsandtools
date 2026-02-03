#!/usr/bin/env python3
"""
Completely rebuild contact.html from index.html template
"""
import re

index_file = r'c:\rexonweldsandtools\index.html'
contact_file = r'c:\rexonweldsandtools\contact.html'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Start with clean index.html content
clean_contact = index_content

# Replace only the title
clean_contact = clean_contact.replace(
    '<title>Rexon Welds And Tools - Home</title>',
    '<title>Rexon Welds And Tools - Contact</title>'
)

# Find and extract the contact-specific content sections
# We need to read the original contact.html to get inquiry form, map, etc
with open(contact_file, 'r', encoding='utf-8') as f:
    original_contact = f.read()

# Extract inquiry form section if it exists
inquiry_form_match = re.search(
    r'<!-- INQUIRY SECTION -->.*?<!-- END INQUIRY SECTION -->',
    original_contact,
    re.DOTALL
)

# Extract contact section if exists
contact_section_match = re.search(
    r'<!-- CONTACT SECTION -->.*?<!-- END CONTACT SECTION -->',
    original_contact,
    re.DOTALL
)

# Extract map section if exists
map_section_match = re.search(
    r'<!-- MAP SECTION -->.*?</section>',
    original_contact,
    re.DOTALL
)

# Now replace the main content area in clean_contact
# Find where to insert contact-specific content (after nav, before footer)
content_start = clean_contact.find('    <section class="slider">')
footer_start = clean_contact.find('    <footer class="footer-container">')

if content_start != -1 and footer_start != -1:
    # Get contact-specific sections
    contact_unique_content = ""
    if inquiry_form_match:
        contact_unique_content += inquiry_form_match.group(0) + "\n\n"
    if contact_section_match:
        contact_unique_content += contact_section_match.group(0) + "\n\n"
    if map_section_match:
        contact_unique_content += map_section_match.group(0) + "\n\n"
    
    # If we found contact-specific content, replace the slider and everything between it and footer
    if contact_unique_content.strip():
        before_content = clean_contact[:content_start]
        after_footer = clean_contact[footer_start:]
        clean_contact = before_content + contact_unique_content.rstrip() + "\n\n    " + after_footer

# Write the clean contact.html
with open(contact_file, 'w', encoding='utf-8') as f:
    f.write(clean_contact)

print("✓ Rebuilt contact.html from index.html template")
print("  - Clean CSS structure")
print("  - Proper HTML hierarchy")
print("  - Preserved contact-specific sections")
