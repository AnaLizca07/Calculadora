import sqlite3
from pathlib import Path
import os

DB_PATH = Path(__file__).parent / 'calculadora.db'

def get_connection():
    """Obtiene una conexión a la base de datos con verificación de tabla"""
    conn = sqlite3.connect(str(DB_PATH))
    
    # Verificar si la tabla existe
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='operaciones'")
    if not cursor.fetchone():
        create_operations_table(conn)
    
    return conn

def create_operations_table(conn=None):
    """Crea la tabla de operaciones"""
    close_conn = False
    try:
        if conn is None:
            conn = sqlite3.connect(str(DB_PATH))
            close_conn = True
            
        conn.execute("""
            CREATE TABLE IF NOT EXISTS operaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operacion TEXT NOT NULL,
                resultado TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
    except Exception as e:
        print(f"Error crítico al crear tabla: {e}")
        raise
    finally:
        if close_conn and conn:
            conn.close()

def save_operation(operation, result):
    """Guarda una operación en la base de datos"""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO operaciones (operacion, resultado) VALUES (?, ?)",
                (operation, result)
            )
            conn.commit()
    except Exception as e:
        print(f"Error al guardar operación: {e}")
        raise

def get_operations_history(limit=10):
    """Obtiene el historial de operaciones"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT operacion, resultado FROM operaciones ORDER BY fecha DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        raise