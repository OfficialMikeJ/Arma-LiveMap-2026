import { useState, useEffect, useRef } from 'react';
import { User, Marker, MarkerType, WSStatus } from '../types';
import MapCanvas from '../components/MapCanvas';
import MarkerTypeSelector from '../components/MarkerTypeSelector';
import ToolBar from '../components/ToolBar';
import FilterSidebar from '../components/FilterSidebar';

interface Props {
  user: User;
  onLogout: () => void;
}

export default function MapPage({ user, onLogout }: Props) {
  const [markers, setMarkers] = useState<Marker[]>([]);
  const [selectedMarkerType, setSelectedMarkerType] = useState<MarkerType>('enemy');
  const [wsStatus, setWsStatus] = useState<WSStatus>({ connected: false, clients: 0, port: 8765 });
  const [showFilters, setShowFilters] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const [zoom, setZoom] = useState(1);
  const [visibleMarkerTypes, setVisibleMarkerTypes] = useState<Set<MarkerType>>(new Set([
    'enemy', 'friendly', 'attack', 'defend', 'pickup', 'drop', 'meet',
    'infantry', 'armor', 'air', 'naval', 'objective', 'other'
  ]));

  useEffect(() => {
    // Load markers
    loadMarkers();

    // Get WebSocket status
    updateWSStatus();

    // Listen for marker updates from WebSocket
    window.electronAPI.onMarkerUpdate((data) => {
      if (data.action === 'add') {
        setMarkers(prev => [...prev, data.data]);
      } else if (data.action === 'remove') {
        setMarkers(prev => prev.filter(m => m.id !== data.data.id));
      }
    });

    // Cleanup
    return () => {
      window.electronAPI.removeMarkerUpdateListener();
    };
  }, []);

  const loadMarkers = async () => {
    const allMarkers = await window.electronAPI.getAllMarkers();
    setMarkers(allMarkers);
  };

  const updateWSStatus = async () => {
    const status = await window.electronAPI.getWSStatus();
    setWsStatus(status);
  };

  const handleAddMarker = async (x: number, y: number) => {
    const marker: Marker = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type: selectedMarkerType,
      shape: getShapeForMarkerType(selectedMarkerType),
      x,
      y,
      color: getColorForMarkerType(selectedMarkerType),
      created_by: user.username,
      timestamp: new Date().toISOString()
    };

    const success = await window.electronAPI.addMarker(marker);
    if (success) {
      setMarkers(prev => [...prev, marker]);
    }
  };

  const handleRemoveMarker = async (markerId: string) => {
    const success = await window.electronAPI.removeMarker(markerId);
    if (success) {
      setMarkers(prev => prev.filter(m => m.id !== markerId));
    }
  };

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 0.25, 5));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 0.25, 0.25));
  };

  const handleZoomReset = () => {
    setZoom(1);
  };

  const handleToggleMarkerType = (type: MarkerType) => {
    setVisibleMarkerTypes(prev => {
      const newSet = new Set(prev);
      if (newSet.has(type)) {
        newSet.delete(type);
      } else {
        newSet.add(type);
      }
      return newSet;
    });
  };

  const handleSelectAll = () => {
    setVisibleMarkerTypes(new Set([
      'enemy', 'friendly', 'attack', 'defend', 'pickup', 'drop', 'meet',
      'infantry', 'armor', 'air', 'naval', 'objective', 'other'
    ]));
  };

  const handleDeselectAll = () => {
    setVisibleMarkerTypes(new Set());
  };

  const filteredMarkers = markers.filter(m => visibleMarkerTypes.has(m.type));

  return (
    <div className="w-full h-full flex flex-col bg-tactical-bg">
      {/* Toolbar */}
      <ToolBar
        user={user}
        wsStatus={wsStatus}
        zoom={zoom}
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onZoomReset={handleZoomReset}
        onToggleFilters={() => setShowFilters(!showFilters)}
        onSettings={() => setShowSettings(true)}
        onFeedback={() => setShowFeedback(true)}
        onLogout={onLogout}
        onRefresh={() => {
          loadMarkers();
          updateWSStatus();
        }}
      />

      <div className="flex-1 flex overflow-hidden">
        {/* Main map area */}
        <div className="flex-1 flex flex-col">
          {/* Marker type selector */}
          <MarkerTypeSelector
            selectedType={selectedMarkerType}
            onSelectType={setSelectedMarkerType}
          />

          {/* Map canvas */}
          <div className="flex-1 relative">
            <MapCanvas
              markers={filteredMarkers}
              zoom={zoom}
              onAddMarker={handleAddMarker}
              onRemoveMarker={handleRemoveMarker}
            />
          </div>

          {/* Status bar */}
          <div className="bg-tactical-surface border-t border-tactical-border px-4 py-2 flex items-center justify-between text-sm text-tactical-text">
            <div>
              Markers: {filteredMarkers.length} / {markers.length}
            </div>
            <div>
              Zoom: {Math.round(zoom * 100)}%
            </div>
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${wsStatus.connected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span>{wsStatus.connected ? 'Connected' : 'Disconnected'} ({wsStatus.clients} users)</span>
            </div>
          </div>
        </div>

        {/* Filter sidebar */}
        {showFilters && (
          <FilterSidebar
            visibleTypes={visibleMarkerTypes}
            onToggleType={handleToggleMarkerType}
            onSelectAll={handleSelectAll}
            onDeselectAll={handleDeselectAll}
            onClose={() => setShowFilters(false)}
          />
        )}
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <SettingsModal
          onClose={() => setShowSettings(false)}
        />
      )}

      {/* Feedback Modal */}
      {showFeedback && (
        <FeedbackModal
          onClose={() => setShowFeedback(false)}
        />
      )}
    </div>
  );
}

