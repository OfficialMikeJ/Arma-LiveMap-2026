import { MarkerType } from '../types';

interface Props {
  selectedType: MarkerType;
  onSelectType: (type: MarkerType) => void;
}

const markerTypes: Array<{ type: MarkerType; label: string; color: string }> = [
  { type: 'enemy', label: '🔴 Enemy', color: '#FF0000' },
  { type: 'friendly', label: '🔵 Friendly', color: '#0066FF' },
  { type: 'attack', label: '⚔️ Attack', color: '#FF0000' },
  { type: 'defend', label: '🛡️ Defend', color: '#0066FF' },
  { type: 'pickup', label: '🚁 Pickup', color: '#00FF00' },
  { type: 'drop', label: '📦 Drop', color: '#FF0000' },
  { type: 'meet', label: '⭐ Meet', color: '#9933FF' },
  { type: 'infantry', label: '🏃 Infantry', color: '#00FF00' },
  { type: 'armor', label: '🚜 Armor', color: '#FFAA00' },
  { type: 'air', label: '✈️ Air', color: '#66CCFF' },
  { type: 'naval', label: '⚓ Naval', color: '#0066FF' },
  { type: 'objective', label: '🎯 Objective', color: '#FFFF00' },
  { type: 'other', label: '⚪ Other', color: '#808080' },
];

export default function MarkerTypeSelector({ selectedType, onSelectType }: Props) {
  return (
    <div className="bg-tactical-surface border-b border-tactical-border px-4 py-2">
      <div className="flex items-center gap-2 overflow-x-auto">
        <span className="text-tactical-text font-medium mr-2">Select Marker:</span>
        {markerTypes.map(({ type, label, color }) => (
          <button
            key={type}
            onClick={() => onSelectType(type)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap ${
              selectedType === type
                ? 'bg-military-600 text-white'
                : 'bg-tactical-bg text-tactical-text hover:bg-tactical-border'
            }`}
            style={{
              borderLeft: `3px solid ${color}`
            }}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
