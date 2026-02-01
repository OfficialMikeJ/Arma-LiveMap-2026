export interface User {
  id: number;
  username: string;
  hasTOTP: boolean;
}

export interface Marker {
  id: string;
  type: MarkerType;
  shape: MarkerShape;
  x: number;
  y: number;
  color: string;
  created_by: string;
  timestamp: string;
  notes?: string;
}

export type MarkerType = 
  | 'enemy'
  | 'friendly'
  | 'attack'
  | 'defend'
  | 'pickup'
  | 'drop'
  | 'meet'
  | 'infantry'
  | 'armor'
  | 'air'
  | 'naval'
  | 'objective'
  | 'other';

export type MarkerShape = 
  | 'circle'
  | 'square'
  | 'diamond'
  | 'triangle'
  | 'arrow'
  | 'star'
  | 'polygon';

export interface Server {
  id: number;
  name: string;
  ip_address: string;
  port: number;
  enabled: boolean;
}

export interface SecurityQuestion {
  question: string;
  answer: string;
}

export interface Feedback {
  type: 'bug' | 'feature' | 'suggestion';
  message: string;
  email?: string;
}

export interface WSStatus {
  connected: boolean;
  clients: number;
  port: number;
}

declare global {
  interface Window {
    electronAPI: {
      login: (username: string, password: string) => Promise<any>;
      register: (username: string, password: string, securityQuestions: SecurityQuestion[]) => Promise<any>;
      logout: (userId: number) => Promise<any>;
      enableTOTP: (userId: number) => Promise<any>;
      verifyTOTP: (userId: number, token: string) => Promise<any>;
      getAllMarkers: () => Promise<Marker[]>;
      addMarker: (marker: Marker) => Promise<boolean>;
      removeMarker: (markerId: string) => Promise<boolean>;
      getAllServers: () => Promise<Server[]>;
      saveServers: (servers: Server[]) => Promise<boolean>;
      submitFeedback: (feedback: Feedback) => Promise<boolean>;
      getWSStatus: () => Promise<WSStatus>;
      onMarkerUpdate: (callback: (data: any) => void) => void;
      removeMarkerUpdateListener: () => void;
    };
  }
}
