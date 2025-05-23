import pyautogui
import time
import subprocess
import os
from pathlib import Path

BUTTON_COORDS = {
    '=': (858, 588), 
    'C': (937, 630)
}

def start_calculator():
    """Inicia la aplicación de la calculadora como un proceso separado."""
    current_script_dir = Path(__file__).parent

    project_root = current_script_dir.parent.parent
    calculator_path = project_root / "src" / "main.py"

    # Verificar si el archivo realmente existe antes de intentar abrirlo
    if not calculator_path.exists():
        print(f"ERROR: No se encontró main.py en la ruta esperada: {calculator_path}")
        # Puedes lanzar una excepción o salir si el archivo no es encontrado
        raise FileNotFoundError(f"Calculadora no encontrada en: {calculator_path}")

    print(f"Iniciando calculadora desde: {calculator_path}")
    return subprocess.Popen(['python3', str(calculator_path)]) # Usa 'python3' aquí también

def close_messagebox():
    """Intenta cerrar una ventana de MessageBox (asumiendo que tiene un botón 'OK' o se cierra con Enter)."""
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5) 

def run_fuzzing_test():
    print("Iniciando prueba de fuzzing...")
    time.sleep(2)

    pyautogui.click(775,390)

    fuzzing_inputs = [
        "+++++++++++++++++++++++++++++",  # Operadores repetidos
        "123.45.67",                       # Múltiples puntos decimales
        "1/0",                             # División por cero
        "sqrt(-5)",                        # Raíz cuadrada de número negativo (simulando, aunque la UI no permite esto directamente)
        "1e+999999",                       # Número extremadamente grande
        "()()()()",                        # Paréntesis vacíos
        "1 + ",                            # Expresión incompleta
        "!@#$%^&*()_+",                    # Caracteres especiales
        "print('hello')",                  # Intento de inyección (eval)
        "import os; os.system('calc')",    # Otro intento de inyección
        "9" * 500 + "/",                   # Cadena muy larga
        "∫" # Solo el símbolo de integral
    ]

    for i, input_str in enumerate(fuzzing_inputs):
        print(f"\n--- Prueba {i+1}: Entrada: '{input_str}' ---")
        pyautogui.click(BUTTON_COORDS['C'][0], BUTTON_COORDS['C'][1]) 
        time.sleep(0.2)

        pyautogui.typewrite(input_str, interval=0.01) 
        time.sleep(0.5) 

        pyautogui.click(BUTTON_COORDS['='][0], BUTTON_COORDS['='][1]) 
        time.sleep(1) 

        close_messagebox()

        print(f"Finalizada prueba para: '{input_str}'")

    print("\nPrueba de fuzzing finalizada.")


if __name__ == "__main__":
    calculator_process = start_calculator()
    try:
        time.sleep(3)
        run_fuzzing_test()
    except Exception as e:
        print(f"Error durante la prueba de fuzzing: {e}")
    finally:
        try:
            window = pyautogui.getWindowsWithTitle("Calculadora Simple")
            if window:
                window[0].close()
        except Exception as e:
            print(f"Error al intentar cerrar la ventana: {e}")
        if calculator_process:
            calculator_process.terminate()