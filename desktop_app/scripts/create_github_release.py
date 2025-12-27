#!/usr/bin/env python3
"""
GitHub Release Automation Script
Automatically creates GitHub releases with version tags
"""

import os
import sys
import json
import requests
from datetime import datetime


class GitHubReleaseManager:
    def __init__(self, repo_owner, repo_name, github_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_latest_release(self):
        """Get the latest release from GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def create_release(self, version, release_notes, prerelease=False):
        """Create a new GitHub release"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/releases"
        
        tag_name = f"v{version}"
        release_name = f"Arma Reforger Live Map v{version}"
        
        data = {
            "tag_name": tag_name,
            "target_commitish": "main",
            "name": release_name,
            "body": release_notes,
            "draft": False,
            "prerelease": prerelease
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"✓ Release {version} created successfully!")
            return response.json()
        else:
            print(f"✗ Failed to create release: {response.status_code}")
            print(f"  Error: {response.text}")
            return None
    
    def upload_asset(self, release_id, file_path, asset_name=None):
        """Upload an asset to a release"""
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            return None
        
        if not asset_name:
            asset_name = os.path.basename(file_path)
        
        url = f"https://uploads.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/{release_id}/assets"
        
        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"
        
        params = {"name": asset_name}
        
        with open(file_path, 'rb') as f:
            response = requests.post(url, headers=headers, params=params, data=f)
        
        if response.status_code == 201:
            print(f"✓ Asset uploaded: {asset_name}")
            return response.json()
        else:
            print(f"✗ Failed to upload asset: {response.status_code}")
            return None
    
    def delete_release(self, release_id):
        """Delete a release (use with caution)"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/releases/{release_id}"
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 204:
            print(f"✓ Release deleted: {release_id}")
            return True
        return False


def read_changelog(changelog_path, version):
    """Extract release notes from CHANGELOG.md for specific version"""
    if not os.path.exists(changelog_path):
        return f"Release version {version}"
    
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to find version section
    version_marker = f"## [{version}]"
    if version_marker in content:
        start = content.find(version_marker)
        # Find next version marker
        next_version = content.find("## [", start + len(version_marker))
        
        if next_version == -1:
            notes = content[start:]
        else:
            notes = content[start:next_version]
        
        return notes.strip()
    
    return f"Release version {version}\n\nSee CHANGELOG.md for details."


def main():
    print("=" * 60)
    print("GitHub Release Automation")
    print("=" * 60)
    
    # Get environment variables
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER')
    repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]
    version = os.environ.get('RELEASE_VERSION')
    changelog_path = os.environ.get('CHANGELOG_PATH', 'CHANGELOG.md')
    asset_path = os.environ.get('ASSET_PATH', '')
    prerelease = os.environ.get('PRERELEASE', 'false').lower() == 'true'
    
    # Validate inputs
    if not github_token:
        print("✗ Error: GITHUB_TOKEN not set")
        sys.exit(1)
    
    if not repo_owner or not repo_name:
        print("✗ Error: Repository information not available")
        sys.exit(1)
    
    if not version:
        print("✗ Error: RELEASE_VERSION not set")
        sys.exit(1)
    
    print(f"Repository: {repo_owner}/{repo_name}")
    print(f"Version: {version}")
    print(f"Prerelease: {prerelease}")
    
    # Initialize manager
    manager = GitHubReleaseManager(repo_owner, repo_name, github_token)
    
    # Read release notes from changelog
    print("\nReading release notes from CHANGELOG...")
    release_notes = read_changelog(changelog_path, version)
    print(f"✓ Release notes loaded ({len(release_notes)} chars)")
    
    # Create release
    print("\nCreating GitHub release...")
    release = manager.create_release(version, release_notes, prerelease)
    
    if not release:
        sys.exit(1)
    
    release_id = release['id']
    print(f"✓ Release ID: {release_id}")
    print(f"✓ Release URL: {release['html_url']}")
    
    # Upload asset if provided
    if asset_path and os.path.exists(asset_path):
        print(f"\nUploading asset: {asset_path}")
        asset = manager.upload_asset(release_id, asset_path)
        if asset:
            print(f"✓ Asset URL: {asset['browser_download_url']}")
    
    print("\n" + "=" * 60)
    print("✅ Release created successfully!")
    print("=" * 60)
    
    # Output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"release_id={release_id}\n")
        f.write(f"release_url={release['html_url']}\n")
        f.write(f"tag_name=v{version}\n")


if __name__ == '__main__':
    main()
