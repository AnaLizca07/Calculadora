Calculadora simple con funciones avanzadas e historial

Contexto del proyecto:
Este proyecto es una calculadora simple desarrollada en Python usando la biblioteca
tkintes para la interfaz gráfica. Su objetivo principal es dar una herramienta básica
de cálculo con funciones aritméticas importantes, que a su vez incorpora funcionalidades
avanzadas como el cálculo de raices cuadradas, potencias, e integrales definidas.

Una característica distintiva de esta calculadora es la persistencia de datos: 
cada operación simple (suma, resta, multiplicación, división) realizada se guarda en 
una base de datos SQLite, permitiendo así mantener un historial de cálculos. 

El proyecto está estructurado de manera modular, separando las responsabilidades de la interfaz 
de usuario, las operaciones lógicas y la interacción con la base de datos, lo que facilita 
su mantenimiento y escalabilidad. Adicionalmente, cuenta con un conjunto robusto de pruebas 
(unitarias, de integración y de sistema) para asegurar su correcto funcionamiento y estabilidad.


Características
Operaciones Básicas: Suma, resta, multiplicación y división.
Funciones Avanzadas:
Raíz cuadrada, Potencia, Integral definida 
​
Historial de Operaciones: Guarda cada cálculo básico (suma, resta, multiplicación, división) de forma 
operación y resultado en una base de datos SQLite.

Interfaz gráfica intuitiva: Desarrollada con tkinter para una experiencia de usuario sencilla.

Manejo de Errores: Incluye validaciones para entradas inválidas Ejemplo: división por cero, expresiones incompletas.

Modularidad: Código organizado en módulos (database, operations, ui, utils) para una mejor gestión.

Estructura del proyecto:

src/main.py: Punto de entrada principal de la aplicación. Inicializa la interfaz de usuario y la base de datos.

src/database.py: Contiene las funciones para interactuar con la base de datos SQLite (conexión, creación de tabla, guardar y recuperar operaciones).

src/operations.py: Define la lógica para todas las operaciones de la calculadora (cálculo, raíz cuadrada, potencia, integral) y asigna comandos a los botones de la UI.

src/ui.py: Se encarga de la creación y configuración de la interfaz gráfica de usuario con tkinter (ventana principal, pantalla, botones).

src/utils.py: Contiene funciones utilitarias, como la verificación de cadenas vacías.

tests/: Directorio que alberga todas las pruebas del proyecto.

test_unit.py: Pruebas unitarias para funciones específicas.

test_integration.py: Pruebas de integración, verificando la interacción entre componentes (lógica y base de datos).

test_system.py: Pruebas de sistema completas, simulando la interacción del usuario con la UI y verificando la persistencia de datos.

test_fuzzing.py: Prueba de fuzzing para evaluar la robustez de la aplicación ante entradas inesperadas.

test_performance.py: Prueba de rendimiento para medir la capacidad de respuesta de la aplicación bajo carga.

Requisitos:

Para ejecutar esta aplicación y sus pruebas, necesitarás Python 3 y las siguientes bibliotecas:

tkinter (generalmente viene incluido con Python)
sqlite3 (viene incluido con Python)
sympy
pytest (para ejecutar las pruebas)
pyautogui (para las pruebas de fuzzing y rendimiento)

Para instalar librerias externas, se puede usar pip:
pip install sympy pytest pyautogui

Ejecución de la aplicación:

Para iniciar la calculadora, hay que navegar al directorio src y ejecutar el archivo main.py
cd src
python3 main.py

Ejecución de las pruebas
Para ejecutar las pruebas, debemos de estar en la raíz del proyecto y tener instalado pytest.

Pruebas unitarias
pytest tests/test_unit.py

Pruebas de integración:
Las pruebas de integración validan la interacción entre diferentes módulos, 
como la lógica de operaciones y la base de datos.

pytest tests/test_integration.py

Prueba de sistema
Las pruebas de sistema simulan la interacción del usuario final con la aplicación completa, 
incluyendo la GUI y la persistencia de datos

pytest tests/test_system.py

Pruebas de fuzzing
Las pruebas de fuzzing envían entradas aleatorias o inesperadas a la aplicación para encontrar
 fallos o vulnerabilidades.

Para ejecutar la prueba de fuzzing, debes asegurarte de que la ventana de la calculadora esté 
visible y activa en tu pantalla, ya que pyautogui interactúa directamente con la interfaz gráfica

python3 tests/test_fuzzing.py

Pruebas de rendimiento
Las pruebas de rendimiento miden la capacidad de respuesta y la eficiencia de la aplicación bajo una carga de trabajo simulada.

Al igual que con las pruebas de fuzzing, la ventana de la calculadora debe estar visible y activa 
para que pyautogui pueda simular los clics de los botones.

python3 tests/test_performance.py

