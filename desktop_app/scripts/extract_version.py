#!/usr/bin/env python3
"""
Extract version from code
Safe version extraction with proper encoding handling
"""

import sys
import re
import os

def extract_version(file_path):
    """Extract VERSION from Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find VERSION = "x.x.x" pattern
        match = re.search(r'VERSION\s*=\s*["\']([0-9.]+)["\']', content)
        
        if match:
            return match.group(1)
        else:
            print("Error: VERSION not found in file", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_version.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    version = extract_version(file_path)
    print(version)
