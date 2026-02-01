import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import { DatabaseService } from './database';
import { WebSocketServer } from './websocket-server';
import { AuthService } from './auth';

let mainWindow: BrowserWindow | null = null;
let dbService: DatabaseService;
let wsServer: WebSocketServer;
let authService: AuthService;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    backgroundColor: '#1a1a1a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    title: 'Arma Reforger Tactical Map v1.0.0',
    icon: path.join(__dirname, '../../build/icon.ico')
  });

  // Load the app
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  // Initialize services
  dbService = new DatabaseService(path.join(app.getPath('userData'), 'tacmap.db'));
  authService = new AuthService(dbService);
  wsServer = new WebSocketServer(8765);

  // Setup IPC handlers
  setupIPCHandlers();

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    wsServer.stop();
    dbService.close();
    app.quit();
  }
});

function setupIPCHandlers() {
  // Auth handlers
  ipcMain.handle('auth:login', async (event, username: string, password: string) => {
    return await authService.login(username, password);
  });

  ipcMain.handle('auth:register', async (event, username: string, password: string, securityQuestions: any[]) => {
    return await authService.register(username, password, securityQuestions);
  });

  ipcMain.handle('auth:logout', async (event, userId: number) => {
    return await authService.logout(userId);
  });

  ipcMain.handle('auth:enableTOTP', async (event, userId: number) => {
    return await authService.enableTOTP(userId);
  });

  ipcMain.handle('auth:verifyTOTP', async (event, userId: number, token: string) => {
    return await authService.verifyTOTP(userId, token);
  });

  // Marker handlers
  ipcMain.handle('markers:getAll', async () => {
    return dbService.getAllMarkers();
  });

  ipcMain.handle('markers:add', async (event, marker: any) => {
    const result = dbService.addMarker(marker);
    if (result) {
      wsServer.broadcastMarker('add', marker);
    }
    return result;
  });

  ipcMain.handle('markers:remove', async (event, markerId: string) => {
    const result = dbService.removeMarker(markerId);
    if (result) {
      wsServer.broadcastMarker('remove', { id: markerId });
    }
    return result;
  });

  // Server configuration handlers
  ipcMain.handle('servers:getAll', async () => {
    return dbService.getAllServers();
  });

  ipcMain.handle('servers:save', async (event, servers: any[]) => {
    return dbService.saveServers(servers);
  });

  // Feedback handlers
  ipcMain.handle('feedback:submit', async (event, feedback: any) => {
    return dbService.saveFeedback(feedback);
  });

  // WebSocket status
  ipcMain.handle('ws:getStatus', async () => {
    return {
      connected: wsServer.isRunning(),
      clients: wsServer.getClientCount(),
      port: 8765
    };
  });
}

// Handle marker updates from WebSocket
wsServer.on('marker', (data: any) => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send('marker:update', data);
  }
});
