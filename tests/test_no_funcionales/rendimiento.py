import pyautogui
import time
import subprocess
import os
from pathlib import Path

BUTTON_COORDS = {
    '7': (710, 450), 
    '8': (775, 450),
    '9': (857, 450),
    '/': (929, 450),
    '4': (694, 500),
    '5': (774, 500),
    '6': (858, 500),
    '*': (940, 500),
    '1': (696, 540),
    '2': (755, 540),
    '3': (855, 540),
    '-': (939, 540),
    '0': (695, 588),
    '.': (774, 588),
    '=': (858, 588),
    '+': (938, 588),
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

def run_performance_test():
    print("Iniciando prueba de rendimiento...")
    time.sleep(2) # Dar tiempo para que la ventana de la calculadora se cargue y se active

    # Patrón de entrada rápido para la prueba de rendimiento
    rapid_sequence = "1+2-3*4/5=C" * 5 # Repetir la secuencia 5 veces

    start_time = time.time()

    for char in rapid_sequence:
        if char in BUTTON_COORDS:
            x, y = BUTTON_COORDS[char]
            pyautogui.click(x, y)
        elif char == '=':
            # Presionar el botón '='
            pyautogui.click(BUTTON_COORDS['='][0], BUTTON_COORDS['='][1])
            # Si el cálculo es muy rápido, puede que el display no actualice
            # Puedes añadir una pequeña pausa si observas que se saltan resultados
            time.sleep(0.05)
        elif char == 'C':
            # Presionar el botón 'C'
            pyautogui.click(BUTTON_COORDS['C'][0], BUTTON_COORDS['C'][1])
            time.sleep(0.05)
        else: # Si es un número o punto que no tenemos en BUTTON_COORDS para clics individuales, usar typewrite
              # Aunque para esta prueba, es mejor clics individuales para simular un usuario
            pass
        # Una pausa muy pequeña para simular la velocidad humana y permitir la actualización de la UI
        time.sleep(0.01) # Ajusta este valor si necesitas más o menos velocidad

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Secuencia de {len(rapid_sequence)} pulsaciones completada en {elapsed_time:.2f} segundos.")

    print("Prueba de rendimiento finalizada.")

# --- Ejecución principal del script de prueba ---
if __name__ == "__main__":

    calculator_process = start_calculator()

    try:
        # Dar tiempo a la calculadora para que se inicie completamente
        time.sleep(3)
        run_performance_test()
    except Exception as e:
        print(f"Error durante la prueba: {e}")
    finally:
        # Cierra la ventana de la calculadora al finalizar la prueba
        # Esto es un poco tricky con PyAutoGUI. Puedes intentar cerrar la ventana por título:
        try:
            window = pyautogui.getWindowsWithTitle("Calculadora Simple")
            if window:
                window[0].close() # Cierra la primera ventana encontrada con ese título
                print("Ventana de la calculadora cerrada.")
            else:
                print("No se encontró la ventana de la calculadora para cerrar.")
        except Exception as e:
            print(f"Error al intentar cerrar la ventana: {e}")
        # Si usaste subprocess.Popen, también puedes terminar el proceso:
        if calculator_process:
            calculator_process.terminate()
            print("Proceso de la calculadora terminado.")