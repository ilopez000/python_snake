import tkinter as tk  # Importar la biblioteca tkinter para interfaces gráficas
import random  # Importar para generar números aleatorios

# Configuración básica del juego
ANCHO = 300  # Ancho del canvas
ALTO = 300  # Alto del canvas
TAMAÑO_SERPIENTE = 10  # Tamaño de cada segmento de la serpiente
TAMAÑO_COMIDA = 10  # Tamaño de la comida
TIEMPO_RETRASO = 500  # Tiempo de retraso en milisegundos para el movimiento de la serpiente

# Direcciones posibles para la serpiente
DIRECCIONES = {
    "Left": (-1, 0),
    "Right": (1, 0),
    "Up": (0, -1),
    "Down": (0, 1),
}

class JuegoSerpiente:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="black")  # Crear el canvas
        self.canvas.pack()

        self.serpiente = [(ANCHO // 2, ALTO // 2)]  # Posición inicial de la serpiente
        self.direccion = "Right"  # Dirección inicial
        self.comida = self.crear_comida()  # Crear la primera comida

        self.en_ejecucion = True  # El juego está en ejecución
        self.puntuacion = 0  # Puntuación inicial

        # Vincular las teclas de dirección al método de cambio de dirección
        self.root.bind("<KeyPress>", self.cambiar_direccion)

        self.actualizar()  # Iniciar la actualización del juego

    def crear_comida(self):
        # Crear comida en una posición aleatoria dentro del canvas
        x = random.randint(0, (ANCHO - TAMAÑO_COMIDA) // TAMAÑO_SERPIENTE) * TAMAÑO_SERPIENTE
        y = random.randint(0, (ALTO - TAMAÑO_COMIDA) // TAMAÑO_SERPIENTE) * TAMAÑO_SERPIENTE
        return (x, y)

    def cambiar_direccion(self, event):
        # Cambiar la dirección de la serpiente según la tecla presionada
        tecla = event.keysym  # Obtener la tecla presionada
        if tecla in DIRECCIONES:
            nueva_direccion = DIRECCIONES[tecla]
            direccion_actual = DIRECCIONES[self.direccion]

            # Evitar moverse en dirección opuesta a la actual
            if (
                nueva_direccion[0] != -direccion_actual[0]
                or nueva_direccion[1] != -direccion_actual[1]
            ):
                self.direccion = tecla

    def actualizar(self):
        if self.en_ejecucion:
            self.mover_serpiente()  # Mover la serpiente en la dirección actual
            if self.comprobar_colision():  # Verificar colisiones
                self.en_ejecucion = False
                self.fin_del_juego()  # Mostrar mensaje de fin del juego
            else:
                self.canvas.delete("all")  # Limpiar el canvas
                self.dibujar_serpiente()  # Dibujar la serpiente
                self.dibujar_comida()  # Dibujar la comida
                self.root.after(TIEMPO_RETRASO, self.actualizar)  # Llamar de nuevo después de un retraso

    def mover_serpiente(self):
        dx, dy = DIRECCIONES[self.direccion]  # Obtener el cambio en x e y según la dirección
        cabeza_x, cabeza_y = self.serpiente[0]  # Obtener la posición de la cabeza de la serpiente
        nueva_cabeza = (cabeza_x + dx * TAMAÑO_SERPIENTE, cabeza_y + dy * TAMAÑO_SERPIENTE)

        # Verificar si la serpiente comió la comida
        if nueva_cabeza == self.comida:
            self.serpiente.insert(0, nueva_cabeza)  # Agregar a la cabeza
            self.comida = self.crear_comida()  # Crear nueva comida
            self.puntuacion += 1  # Incrementar la puntuación
        else:
            self.serpiente.insert(0, nueva_cabeza)
            self.serpiente.pop()  # Eliminar la cola si no comió

    def comprobar_colision(self):
        cabeza_x, cabeza_y = self.serpiente[0]

        # Verificar colisiones con los bordes del canvas
        if cabeza_x < 0 or cabeza_x >= ANCHO or cabeza_y < 0 or cabeza_y >= ALTO:
            return True

        # Verificar colisiones consigo misma
        if self.serpiente[0] in self.serpiente[1:]:
            return True

        return False

    def dibujar_serpiente(self):
        for x, y in self.serpiente:
            self.canvas.create_rectangle(x, y, x + TAMAÑO_SERPIENTE, y + TAMAÑO_SERPIENTE, fill="green")

    def dibujar_comida(self):
        x, y = self.comida
        self.canvas.create_rectangle(x, y, x + TAMAÑO_COMIDA, y + TAMAÑO_COMIDA, fill="red")

    def fin_del_juego(self):
        # Mostrar mensaje de fin del juego en el canvas
        self.canvas.create_text(
            ANCHO // 2, ALTO // 2,
            text="Game Over",
            fill="white",
            font=("Helvetica", 16)
        )
        print(f"Game Over. Puntuación: {self.puntuacion}")

# Crear la ventana de tkinter y lanzar el juego
root = tk.Tk()
game = JuegoSerpiente(root)
root.mainloop()
