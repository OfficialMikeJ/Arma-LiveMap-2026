import { MarkerType } from '../types';

interface Props {
  visibleTypes: Set<MarkerType>;
  onToggleType: (type: MarkerType) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onClose: () => void;
}

const markerTypes: Array<{ type: MarkerType; label: string; color: string }> = [
  { type: 'enemy', label: 'Enemy', color: '#FF0000' },
  { type: 'friendly', label: 'Friendly', color: '#0066FF' },
  { type: 'attack', label: 'Attack', color: '#FF0000' },
  { type: 'defend', label: 'Defend', color: '#0066FF' },
  { type: 'pickup', label: 'Pickup', color: '#00FF00' },
  { type: 'drop', label: 'Drop', color: '#FF0000' },
  { type: 'meet', label: 'Meet', color: '#9933FF' },
  { type: 'infantry', label: 'Infantry', color: '#00FF00' },
  { type: 'armor', label: 'Armor', color: '#FFAA00' },
  { type: 'air', label: 'Air', color: '#66CCFF' },
  { type: 'naval', label: 'Naval', color: '#0066FF' },
  { type: 'objective', label: 'Objective', color: '#FFFF00' },
  { type: 'other', label: 'Other', color: '#808080' },
];

export default function FilterSidebar({
  visibleTypes,
  onToggleType,
  onSelectAll,
  onDeselectAll,
  onClose
}: Props) {
  return (
    <div className="w-64 bg-tactical-surface border-l border-tactical-border flex flex-col">
      <div className="p-4 border-b border-tactical-border flex items-center justify-between">
        <h3 className="font-bold text-military-500">Marker Filters</h3>
        <button
          onClick={onClose}
          className="text-tactical-text hover:text-white text-xl"
        >
          &times;
        </button>
      </div>

      <div className="p-4 space-y-2 flex-1 overflow-y-auto">
        {markerTypes.map(({ type, label, color }) => (
          <label
            key={type}
            className="flex items-center gap-2 p-2 rounded hover:bg-tactical-bg cursor-pointer"
          >
            <input
              type="checkbox"
              checked={visibleTypes.has(type)}
              onChange={() => onToggleType(type)}
              className="w-4 h-4"
            />
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: color }}
            />
            <span className="text-tactical-text">{label}</span>
          </label>
        ))}
      </div>

      <div className="p-4 border-t border-tactical-border space-y-2">
        <button
          onClick={onSelectAll}
          className="btn btn-secondary w-full"
        >
          Select All
        </button>
        <button
          onClick={onDeselectAll}
          className="btn btn-secondary w-full"
        >
          Deselect All
        </button>
      </div>
    </div>
  );
}
