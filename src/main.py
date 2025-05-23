import tkinter as tk
from ui import create_main_window, create_display, create_buttons
from operations import setup_button_commands
from database import create_operations_table

def main():
    """
    Initializes the calculator application's components.
    Does NOT start the Tkinter event loop.
    Returns the main window (root) and display widget.
    """
    create_operations_table()
    ventana = create_main_window()
    pantalla = create_display(ventana)
    create_buttons(ventana, pantalla)
    setup_button_commands(ventana, pantalla)  # Assign commands to buttons
    return ventana, pantalla # Devuelve la ventana y la pantalla para que la prueba pueda interactuar con ellas.

if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando main.py se ejecuta directamente
    # (ej. python src/main.py en la terminal)
    root_window, _ = main() # Llama a main para construir la UI
    root_window.mainloop()  # Inicia el bucle de eventos solo cuando se ejecuta la app normalmente