function getShapeForMarkerType(type: MarkerType): string {
  const shapeMap: Record<MarkerType, string> = {
    enemy: 'circle',
    friendly: 'circle',
    attack: 'arrow',
    defend: 'square',
    pickup: 'triangle',
    drop: 'triangle',
    meet: 'star',
    infantry: 'circle',
    armor: 'square',
    air: 'triangle',
    naval: 'diamond',
    objective: 'diamond',
    other: 'circle'
  };
  return shapeMap[type] || 'circle';
}

function getColorForMarkerType(type: MarkerType): string {
  const colorMap: Record<MarkerType, string> = {
    enemy: '#FF0000',
    friendly: '#0066FF',
    attack: '#FF0000',
    defend: '#0066FF',
    pickup: '#00FF00',
    drop: '#FF0000',
    meet: '#9933FF',
    infantry: '#00FF00',
    armor: '#FFAA00',
    air: '#66CCFF',
    naval: '#0066FF',
    objective: '#FFFF00',
    other: '#808080'
  };
  return colorMap[type] || '#808080';
}

// Placeholder modals - will implement fully later
function SettingsModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="card w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-military-500">Settings</h2>
          <button onClick={onClose} className="text-tactical-text hover:text-white text-2xl">&times;</button>
        </div>
        <p className="text-tactical-text">Settings coming soon...</p>
      </div>
    </div>
  );
}

function FeedbackModal({ onClose }: { onClose: () => void }) {
  const [type, setType] = useState<'bug' | 'feature' | 'suggestion'>('bug');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await window.electronAPI.submitFeedback({ type, message, email });
    if (success) {
      setSubmitted(true);
      setTimeout(() => onClose(), 2000);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="card w-full max-w-2xl">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-military-500">📝 Feedback</h2>
          <button onClick={onClose} className="text-tactical-text hover:text-white text-2xl">&times;</button>
        </div>

        {submitted ? (
          <div className="text-center text-green-400 py-8">
            ✓ Thank you for your feedback!
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-tactical-text mb-2">Type</label>
              <select className="input" value={type} onChange={(e) => setType(e.target.value as any)}>
                <option value="bug">Bug Report</option>
                <option value="feature">Feature Request</option>
                <option value="suggestion">Suggestion</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-tactical-text mb-2">Message</label>
              <textarea
                className="input h-32 resize-none"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
                placeholder="Describe your feedback..."
              />
            </div>

            <div className="mb-4">
              <label className="block text-tactical-text mb-2">Email (Optional)</label>
              <input
                type="email"
                className="input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
              />
            </div>

            <button type="submit" className="btn btn-primary w-full">Submit Feedback</button>
          </form>
        )}

        <div className="mt-4 pt-4 border-t border-tactical-border">
          <a
            href="https://discord.gg/ykkkjwDnAD"
            target="_blank"
            rel="noopener noreferrer"
            className="text-military-500 hover:text-military-400"
          >
            Join our Discord Community →
          </a>
        </div>
      </div>
    </div>
  );
}
