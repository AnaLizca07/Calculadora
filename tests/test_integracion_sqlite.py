import pytest
import sqlite3
import os
from pathlib import Path
from unittest.mock import patch
from src.database import create_operations_table, get_operations_history
from src.operations import calculate
from src.ui import create_display, create_main_window
import tkinter as tk

@pytest.fixture
def setup_db():
    """Configuración de la base de datos para pruebas"""
    # Crear la tabla
    create_operations_table()
    yield
    # Limpieza: eliminar la base de datos de prueba
    db_path = Path(__file__).parent.parent / 'src' / 'calculadora.db'
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

def test_sqlite_integration(setup_db):
    """Prueba de integración con SQLite"""
    # Configuración
    ventana = create_main_window()
    pantalla = create_display(ventana)
    
    # Verificar que la base de datos está vacía al inicio
    assert len(get_operations_history()) == 0
    
    # Operaciones de prueba
    test_cases = [
        ("2+3", "5"),
        ("10-4", "6"),
        ("3*4", "12"),
        ("8/2", "4")
    ]
    
    # Ejecutar operaciones
    for operation, expected in test_cases:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, operation)
        calculate(pantalla)
        assert pantalla.get() == expected
    
    # Verificar historial
    history = get_operations_history()
    assert len(history) == len(test_cases)
    
    # Verificar contenido
    saved_ops = {op: res for op, res in history}
    for operation, expected in test_cases:
        assert operation in saved_ops
        assert saved_ops[operation] == expected
    
    # Verificar que el archivo de la base de datos existe
    db_path = Path(__file__).parent.parent / 'src' / 'calculadora.db'
    assert db_path.exists()