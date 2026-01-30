#!/usr/bin/env python3
"""
Auto-increment patch version
Used by GitHub Actions to automatically bump version on every push
"""

import sys
import re

def increment_version(version):
    """Increment the patch version
    
    Examples:
        0.099.024 -> 0.099.025
        0.100.030 -> 0.100.031
    """
    # Split version into parts
    parts = version.split('.')
    
    if len(parts) != 3:
        print(f"Error: Invalid version format: {version}", file=sys.stderr)
        sys.exit(1)
    
    major, minor, patch = parts
    
    # Increment patch
    new_patch = int(patch) + 1
    
    # Format with leading zeros to maintain width
    new_version = f"{major}.{minor}.{new_patch:03d}"
    
    return new_version

def update_version_in_file(file_path, old_version, new_version):
    """Update version in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace version
        patterns = [
            (f'VERSION = "{old_version}"', f'VERSION = "{new_version}"'),
            (f"VERSION = '{old_version}'", f"VERSION = '{new_version}'"),
            (f"'version': '{old_version}'", f"'version': '{new_version}'"),
        ]
        
        for old_pattern, new_pattern in patterns:
            content = content.replace(old_pattern, new_pattern)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python auto_increment_version.py <current_version>")
        sys.exit(1)
    
    current_version = sys.argv[1]
    new_version = increment_version(current_version)
    
    # Update files
    files_updated = 0
    
    if update_version_in_file('gui/main_window.py', current_version, new_version):
        files_updated += 1
    
    if update_version_in_file('gui/feedback_dialog.py', current_version, new_version):
        files_updated += 1
    
    # Output new version for GitHub Actions
    print(new_version)
