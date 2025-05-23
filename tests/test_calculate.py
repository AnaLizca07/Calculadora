import pytest
from unittest.mock import patch, MagicMock
from src.operations import calculate
from src.ui import create_display, create_main_window
import tkinter as tk

def test_calculate_unit():
    """Prueba unitaria para la función calculate()."""
    # Configuración
    ventana = create_main_window()
    pantalla = create_display(ventana)
    
    # Caso 1: Suma básica
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "2+3")
    calculate(pantalla)
    assert pantalla.get() == "5"
    
    # Caso 2: División
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "10/2")
    calculate(pantalla)
    assert pantalla.get() == "5"
    
    # Caso 3: Expresión vacía
    pantalla.delete(0, tk.END)
    with patch('tkinter.messagebox.showerror') as mock_error:
        calculate(pantalla)
        mock_error.assert_called_once_with("ERROR", "La expresión está vacía")
    assert pantalla.get() == "0"
    
    # Caso 4: División por cero
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "5/0")
    with patch('tkinter.messagebox.showerror') as mock_error:
        calculate(pantalla)
        mock_error.assert_called_once_with("ERROR", "No es posible dividir entre cero")
    assert pantalla.get() == "0"
    
    # Caso 5: Operador al final
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "5+")
    with patch('tkinter.messagebox.showerror') as mock_error:
        calculate(pantalla)
        mock_error.assert_called_once_with("ERROR", "La expresión no puede terminar con un operador")