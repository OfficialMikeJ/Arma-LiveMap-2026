#!/usr/bin/env python3
"""
Standalone WebSocket server for Arma Reforger Live Map
Run this script to start the WebSocket server for real-time marker synchronization
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.websocket_server import WebSocketServer
import argparse


def main():
    parser = argparse.ArgumentParser(description='Arma Reforger Live Map WebSocket Server')
    parser.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8765, help='Server port (default: 8765)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("Arma Reforger Live Map - WebSocket Server")
    print("=" * 60)
    print(f"Starting server on {args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        server = WebSocketServer(host=args.host, port=args.port)
        server.run()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
