import pytest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch, MagicMock
import sqlite3
import os
from pathlib import Path
from src.main import main
from src.database import create_operations_table, get_operations_history
from src.operations import setup_button_commands

@pytest.fixture(scope="module")
def setup_system():
    """Configuración inicial para la prueba de sistema con SQLite"""
    #! Configurar ruta de la base de datos de prueba
    test_db_path = Path(__file__).parent.parent / "src" / "test_calculadora.db"
    
    #! Configurar variable de entorno para usar la base de datos de prueba
    os.environ['CALCULADORA_DB_PATH'] = str(test_db_path)
    
    #! Crear tabla en la base de datos
    create_operations_table()
    
    yield
    
    #! Limpieza posterior - eliminar la base de datos de prueba
    try:
        os.remove(test_db_path)
    except FileNotFoundError:
        pass

def test_system_calculator(setup_system):
    """Prueba de sistema completa de la calculadora con SQLite"""
    #! Inicialización de la aplicación
    root = tk.Tk()
    with patch('tkinter.Tk', return_value=root):
        main()
    
    #! Obtener referencias a los componentes de la UI
    pantalla = None
    botones = {}
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Entry):
            pantalla = widget
        elif isinstance(widget, tk.Button):
            botones[widget.cget("text")] = widget
    
    #! Verificar que los componentes críticos existen
    assert pantalla is not None
    assert '7' in botones  # Botón numérico
    assert '+' in botones  # Operador básico
    assert '=' in botones  # Calcular
    assert '√' in botones  # Operación avanzada
    assert 'C' in botones  # Limpiar
    
    #! Prueba de operaciones básicas
    def simular_clic(boton_texto):
        botones[boton_texto].invoke()
    
    #* Test 1: Suma simple
    simular_clic('3')
    simular_clic('+')
    simular_clic('2')
    simular_clic('=')
    assert pantalla.get() == '5'
    
    #! Verificar que se guardó en la base de datos
    historial = get_operations_history(1)
    assert len(historial) == 1, f"Historial esperado: 1 operación, obtenido: {len(historial)}"
    assert historial[0][0] == '3+2'
    assert historial[0][1] == '5'
    
    #* Test 2: Limpiar pantalla
    simular_clic('C')
    assert pantalla.get() == '0'
    
    #* Test 3: Operación compleja
    simular_clic('1')
    simular_clic('0')
    simular_clic('*')
    simular_clic('2')
    simular_clic('+')
    simular_clic('3')
    simular_clic('=')
    assert pantalla.get() == '23'
    
    #! Verificar que se guardó la operación compleja
    historial = get_operations_history(2)
    assert len(historial) == 2
    assert historial[1][0] == '10*2+3'
    assert historial[1][1] == '23'
    
    #* 4. Prueba de manejo de errores
    
    #! División por cero
    simular_clic('C')
    simular_clic('5')
    simular_clic('/')
    simular_clic('0')
    with patch('tkinter.messagebox.showerror') as mock_error:
        simular_clic('=')
        mock_error.assert_called_once_with("ERROR", "No es posible dividir entre cero")
    assert pantalla.get() == '0'
    
    #* 5. Prueba de interfaz de usuario simple
    
    simular_clic('C')
    simular_clic('5')
    simular_clic('*')
    simular_clic('5')
    simular_clic('=')
    simular_clic('√')
    assert pantalla.get() == '5'
    
    #! Cerrar la aplicación
    root.destroy()