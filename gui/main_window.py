from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSpinBox, QSlider, QGroupBox, QFrame)
from PyQt5.QtCore import Qt
from models.simulator import Simulator
from gui.canvas import SimulationCanvas

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación SWR - Step With Replacement")
        self.setGeometry(50, 50, 1200, 850)
        
        # Crear simulador
        self.simulator = Simulator(grid_width=40, grid_height=40, step_size=1)
        
        # Crear interfaz
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel izquierdo (controles y estadísticas)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # Panel derecho (canvas solamente)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_panel.setLayout(right_layout)
        
        # Canvas de simulación (sin scroll)
        self.canvas = SimulationCanvas(self.simulator)
        right_layout.addWidget(self.canvas)
        
        main_layout.addWidget(right_panel, stretch=1)
        
    def create_left_panel(self):
        """Crea el panel izquierdo con controles y estadísticas"""
        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)
        panel.setMaximumWidth(350)
        panel.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Panel de control
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)
        
        # Panel de estadísticas
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)
        
        # Leyenda
        legend_panel = self.create_legend_panel()
        layout.addWidget(legend_panel)
        
        layout.addStretch()
        
        return panel
    
    def create_control_panel(self):
        """Crea el panel de controles"""
        group = QGroupBox("Controles")
        layout = QVBoxLayout()
        
        # Número de pasos máximo
        steps_layout = QHBoxLayout()
        steps_label = QLabel("Pasos válidos objetivo:")
        self.steps_spinbox = QSpinBox()
        self.steps_spinbox.setMinimum(1)
        self.steps_spinbox.setMaximum(1000)
        self.steps_spinbox.setValue(500)
        self.steps_spinbox.valueChanged.connect(self.on_steps_changed)
        
        steps_layout.addWidget(steps_label)
        steps_layout.addWidget(self.steps_spinbox)
        layout.addLayout(steps_layout)
        
        # Tamaño del paso
        step_size_layout = QHBoxLayout()
        step_size_label = QLabel("Tamaño del paso:")
        self.step_size_spinbox = QSpinBox()
        self.step_size_spinbox.setMinimum(1)
        self.step_size_spinbox.setMaximum(5)
        self.step_size_spinbox.setValue(1)
        self.step_size_spinbox.valueChanged.connect(self.on_step_size_changed)
        
        step_size_layout.addWidget(step_size_label)
        step_size_layout.addWidget(self.step_size_spinbox)
        layout.addLayout(step_size_layout)
        
        # Velocidad de animación
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Velocidad de animación:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(500)
        self.speed_slider.setValue(100)
        self.speed_slider.setInvertedAppearance(True)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        layout.addLayout(speed_layout)
        
        # Separador
        layout.addSpacing(10)
        
        # Botones en cuadrícula 2x2
        buttons_layout = QVBoxLayout()
        
        # Primera fila
        row1 = QHBoxLayout()
        self.btn_start = QPushButton("▶ Iniciar")
        self.btn_start.clicked.connect(self.start_simulation)
        self.btn_start.setMinimumHeight(40)
        
        self.btn_pause = QPushButton("⏸ Pausar")
        self.btn_pause.clicked.connect(self.pause_simulation)
        self.btn_pause.setEnabled(False)
        self.btn_pause.setMinimumHeight(40)
        
        row1.addWidget(self.btn_start)
        row1.addWidget(self.btn_pause)
        
        # Segunda fila
        row2 = QHBoxLayout()
        self.btn_step = QPushButton("⏭ Paso a Paso")
        self.btn_step.clicked.connect(self.step_simulation)
        self.btn_step.setMinimumHeight(40)
        
        self.btn_reset = QPushButton("🔄 Reiniciar")
        self.btn_reset.clicked.connect(self.reset_simulation)
        self.btn_reset.setMinimumHeight(40)
        
        row2.addWidget(self.btn_step)
        row2.addWidget(self.btn_reset)
        
        buttons_layout.addLayout(row1)
        buttons_layout.addLayout(row2)
        layout.addLayout(buttons_layout)
        
        group.setLayout(layout)
        return group
    
    def create_stats_panel(self):
        """Crea el panel de estadísticas"""
        group = QGroupBox("Estadísticas en Tiempo Real")
        layout = QVBoxLayout()
        
        self.label_valid_steps = QLabel("✓ Pasos válidos: 0")
        self.label_invalid_steps = QLabel("✗ Pasos inválidos: 0")
        self.label_total_attempts = QLabel("Total intentos: 0")
        self.label_efficiency = QLabel("Eficiencia: 0%")
        self.label_max_steps = QLabel("Objetivo: 500")
        self.label_status = QLabel("Estado: Listo")
        
        self.label_valid_steps.setStyleSheet("font-size: 13px; padding: 5px; color: green; font-weight: bold;")
        self.label_invalid_steps.setStyleSheet("font-size: 13px; padding: 5px; color: red; font-weight: bold;")
        self.label_total_attempts.setStyleSheet("font-size: 13px; padding: 5px;")
        self.label_efficiency.setStyleSheet("font-size: 13px; padding: 5px; color: blue;")
        self.label_max_steps.setStyleSheet("font-size: 13px; padding: 5px;")
        self.label_status.setStyleSheet("font-size: 14px; padding: 8px; font-weight: bold; background-color: #f0f0f0; border-radius: 5px;")
        
        layout.addWidget(self.label_valid_steps)
        layout.addWidget(self.label_invalid_steps)
        layout.addWidget(self.label_total_attempts)
        layout.addWidget(self.label_efficiency)
        layout.addWidget(self.label_max_steps)
        layout.addSpacing(10)
        layout.addWidget(self.label_status)
        
        group.setLayout(layout)
        return group
    
    def create_legend_panel(self):
        """Crea el panel de leyenda"""
        group = QGroupBox("Leyenda")
        layout = QVBoxLayout()
        
        legend_items = [
            ("🟢", "Posición inicial"),
            ("🔴", "Posición actual"),
            ("🔵", "Camino recorrido (puede superponerse)"),
            ("❌", "Intentos de salirse del grid (no cuentan)")
        ]
        
        for icon, text in legend_items:
            label = QLabel(f"{icon}  {text}")
            label.setStyleSheet("font-size: 11px; padding: 3px;")
            layout.addWidget(label)
        
        group.setLayout(layout)
        return group
    
    def on_steps_changed(self, value):
        """Callback cuando cambia el número de pasos"""
        self.simulator.set_max_steps(value)
        self.update_stats()
    
    def on_step_size_changed(self, value):
        """Callback cuando cambia el tamaño del paso"""
        # Solo permitir cambiar si la simulación no está corriendo
        if not self.canvas.timer.isActive():
            self.simulator.step_size = value
            self.simulator.particle.step_size = value
            self.canvas.update()
    
    def on_speed_changed(self, value):
        """Callback cuando cambia la velocidad"""
        self.canvas.set_animation_speed(value)
    
    def start_simulation(self):
        """Inicia la simulación automática"""
        self.simulator.set_max_steps(self.steps_spinbox.value())
        self.canvas.start_animation()
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_step.setEnabled(False)
        self.step_size_spinbox.setEnabled(False)  # Deshabilitar durante simulación
        self.label_status.setText("Estado: Simulando...")
        self.label_status.setStyleSheet("font-size: 14px; padding: 8px; font-weight: bold; background-color: #d4edda; color: #155724; border-radius: 5px;")
        
        # Conectar actualización de estadísticas
        self.canvas.timer.timeout.connect(self.update_stats)
    
    def pause_simulation(self):
        """Pausa la simulación"""
        self.canvas.stop_animation()
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_step.setEnabled(True)
        self.step_size_spinbox.setEnabled(True)  # Habilitar cuando pausa
        self.label_status.setText("Estado: Pausado")
        self.label_status.setStyleSheet("font-size: 14px; padding: 8px; font-weight: bold; background-color: #fff3cd; color: #856404; border-radius: 5px;")
    
    def step_simulation(self):
        """Ejecuta un paso manual"""
        result = self.simulator.step()
        self.canvas.update()
        self.update_stats()
        
        if result['finished']:
            self.on_simulation_finished()
    
    def reset_simulation(self):
        """Reinicia la simulación"""
        self.canvas.stop_animation()
        self.simulator.reset()
        self.simulator.set_max_steps(self.steps_spinbox.value())
        self.canvas.update()
        self.update_stats()
        
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_step.setEnabled(True)
        self.step_size_spinbox.setEnabled(True)  # Habilitar cuando reinicia
        self.label_status.setText("Estado: Listo")
        self.label_status.setStyleSheet("font-size: 14px; padding: 8px; font-weight: bold; background-color: #f0f0f0; border-radius: 5px;")
    
    def update_stats(self):
        """Actualiza las estadísticas en la interfaz"""
        stats = self.simulator.get_stats()
        
        self.label_valid_steps.setText(f"✓ Pasos válidos: {stats['valid_steps']}")
        self.label_invalid_steps.setText(f"✗ Pasos inválidos: {stats['invalid_steps']}")
        self.label_total_attempts.setText(f"Total intentos: {stats['total_attempts']}")
        self.label_max_steps.setText(f"Objetivo: {stats['max_steps']}")
        
        # Calcular eficiencia
        if stats['total_attempts'] > 0:
            efficiency = (stats['valid_steps'] / stats['total_attempts']) * 100
            self.label_efficiency.setText(f"Eficiencia: {efficiency:.1f}%")
        else:
            self.label_efficiency.setText("Eficiencia: 0%")
        
        if stats['is_finished']:
            self.on_simulation_finished()
    
    def on_simulation_finished(self):
        """Callback cuando la simulación termina"""
        self.canvas.stop_animation()
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(False)
        self.btn_step.setEnabled(False)
        self.step_size_spinbox.setEnabled(True)  # Habilitar cuando termina
        
        self.label_status.setText("Estado: ¡Simulación completada!")
        self.label_status.setStyleSheet("font-size: 14px; padding: 8px; font-weight: bold; background-color: #cce5ff; color: #004085; border-radius: 5px;")