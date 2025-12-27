#!/usr/bin/env python3
"""
Version Update Script
Automatically updates version numbers across the codebase
"""

import os
import re
import json
from datetime import datetime


class VersionUpdater:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.version_file = os.path.join(base_dir, 'versions.json')
        self.files_to_update = [
            'gui/main_window.py',
            'gui/feedback_dialog.py',
            'README.md',
            'CHANGELOG.md'
        ]
    
    def load_versions(self):
        """Load version configuration"""
        with open(self.version_file, 'r') as f:
            return json.load(f)
    
    def save_versions(self, data):
        """Save version configuration"""
        with open(self.version_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_file(self, filepath, old_version, new_version):
        """Update version in a specific file"""
        full_path = os.path.join(self.base_dir, filepath)
        
        if not os.path.exists(full_path):
            print(f"  ⚠ File not found: {filepath}")
            return False
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace version strings
        patterns = [
            (f'VERSION = "{old_version}"', f'VERSION = "{new_version}"'),
            (f"'version': '{old_version}'", f"'version': '{new_version}'"),
            (f'**Current Version:** {old_version}', f'**Current Version:** {new_version}'),
            (f'## [{old_version}]', f'## [{new_version}]')
        ]
        
        updated = False
        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                updated = True
        
        if updated:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Updated: {filepath}")
            return True
        
        return False
    
    def bump_version(self, new_version):
        """Bump version across all files"""
        print("=" * 60)
        print("Version Update")
        print("=" * 60)
        
        # Load current version
        versions = self.load_versions()
        old_version = versions['current_version']
        
        print(f"\nCurrent version: {old_version}")
        print(f"New version: {new_version}")
        
        # Update files
        print("\nUpdating files...")
        for filepath in self.files_to_update:
            self.update_file(filepath, old_version, new_version)
        
        # Update versions.json
        versions['current_version'] = new_version
        versions['version_history'].insert(0, {
            'version': new_version,
            'release_date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'release',
            'notes': f'Version {new_version} release'
        })
        
        self.save_versions(versions)
        print(f"  ✓ Updated: versions.json")
        
        print("\n" + "=" * 60)
        print(f"✅ Version updated to {new_version}")
        print("=" * 60)
        
        return True


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 0.100.030")
        sys.exit(1)
    
    new_version = sys.argv[1]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    updater = VersionUpdater(base_dir)
    updater.bump_version(new_version)


if __name__ == '__main__':
    main()
