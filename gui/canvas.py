from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

class SimulationCanvas(QWidget):
    """Widget personalizado para visualizar la simulación"""
    
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.cell_size = 15  # Tamaño de cada celda en píxeles
        self.setMinimumSize(600, 600)
        
        # Timer para animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)
        self.animation_speed = 100  # ms entre pasos
        
        # Para mostrar el último intento inválido temporalmente
        self.last_invalid_attempt = None
        self.show_invalid_timer = QTimer()
        self.show_invalid_timer.timeout.connect(self.clear_invalid_attempt)
        
    def set_animation_speed(self, speed):
        """Establece la velocidad de animación en ms"""
        self.animation_speed = speed
        if self.timer.isActive():
            self.timer.setInterval(speed)
    
    def start_animation(self):
        """Inicia la animación automática"""
        self.timer.start(self.animation_speed)
    
    def stop_animation(self):
        """Detiene la animación"""
        self.timer.stop()
    
    def animate_step(self):
        """Ejecuta un paso y actualiza la visualización"""
        result = self.simulator.step()
        
        # Si fue un intento inválido, mostrarlo temporalmente
        if not result['moved']:
            self.last_invalid_attempt = result.get('attempted_position')
            self.show_invalid_timer.start(200)  # Mostrar por 200ms
        
        self.update()
        
        if result['finished']:
            self.timer.stop()
    
    def clear_invalid_attempt(self):
        """Limpia el último intento inválido mostrado"""
        self.last_invalid_attempt = None
        self.show_invalid_timer.stop()
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el grid y la simulación"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo blanco para todo el widget
        painter.fillRect(0, 0, self.width(), self.height(), QColor(255, 255, 255))
        
        # Calcular dimensiones del grid
        width = self.simulator.grid_width * self.cell_size
        height = self.simulator.grid_height * self.cell_size
        
        # Centrar el grid en el widget
        offset_x = (self.width() - width) // 2
        offset_y = (self.height() - height) // 2
        
        # Dibujar fondo del grid
        painter.fillRect(offset_x, offset_y, width, height, QColor(250, 250, 250))
        
        # Dibujar grid
        self.draw_grid(painter, offset_x, offset_y)
        
        # Dibujar intentos inválidos permanentes
        self.draw_invalid_attempts(painter, offset_x, offset_y)
        
        # Dibujar camino
        self.draw_path(painter, offset_x, offset_y)
        
        # Dibujar último intento inválido (temporal, más visible)
        if self.last_invalid_attempt:
            self.draw_last_invalid(painter, offset_x, offset_y)
        
        # Dibujar partícula actual
        self.draw_particle(painter, offset_x, offset_y)
    
    def draw_grid(self, painter, offset_x, offset_y):
        """Dibuja el grid de fondo"""
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        
        for i in range(self.simulator.grid_width + 1):
            x = offset_x + i * self.cell_size
            painter.drawLine(x, offset_y, x, offset_y + self.simulator.grid_height * self.cell_size)
        
        for i in range(self.simulator.grid_height + 1):
            y = offset_y + i * self.cell_size
            painter.drawLine(offset_x, y, offset_x + self.simulator.grid_width * self.cell_size, y)
        
        # Dibujar borde del grid más grueso
        painter.setPen(QPen(QColor(100, 100, 100), 3))
        painter.drawRect(offset_x, offset_y, 
                        self.simulator.grid_width * self.cell_size,
                        self.simulator.grid_height * self.cell_size)
    
    def draw_invalid_attempts(self, painter, offset_x, offset_y):
        """Dibuja todos los intentos inválidos (fuera del grid)"""
        invalid_attempts = self.simulator.particle.get_invalid_attempts()
        
        for attempt in invalid_attempts:
            from_pos = attempt['from']
            to_pos = attempt['to']
            
            # Calcular coordenadas
            x1 = offset_x + from_pos[0] * self.cell_size + self.cell_size // 2
            y1 = offset_y + from_pos[1] * self.cell_size + self.cell_size // 2
            x2 = offset_x + to_pos[0] * self.cell_size + self.cell_size // 2
            y2 = offset_y + to_pos[1] * self.cell_size + self.cell_size // 2
            
            # Dibujar línea roja punteada para intentos inválidos
            painter.setPen(QPen(QColor(255, 100, 100, 150), 2, Qt.DashLine))
            painter.drawLine(x1, y1, x2, y2)
            
            # Dibujar X en el punto de intento inválido
            size = 6
            painter.setPen(QPen(QColor(255, 0, 0, 150), 2))
            painter.drawLine(x2 - size, y2 - size, x2 + size, y2 + size)
            painter.drawLine(x2 - size, y2 + size, x2 + size, y2 - size)
    
    def draw_last_invalid(self, painter, offset_x, offset_y):
        """Dibuja el último intento inválido de forma más visible"""
        pos = self.simulator.particle.get_position()
        
        x1 = offset_x + pos[0] * self.cell_size + self.cell_size // 2
        y1 = offset_y + pos[1] * self.cell_size + self.cell_size // 2
        x2 = offset_x + self.last_invalid_attempt[0] * self.cell_size + self.cell_size // 2
        y2 = offset_y + self.last_invalid_attempt[1] * self.cell_size + self.cell_size // 2
        
        # Línea roja sólida
        painter.setPen(QPen(QColor(255, 0, 0), 3, Qt.SolidLine))
        painter.drawLine(x1, y1, x2, y2)
        
        # X grande en el destino
        size = 8
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawLine(x2 - size, y2 - size, x2 + size, y2 + size)
        painter.drawLine(x2 - size, y2 + size, x2 + size, y2 - size)
    
    def draw_path(self, painter, offset_x, offset_y):
        """Dibuja el camino recorrido por la partícula"""
        path = self.simulator.get_path()
        
        if len(path) < 2:
            return
        
        # Dibujar líneas conectando el camino
        painter.setPen(QPen(QColor(100, 150, 255), 2, Qt.SolidLine))
        
        for i in range(len(path) - 1):
            x1 = offset_x + path[i][0] * self.cell_size + self.cell_size // 2
            y1 = offset_y + path[i][1] * self.cell_size + self.cell_size // 2
            x2 = offset_x + path[i + 1][0] * self.cell_size + self.cell_size // 2
            y2 = offset_y + path[i + 1][1] * self.cell_size + self.cell_size // 2
            painter.drawLine(x1, y1, x2, y2)
        
        # Dibujar puntos visitados con transparencia para ver superposiciones (SWR)
        painter.setBrush(QBrush(QColor(150, 200, 255, 150)))
        painter.setPen(QPen(QColor(50, 100, 200), 1))
        
        for pos in path[:-1]:  # Todos excepto la posición actual
            x = offset_x + pos[0] * self.cell_size + self.cell_size // 4
            y = offset_y + pos[1] * self.cell_size + self.cell_size // 4
            painter.drawEllipse(x, y, self.cell_size // 2, self.cell_size // 2)
    
    def draw_particle(self, painter, offset_x, offset_y):
        """Dibuja la posición actual de la partícula"""
        pos = self.simulator.particle.get_position()
        
        # Dibujar partícula
        painter.setBrush(QBrush(QColor(255, 100, 100)))
        painter.setPen(QPen(QColor(200, 0, 0), 2))
        
        x = offset_x + pos[0] * self.cell_size + self.cell_size // 4
        y = offset_y + pos[1] * self.cell_size + self.cell_size // 4
        painter.drawEllipse(x, y, self.cell_size // 2, self.cell_size // 2)
        
        # Dibujar punto de inicio
        if len(self.simulator.get_path()) > 0:
            start = self.simulator.get_path()[0]
            painter.setBrush(QBrush(QColor(100, 255, 100)))
            painter.setPen(QPen(QColor(0, 200, 0), 2))
            
            sx = offset_x + start[0] * self.cell_size + self.cell_size // 4
            sy = offset_y + start[1] * self.cell_size + self.cell_size // 4
            painter.drawEllipse(sx, sy, self.cell_size // 2, self.cell_size // 2)