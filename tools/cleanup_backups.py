import os
from pathlib import Path

ROOT = r"c:\rexonweldsandtools"

deleted_files = []
total_deleted = 0

# Walk through all files
for root, dirs, files in os.walk(ROOT):
    for file in files:
        # Check if file is a backup file
        if file.endswith('.bak') or file.endswith('.bak2') or file.endswith('.bak3'):
            filepath = os.path.join(root, file)
            
            try:
                os.remove(filepath)
                deleted_files.append(filepath)
                total_deleted += 1
                print(f"✓ Deleted: {filepath}")
            
            except Exception as e:
                print(f"✗ Error deleting {filepath}: {e}")

print(f"\nDeleted files:")
for file in deleted_files:
    print(f"  - {file}")
print(f"\nTotal deleted: {total_deleted}")
