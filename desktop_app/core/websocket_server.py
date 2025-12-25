import asyncio
import json
import websockets
from datetime import datetime


class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.markers = {}
        self.server = None
    
    async def register(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send existing markers to new client
        if self.markers:
            await websocket.send(json.dumps({
                'type': 'markers_sync',
                'markers': list(self.markers.values())
            }))
    
    async def unregister(self, websocket):
        """Unregister client"""
        self.clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast(self, message, exclude=None):
        """Broadcast message to all clients except sender"""
        if self.clients:
            tasks = []
            for client in self.clients:
                if client != exclude:
                    tasks.append(client.send(message))
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def handle_client(self, websocket, path):
        """Handle client connection"""
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data['type'] == 'marker_add':
                    marker = data['marker']
                    marker_id = f"{marker['user_id']}_{marker['timestamp']}"
                    marker['id'] = marker_id
                    self.markers[marker_id] = marker
                    
                    # Broadcast to all clients
                    await self.broadcast(json.dumps({
                        'type': 'marker_added',
                        'marker': marker
                    }), exclude=websocket)
                
                elif data['type'] == 'marker_remove':
                    marker_id = data['marker_id']
                    if marker_id in self.markers:
                        del self.markers[marker_id]
                        
                        # Broadcast to all clients
                        await self.broadcast(json.dumps({
                            'type': 'marker_removed',
                            'marker_id': marker_id
                        }), exclude=websocket)
                
                elif data['type'] == 'position_update':
                    # Broadcast position updates
                    await self.broadcast(json.dumps(data), exclude=websocket)
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start WebSocket server"""
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await asyncio.Future()
    
    def run(self):
        """Run server in event loop"""
        asyncio.run(self.start())
