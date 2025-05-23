import tkinter as tk

def create_main_window():
    """Creates and configures the main calculator window."""
    ventana = tk.Tk()
    ventana.title("Calculadora Simple")
    ventana.geometry("300x400")
    ventana.resizable(False, False)
    return ventana

def create_display(ventana):
    """Creates the entry field for displaying input and results."""
    pantalla = tk.Entry(ventana, width=20, font=('Arial', 14), justify="right")
    pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
    pantalla.insert(0, "0")
    return pantalla

def create_buttons(ventana, pantalla):
    """Creates the standard and advanced calculator buttons."""
    # Normal buttons
    botones_normales = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]

    fila = 1
    columna = 0
    for boton_texto in botones_normales:
        # Commands for these buttons will be set in operations.py
        tk.Button(ventana, text=boton_texto, width=5, height=2).grid(row=fila, column=columna)
        columna += 1
        if columna > 3:
            columna = 0
            fila += 1

    # Advanced buttons
    botones_avanzados = [
        ("√", 5, 0),
        ("x^y", 5, 1),
        ("∫", 5, 2),
        ("C", 5, 3)
    ]
    for text, row, col in botones_avanzados:
        # Commands for these buttons will be set in operations.py
        tk.Button(ventana, text=text, width=5, height=2).grid(row=row, column=col)