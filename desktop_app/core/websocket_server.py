import asyncio
import json
import websockets
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.markers = {}
        self.player_positions = {}
        self.server = None
    
    async def register(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send existing markers to new client
        if self.markers:
            await websocket.send(json.dumps({
                'type': 'markers_sync',
                'markers': list(self.markers.values())
            }))
            logger.info(f"Sent {len(self.markers)} markers to new client")
        
        # Send existing player positions to new client
        if self.player_positions:
            await websocket.send(json.dumps({
                'type': 'positions_sync',
                'positions': list(self.player_positions.values())
            }))
            logger.info(f"Sent {len(self.player_positions)} player positions to new client")
    
    async def unregister(self, websocket):
        """Unregister client"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
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
                message_type = data.get('type')
                
                if message_type == 'marker_add':
                    marker = data['marker']
                    marker_id = f"{marker['user_id']}_{marker['timestamp']}"
                    marker['id'] = marker_id
                    self.markers[marker_id] = marker
                    logger.info(f"Marker added: {marker_id} ({marker['type']})")
                    
                    # Broadcast to all clients
                    await self.broadcast(json.dumps({
                        'type': 'marker_added',
                        'marker': marker
                    }), exclude=websocket)
                
                elif message_type == 'marker_remove':
                    marker_id = data['marker_id']
                    if marker_id in self.markers:
                        del self.markers[marker_id]
                        logger.info(f"Marker removed: {marker_id}")
                        
                        # Broadcast to all clients
                        await self.broadcast(json.dumps({
                            'type': 'marker_removed',
                            'marker_id': marker_id
                        }), exclude=websocket)
                
                elif message_type == 'position_update':
                    # Store and broadcast position updates
                    player_data = data.get('player', {})
                    user_id = player_data.get('user_id')
                    if user_id:
                        self.player_positions[user_id] = player_data
                        await self.broadcast(json.dumps(data), exclude=websocket)
                        logger.debug(f"Position updated for user {user_id}")
                
                elif message_type == 'chat_message':
                    # Broadcast chat messages
                    logger.info(f"Chat message from {data.get('username', 'unknown')}: {data.get('message', '')[:50]}")
                    await self.broadcast(json.dumps(data), exclude=websocket)
                
                elif message_type == 'ping':
                    # Respond to ping with pong
                    await websocket.send(json.dumps({'type': 'pong', 'timestamp': data.get('timestamp')}))
                
                else:
                    logger.warning(f"Unknown message type: {message_type}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed normally")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {e}")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start WebSocket server"""
        self.server = await websockets.serve(
            self.handle_client, 
            self.host, 
            self.port,
            ping_interval=20,
            ping_timeout=10
        )
        logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        logger.info("Server ready to accept connections")
        await asyncio.Future()
    
    def run(self):
        """Run server in event loop"""
        asyncio.run(self.start())
