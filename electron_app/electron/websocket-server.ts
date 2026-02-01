import * as WebSocket from 'ws';
import { EventEmitter } from 'events';

export class WebSocketServer extends EventEmitter {
  private wss: WebSocket.Server | null = null;
  private port: number;
  private clients: Set<WebSocket> = new Set();

  constructor(port: number) {
    super();
    this.port = port;
    this.start();
  }

  start() {
    try {
      this.wss = new WebSocket.Server({ port: this.port });

      this.wss.on('connection', (ws: WebSocket) => {
        console.log('New WebSocket client connected');
        this.clients.add(ws);

        ws.on('message', (message: string) => {
          try {
            const data = JSON.parse(message.toString());
            this.handleMessage(data, ws);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        });

        ws.on('close', () => {
          console.log('WebSocket client disconnected');
          this.clients.delete(ws);
        });

        ws.on('error', (error) => {
          console.error('WebSocket error:', error);
          this.clients.delete(ws);
        });

        // Send welcome message
        ws.send(JSON.stringify({
          type: 'connected',
          message: 'Connected to Tactical Map WebSocket Server',
          clients: this.clients.size
        }));
      });

      console.log(`WebSocket server running on port ${this.port}`);
    } catch (error) {
      console.error('Failed to start WebSocket server:', error);
    }
  }

  private handleMessage(data: any, sender: WebSocket) {
    // Broadcast marker updates to all clients except sender
    if (data.type === 'marker') {
      this.broadcastToOthers(data, sender);
      this.emit('marker', data);
    }
  }

  broadcastMarker(action: 'add' | 'remove', marker: any) {
    const message = JSON.stringify({
      type: 'marker',
      action,
      data: marker,
      timestamp: new Date().toISOString()
    });

    this.broadcast(message);
  }

  private broadcast(message: string) {
    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  }

  private broadcastToOthers(data: any, sender: WebSocket) {
    const message = JSON.stringify(data);
    this.clients.forEach((client) => {
      if (client !== sender && client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  }

  getClientCount(): number {
    return this.clients.size;
  }

  isRunning(): boolean {
    return this.wss !== null;
  }

  stop() {
    if (this.wss) {
      this.clients.forEach((client) => {
        client.close();
      });
      this.wss.close();
      this.wss = null;
      console.log('WebSocket server stopped');
    }
  }
}
