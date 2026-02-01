import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  // Auth
  login: (username: string, password: string) => ipcRenderer.invoke('auth:login', username, password),
  register: (username: string, password: string, securityQuestions: any[]) => 
    ipcRenderer.invoke('auth:register', username, password, securityQuestions),
  logout: (userId: number) => ipcRenderer.invoke('auth:logout', userId),
  enableTOTP: (userId: number) => ipcRenderer.invoke('auth:enableTOTP', userId),
  verifyTOTP: (userId: number, token: string) => ipcRenderer.invoke('auth:verifyTOTP', userId, token),

  // Markers
  getAllMarkers: () => ipcRenderer.invoke('markers:getAll'),
  addMarker: (marker: any) => ipcRenderer.invoke('markers:add', marker),
  removeMarker: (markerId: string) => ipcRenderer.invoke('markers:remove', markerId),

  // Servers
  getAllServers: () => ipcRenderer.invoke('servers:getAll'),
  saveServers: (servers: any[]) => ipcRenderer.invoke('servers:save', servers),

  // Feedback
  submitFeedback: (feedback: any) => ipcRenderer.invoke('feedback:submit', feedback),

  // WebSocket
  getWSStatus: () => ipcRenderer.invoke('ws:getStatus'),

  // Event listeners
  onMarkerUpdate: (callback: (data: any) => void) => {
    ipcRenderer.on('marker:update', (_event, data) => callback(data));
  },
  removeMarkerUpdateListener: () => {
    ipcRenderer.removeAllListeners('marker:update');
  }
});
