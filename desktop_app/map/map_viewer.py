from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPolygonItem
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QColor, QPen, QBrush, QPixmap, QPainter, QPolygonF, QWheelEvent
from datetime import datetime


class MapMarker:
    def __init__(self, marker_id, marker_type, x, y, user_id, description=""):
        self.id = marker_id
        self.type = marker_type
        self.x = x
        self.y = y
        self.user_id = user_id
        self.description = description
        self.timestamp = datetime.now().isoformat()


# Vanilla Arma Reforger marker types
ARMA_MARKER_TYPES = {
    'enemy': {'name': 'Enemy', 'color': QColor(220, 50, 50), 'shape': 'circle'},
    'friendly': {'name': 'Friendly', 'color': QColor(50, 150, 220), 'shape': 'circle'},
    'attack': {'name': 'Attack', 'color': QColor(220, 50, 50), 'shape': 'arrow'},
    'defend': {'name': 'Defend', 'color': QColor(50, 150, 220), 'shape': 'square'},
    'objective': {'name': 'Objective', 'color': QColor(220, 180, 50), 'shape': 'diamond'},
    'pickup': {'name': 'Pickup', 'color': QColor(100, 220, 100), 'shape': 'triangle_up'},
    'drop': {'name': 'Drop', 'color': QColor(220, 100, 100), 'shape': 'triangle_down'},
    'meet': {'name': 'Meet', 'color': QColor(150, 100, 220), 'shape': 'star'},
    'infantry': {'name': 'Infantry', 'color': QColor(100, 150, 100), 'shape': 'circle'},
    'armor': {'name': 'Armor', 'color': QColor(150, 150, 50), 'shape': 'square'},
    'air': {'name': 'Air', 'color': QColor(100, 180, 220), 'shape': 'triangle_up'},
    'naval': {'name': 'Naval', 'color': QColor(50, 100, 220), 'shape': 'diamond'},
    'other': {'name': 'Other', 'color': QColor(150, 150, 150), 'shape': 'circle'}
}


class MapViewer(QGraphicsView):
    marker_added = Signal(object)
    marker_removed = Signal(str)
    
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.markers = {}
        self.marker_mode = "enemy"
        self.zoom_level = 1.0
        self.marker_filters = {marker_type: True for marker_type in ARMA_MARKER_TYPES.keys()}
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Enable better scrolling and zooming
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Set background
        self.setStyleSheet("background-color: #0d0d0d;")
        
        self.load_default_map()
    
    def load_default_map(self):
        """Load default map (placeholder)"""
        # Create a simple grid as placeholder map
        self.scene.clear()
        self.markers.clear()
        
        # Create map bounds (10km x 10km grid)
        map_size = 4000
        self.scene.setSceneRect(0, 0, map_size, map_size)
        
        # Draw grid
        grid_pen = QPen(QColor(50, 50, 50))
        grid_spacing = 400
        
        for i in range(0, map_size + 1, grid_spacing):
            self.scene.addLine(i, 0, i, map_size, grid_pen)
            self.scene.addLine(0, i, map_size, i, grid_pen)
        
        # Add coordinate labels
        label_color = QColor(100, 100, 100)
        for i in range(0, map_size + 1, grid_spacing):
            label = self.scene.addText(f"{i//400}")
            label.setDefaultTextColor(label_color)
            label.setPos(i - 10, -30)
            
            label = self.scene.addText(f"{i//400}")
            label.setDefaultTextColor(label_color)
            label.setPos(-30, i - 10)
        
        # Add map title
        title = self.scene.addText("ARMA REFORGER - Live Map\n(Click to place enemy markers)")
        title.setDefaultTextColor(QColor(90, 122, 81))
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setPos(map_size / 2 - 200, -100)
    
    def load_map_image(self, image_path):
        """Load actual map image"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.scene.clear()
            self.markers.clear()
            self.scene.addPixmap(pixmap)
            self.scene.setSceneRect(pixmap.rect())
    
    def set_marker_mode(self, mode):
        """Set marker mode (enemy, friendly, objective, etc.)"""
        self.marker_mode = mode
    
    def zoom_in(self):
        """Zoom in on the map"""
        factor = 1.25
        self.zoom_level *= factor
        if self.zoom_level > 5.0:
            self.zoom_level = 5.0
            factor = 1.0
        self.scale(factor, factor)
    
    def zoom_out(self):
        """Zoom out on the map"""
        factor = 0.8
        self.zoom_level *= factor
        if self.zoom_level < 0.25:
            self.zoom_level = 0.25
            factor = 1.0
        self.scale(factor, factor)
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.resetTransform()
        self.zoom_level = 1.0
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming when Ctrl is pressed"""
        if event.modifiers() == Qt.ControlModifier:
            # Zoom with Ctrl + Mouse Wheel
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            # Normal scroll behavior
            super().wheelEvent(event)
    
    def set_marker_filter(self, marker_type, visible):
        """Set visibility filter for marker type"""
        self.marker_filters[marker_type] = visible
        self.apply_filters()
    
    def apply_filters(self):
        """Apply visibility filters to all markers"""
        for marker_id, marker_data in self.markers.items():
            marker_type = marker_data['marker'].type
            visible = self.marker_filters.get(marker_type, True)
            marker_data['item'].setVisible(visible)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Get scene position
            scene_pos = self.mapToScene(event.pos())
            
            # Check if clicking on existing marker to remove it
            items = self.scene.items(scene_pos)
            for item in items:
                if isinstance(item, QGraphicsEllipseItem) and hasattr(item, 'marker_id'):
                    self.remove_marker(item.marker_id)
                    return
            
            # Add new marker
            self.add_marker_at_position(scene_pos.x(), scene_pos.y())
        
        super().mousePressEvent(event)
    
    def add_marker_at_position(self, x, y):
        """Add marker at specified position"""
        marker_id = f"{self.user_id}_{datetime.now().timestamp()}"
        marker = MapMarker(marker_id, self.marker_mode, x, y, self.user_id)
        
        self.add_marker_visual(marker)
        self.marker_added.emit(marker)
    
    def add_marker_visual(self, marker):
        """Add visual marker to map"""
        if marker.id in self.markers:
            return
        
        # Determine color based on marker type
        if marker.type == "enemy":
            color = QColor(220, 50, 50)
        elif marker.type == "friendly":
            color = QColor(50, 150, 220)
        elif marker.type == "objective":
            color = QColor(220, 180, 50)
        else:
            color = QColor(150, 150, 150)
        
        # Create marker circle
        marker_item = QGraphicsEllipseItem(marker.x - 10, marker.y - 10, 20, 20)
        marker_item.setBrush(QBrush(color))
        marker_item.setPen(QPen(QColor(255, 255, 255), 2))
        marker_item.setZValue(100)
        marker_item.marker_id = marker.id
        
        self.scene.addItem(marker_item)
        self.markers[marker.id] = {'marker': marker, 'item': marker_item}
    
    def remove_marker(self, marker_id):
        """Remove marker from map"""
        if marker_id in self.markers:
            self.scene.removeItem(self.markers[marker_id]['item'])
            del self.markers[marker_id]
            self.marker_removed.emit(marker_id)
    
    def clear_all_markers(self):
        """Clear all markers"""
        for marker_data in list(self.markers.values()):
            self.scene.removeItem(marker_data['item'])
        self.markers.clear()
