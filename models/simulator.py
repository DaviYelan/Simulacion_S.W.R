from models.particle import Particle

class Simulator:
    """Clase que maneja la simulación de la caminata aleatoria con reemplazo (SWR)"""
    
    def __init__(self, grid_width, grid_height, step_size=1):
        """
        Inicializa el simulador
        
        Args:
            grid_width: Ancho del grid
            grid_height: Alto del grid
            step_size: Tamaño del paso
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.step_size = step_size
        
        # Iniciar partícula en el centro
        start_x = grid_width // 2
        start_y = grid_height // 2
        self.particle = Particle(start_x, start_y, step_size)
        
        self.max_steps = 0
        self.is_running = False
        self.is_finished = False
        
    def set_max_steps(self, max_steps):
        """Establece el número máximo de pasos VÁLIDOS"""
        self.max_steps = max_steps
        
    def reset(self):
        """Reinicia la simulación"""
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.particle.reset(start_x, start_y)
        self.is_running = False
        self.is_finished = False
        
    def step(self):
        """
        Ejecuta un paso de la simulación usando SWR (Step With Replacement)
        
        Con SWR:
        - La partícula SIEMPRE intenta moverse aleatoriamente
        - Si el movimiento está dentro del grid: se cuenta como paso VÁLIDO
        - Si el movimiento sale del grid: NO se cuenta (paso inválido)
        - La simulación termina cuando alcanza el número de pasos VÁLIDOS deseado
        
        Returns:
            dict con información del paso: 
            {
                'moved': bool,              # Si la partícula se movió (paso válido)
                'position': (x, y),         # Posición actual
                'attempted_position': (x, y), # Posición que intentó alcanzar
                'valid_steps': int,         # Pasos válidos dados
                'invalid_steps': int,       # Intentos de salirse del grid
                'finished': bool            # Si alcanzó el objetivo
            }
        """
        if self.is_finished:
            stats = self.particle.get_stats()
            pos = self.particle.get_position()
            return {
                'moved': False,
                'position': pos,
                'attempted_position': pos,
                'valid_steps': stats['valid_steps'],
                'invalid_steps': stats['invalid_steps'],
                'finished': True
            }
        
        # Intentar moverse (SWR: siempre intenta, puede o no ser válido)
        move_result = self.particle.move(self.grid_width, self.grid_height)
        
        stats = self.particle.get_stats()
        
        # Verificar si alcanzó el máximo de pasos VÁLIDOS
        if stats['valid_steps'] >= self.max_steps:
            self.is_finished = True
        
        return {
            'moved': move_result['success'],
            'position': move_result['current_position'],
            'attempted_position': move_result['attempted_position'],
            'valid_steps': stats['valid_steps'],
            'invalid_steps': stats['invalid_steps'],
            'finished': self.is_finished
        }
    
    def get_path(self):
        """Retorna el camino completo de la partícula"""
        return self.particle.get_path()
    
    def get_stats(self):
        """Retorna estadísticas de la simulación"""
        particle_stats = self.particle.get_stats()
        return {
            'valid_steps': particle_stats['valid_steps'],
            'invalid_steps': particle_stats['invalid_steps'],
            'total_attempts': particle_stats['total_attempts'],
            'max_steps': self.max_steps,
            'is_finished': self.is_finished,
            'path_length': len(self.particle.path)
        }