import { useRef, useEffect, useState } from 'react';
import { Marker } from '../types';

interface Props {
  markers: Marker[];
  zoom: number;
  onAddMarker: (x: number, y: number) => void;
  onRemoveMarker: (markerId: string) => void;
}

export default function MapCanvas({ markers, zoom, onAddMarker, onRemoveMarker }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [panOffset, setPanOffset] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [lastMouse Pos, setLastMousePos] = useState({ x: 0, y: 0 });

  const MAP_WIDTH = 8000;
  const MAP_HEIGHT = 8000;
  const MARKER_SIZE = 20;

  useEffect(() => {
    drawMap();
  }, [markers, zoom, panOffset]);

  const drawMap = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();

    // Apply zoom and pan
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    ctx.translate(centerX + panOffset.x, centerY + panOffset.y);
    ctx.scale(zoom, zoom);
    ctx.translate(-centerX, -centerY);

    // Draw grid
    drawGrid(ctx, canvas);

    // Draw markers
    markers.forEach(marker => {
      drawMarker(ctx, marker, canvas);
    });

    ctx.restore();
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    const gridSize = 500;
    ctx.strokeStyle = '#2d2d2d';
    ctx.lineWidth = 1;

    // Vertical lines
    for (let x = 0; x <= MAP_WIDTH; x += gridSize) {
      const screenX = (x / MAP_WIDTH) * canvas.width;
      ctx.beginPath();
      ctx.moveTo(screenX, 0);
      ctx.lineTo(screenX, canvas.height);
      ctx.stroke();
    }

    // Horizontal lines
    for (let y = 0; y <= MAP_HEIGHT; y += gridSize) {
      const screenY = (y / MAP_HEIGHT) * canvas.height;
      ctx.beginPath();
      ctx.moveTo(0, screenY);
      ctx.lineTo(canvas.width, screenY);
      ctx.stroke();
    }
  };

  const drawMarker = (ctx: CanvasRenderingContext2D, marker: Marker, canvas: HTMLCanvasElement) => {
    const screenX = (marker.x / MAP_WIDTH) * canvas.width;
    const screenY = (marker.y / MAP_HEIGHT) * canvas.height;

    ctx.fillStyle = marker.color;
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 2;

    // Draw based on shape
    switch (marker.shape) {
      case 'circle':
        ctx.beginPath();
        ctx.arc(screenX, screenY, MARKER_SIZE / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        break;

      case 'square':
        ctx.fillRect(screenX - MARKER_SIZE / 2, screenY - MARKER_SIZE / 2, MARKER_SIZE, MARKER_SIZE);
        ctx.strokeRect(screenX - MARKER_SIZE / 2, screenY - MARKER_SIZE / 2, MARKER_SIZE, MARKER_SIZE);
        break;

      case 'diamond':
        ctx.beginPath();
        ctx.moveTo(screenX, screenY - MARKER_SIZE / 2);
        ctx.lineTo(screenX + MARKER_SIZE / 2, screenY);
        ctx.lineTo(screenX, screenY + MARKER_SIZE / 2);
        ctx.lineTo(screenX - MARKER_SIZE / 2, screenY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;

      case 'triangle':
        ctx.beginPath();
        ctx.moveTo(screenX, screenY - MARKER_SIZE / 2);
        ctx.lineTo(screenX + MARKER_SIZE / 2, screenY + MARKER_SIZE / 2);
        ctx.lineTo(screenX - MARKER_SIZE / 2, screenY + MARKER_SIZE / 2);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;

      case 'star':
        drawStar(ctx, screenX, screenY, 5, MARKER_SIZE / 2, MARKER_SIZE / 4);
        ctx.fill();
        ctx.stroke();
        break;

      case 'arrow':
        ctx.beginPath();
        ctx.moveTo(screenX, screenY - MARKER_SIZE / 2);
        ctx.lineTo(screenX + MARKER_SIZE / 3, screenY);
        ctx.lineTo(screenX + MARKER_SIZE / 6, screenY);
        ctx.lineTo(screenX + MARKER_SIZE / 6, screenY + MARKER_SIZE / 2);
        ctx.lineTo(screenX - MARKER_SIZE / 6, screenY + MARKER_SIZE / 2);
        ctx.lineTo(screenX - MARKER_SIZE / 6, screenY);
        ctx.lineTo(screenX - MARKER_SIZE / 3, screenY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        break;

      default:
        ctx.beginPath();
        ctx.arc(screenX, screenY, MARKER_SIZE / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    }
  };

  const drawStar = (ctx: CanvasRenderingContext2D, cx: number, cy: number, spikes: number, outerRadius: number, innerRadius: number) => {
    let rot = Math.PI / 2 * 3;
    let x = cx;
    let y = cy;
    const step = Math.PI / spikes;

    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);
    for (let i = 0; i < spikes; i++) {
      x = cx + Math.cos(rot) * outerRadius;
      y = cy + Math.sin(rot) * outerRadius;
      ctx.lineTo(x, y);
      rot += step;

      x = cx + Math.cos(rot) * innerRadius;
      y = cy + Math.sin(rot) * innerRadius;
      ctx.lineTo(x, y);
      rot += step;
    }
    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (isPanning) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Check if clicked on existing marker
    const clickedMarker = findMarkerAtPosition(clickX, clickY, canvas);
    if (clickedMarker) {
      onRemoveMarker(clickedMarker.id);
      return;
    }

    // Add new marker
    // Transform screen coordinates to map coordinates
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    const transformedX = (clickX - centerX - panOffset.x) / zoom + centerX;
    const transformedY = (clickY - centerY - panOffset.y) / zoom + centerY;

    const mapX = (transformedX / canvas.width) * MAP_WIDTH;
    const mapY = (transformedY / canvas.height) * MAP_HEIGHT;

    if (mapX >= 0 && mapX <= MAP_WIDTH && mapY >= 0 && mapY <= MAP_HEIGHT) {
      onAddMarker(mapX, mapY);
    }
  };

  const findMarkerAtPosition = (x: number, y: number, canvas: HTMLCanvasElement): Marker | null => {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    const transformedX = (x - centerX - panOffset.x) / zoom + centerX;
    const transformedY = (y - centerY - panOffset.y) / zoom + centerY;

    for (const marker of markers) {
      const markerScreenX = (marker.x / MAP_WIDTH) * canvas.width;
      const markerScreenY = (marker.y / MAP_HEIGHT) * canvas.height;

      const distance = Math.sqrt(
        Math.pow(transformedX - markerScreenX, 2) + Math.pow(transformedY - markerScreenY, 2)
      );

      if (distance <= MARKER_SIZE / 2) {
        return marker;
      }
    }

    return null;
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (e.button === 2 || e.ctrlKey) { // Right click or Ctrl+click
      setIsPanning(true);
      setLastMousePos({ x: e.clientX, y: e.clientY });
      e.preventDefault();
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (isPanning) {
      const deltaX = e.clientX - lastMousePos.x;
      const deltaY = e.clientY - lastMousePos.y;
      setPanOffset(prev => ({ x: prev.x + deltaX, y: prev.y + deltaY }));
      setLastMousePos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseUp = () => {
    setIsPanning(false);
  };

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
  };

  return (
    <canvas
      ref={canvasRef}
      width={1200}
      height={800}
      className="w-full h-full cursor-crosshair"
      onClick={handleCanvasClick}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onContextMenu={handleContextMenu}
    />
  );
}
