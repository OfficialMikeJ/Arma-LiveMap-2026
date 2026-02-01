import { User, WSStatus } from '../types';

interface Props {
  user: User;
  wsStatus: WSStatus;
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onZoomReset: () => void;
  onToggleFilters: () => void;
  onSettings: () => void;
  onFeedback: () => void;
  onLogout: () => void;
  onRefresh: () => void;
}

export default function ToolBar({
  user,
  wsStatus,
  zoom,
  onZoomIn,
  onZoomOut,
  onZoomReset,
  onToggleFilters,
  onSettings,
  onFeedback,
  onLogout,
  onRefresh
}: Props) {
  return (
    <div className="bg-tactical-surface border-b border-tactical-border px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold text-military-500">Arma Reforger Tactical Map</h1>
        <span className="text-tactical-text">v1.0.0</span>
      </div>

      <div className="flex items-center gap-2">
        {/* Zoom controls */}
        <button
          onClick={onZoomOut}
          className="btn btn-secondary px-3"
          title="Zoom Out"
        >
          −
        </button>
        <button
          onClick={onZoomReset}
          className="btn btn-secondary px-3"
          title="Reset Zoom"
        >
          ⟲ {Math.round(zoom * 100)}%
        </button>
        <button
          onClick={onZoomIn}
          className="btn btn-secondary px-3"
          title="Zoom In"
        >
          +
        </button>

        <div className="w-px h-6 bg-tactical-border mx-2" />

        {/* Actions */}
        <button
          onClick={onToggleFilters}
          className="btn btn-secondary"
          title="Toggle Filters"
        >
          🔍 Filters
        </button>

        <button
          onClick={onRefresh}
          className="btn btn-secondary"
          title="Refresh"
        >
          ↻ Refresh
        </button>

        <button
          onClick={onFeedback}
          className="btn btn-secondary"
          title="Send Feedback"
        >
          📝 Feedback
        </button>

        <button
          onClick={onSettings}
          className="btn btn-secondary"
          title="Settings"
        >
          ⚙ Settings
        </button>

        <div className="w-px h-6 bg-tactical-border mx-2" />

        {/* User info */}
        <div className="flex items-center gap-2 text-tactical-text">
          <span>{user.username}</span>
          <div className={`w-2 h-2 rounded-full ${wsStatus.connected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>

        <button
          onClick={onLogout}
          className="btn btn-danger"
          title="Logout"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
