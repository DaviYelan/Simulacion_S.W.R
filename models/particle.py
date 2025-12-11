import random

class Particle:
    """Clase que representa una partícula en una caminata aleatoria con reemplazo (SWR)"""
    
    def __init__(self, x, y, step_size=1):
        """
        Inicializa la partícula
        
        Args:
            x: Posición inicial en x
            y: Posición inicial en y
            step_size: Tamaño del paso
        """
        self.x = x
        self.y = y
        self.step_size = step_size
        self.path = [(x, y)]  # Historial de posiciones visitadas
        self.valid_steps = 0  # Pasos válidos dados (dentro del grid)
        self.invalid_steps = 0  # Pasos inválidos (intentos de salirse)
        self.invalid_attempts = []  # Lista de intentos inválidos para visualizar
        
    def get_random_move(self):
        """
        Genera un movimiento aleatorio en cualquiera de las 4 direcciones
        
        Returns:
            Tupla (dx, dy) con el movimiento aleatorio
        """
        moves = [
            (self.step_size, 0),   # Derecha
            (-self.step_size, 0),  # Izquierda
            (0, self.step_size),   # Abajo
            (0, -self.step_size)   # Arriba
        ]
        
        return random.choice(moves)
    
    def is_valid_position(self, x, y, grid_width, grid_height):
        """
        Verifica si una posición está dentro del grid
        
        Returns:
            True si la posición es válida, False si está fuera del grid
        """
        return 0 <= x < grid_width and 0 <= y < grid_height
    
    def move(self, grid_width, grid_height):
        """
        Intenta realizar un movimiento aleatorio
        Con SWR (Step With Replacement):
        - SIEMPRE intenta moverse aleatoriamente
        - Si el movimiento está dentro del grid: es VÁLIDO y se ejecuta
        - Si el movimiento sale del grid: es INVÁLIDO y NO se ejecuta (no cuenta)
        
        Returns:
            dict con información del movimiento: {
                'success': bool,
                'attempted_position': (x, y),
                'current_position': (x, y)
            }
        """
        # Generar movimiento aleatorio
        dx, dy = self.get_random_move()
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Verificar si el movimiento es válido (dentro del grid)
        if self.is_valid_position(new_x, new_y, grid_width, grid_height):
            # Movimiento VÁLIDO: actualizar posición
            self.x = new_x
            self.y = new_y
            self.path.append((self.x, self.y))
            self.valid_steps += 1
            return {
                'success': True,
                'attempted_position': (new_x, new_y),
                'current_position': (self.x, self.y)
            }
        else:
            # Movimiento INVÁLIDO: no se mueve, guardar intento para visualizar
            self.invalid_steps += 1
            self.invalid_attempts.append({
                'from': (self.x, self.y),
                'to': (new_x, new_y)
            })
            return {
                'success': False,
                'attempted_position': (new_x, new_y),
                'current_position': (self.x, self.y)
            }
    
    def reset(self, x, y):
        """Reinicia la partícula a una posición inicial"""
        self.x = x
        self.y = y
        self.path = [(x, y)]
        self.valid_steps = 0
        self.invalid_steps = 0
        self.invalid_attempts = []
    
    def get_position(self):
        """Retorna la posición actual"""
        return (self.x, self.y)
    
    def get_path(self):
        """Retorna el camino completo recorrido"""
        return self.path.copy()
    
    def get_invalid_attempts(self):
        """Retorna la lista de intentos inválidos"""
        return self.invalid_attempts.copy()
    
    def get_stats(self):
        """Retorna estadísticas de la partícula"""
        return {
            'valid_steps': self.valid_steps,
            'invalid_steps': self.invalid_steps,
            'total_attempts': self.valid_steps + self.invalid_steps
        }