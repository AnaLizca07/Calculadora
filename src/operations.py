import tkinter as tk
from tkinter import messagebox
import math
from sympy import symbols, integrate, sympify, SympifyError
from utils import is_empty
from database import save_operation

def setup_button_commands(ventana, pantalla):
    """Assigns commands to all calculator buttons."""
    # Get all buttons from the window
    buttons = []
    for widget in ventana.winfo_children():
        if isinstance(widget, tk.Button):
            buttons.append(widget)

    # Assign commands based on button text
    for button in buttons:
        text = button.cget("text")
        if text == '=':
            button.config(command=lambda: calculate(pantalla))
        elif text == '√':
            button.config(command=lambda: square_root(pantalla))
        elif text == 'x^y':
            button.config(command=lambda: power(pantalla, ventana))
        elif text == '∫':
            button.config(command=lambda: integral(pantalla, ventana))
        elif text == 'C':
            button.config(command=lambda: clear(pantalla))
        else:
            button.config(command=lambda b=text: press_button(b, pantalla))

def press_button(text, pantalla):
    """Handles normal button presses (numbers and operators)."""
    if pantalla.get() == "0" and text != '.':
        pantalla.delete(0, tk.END)
    pantalla.insert(tk.END, text)

def calculate(pantalla):
    """Calculates the expression displayed on the screen."""
    try:
        expresion = pantalla.get()

        if is_empty(expresion):
            messagebox.showerror("ERROR", "La expresión está vacía")
            pantalla.delete(0, tk.END)
            pantalla.insert(0, "0")
            return

        if expresion and expresion[-1] in ['+', '-', '*', '/']:
            messagebox.showerror("ERROR", "La expresión no puede terminar con un operador")
            return

        resultado = eval(expresion)

        if resultado == int(resultado):
            resultado = int(resultado)

        pantalla.delete(0, tk.END)
        pantalla.insert(0, str(resultado))
        
        # Guarda la operación en la base de datos
        save_operation(expresion, str(resultado))  # Añade esta línea

    except ZeroDivisionError:
        messagebox.showerror("ERROR", "No es posible dividir entre cero")
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "0")
    except Exception as e:
        messagebox.showerror("ERROR", f"Expresión inválida: {str(e)}")
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "0")

def clear(pantalla):
    """Clears the display and resets it to '0'."""
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "0")

def square_root(pantalla):
    """Calculates the square root of the number on the display."""
    try:
        entrada = pantalla.get().strip()

        if is_empty(entrada):
            messagebox.showerror("ERROR", "Debes ingresar un número")
            return

        valor = float(entrada)

        if valor < 0:
            messagebox.showerror("ERROR", "No se puede calcular la raíz cuadrada de un número negativo")
            return

        resultado = math.sqrt(valor)

        if resultado == int(resultado):
            resultado = int(resultado)

        pantalla.delete(0, tk.END)
        pantalla.insert(0, str(resultado))

        save_operation(entrada, str(resultado))

    except ValueError:
        messagebox.showerror("ERROR", "No es un número válido")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error inesperado: {str(e)}")

def power(pantalla, ventana_principal):
    """Handles the power operation, opening a new window for the exponent."""
    try:
        entrada = pantalla.get().strip()

        if is_empty(entrada):
            messagebox.showerror("ERROR", "Debes ingresar un número base")
            return

        base = float(entrada)

        ventana_exponente = tk.Toplevel(ventana_principal)
        ventana_exponente.title("Exponente")
        ventana_exponente.geometry("200x100")
        ventana_exponente.resizable(False, False)
        ventana_exponente.grab_set()

        tk.Label(ventana_exponente, text="Ingresa el exponente:").pack(pady=5)

        entrada_exponente = tk.Entry(ventana_exponente)
        entrada_exponente.pack(pady=5)
        entrada_exponente.focus_set()

        def calculate_power():
            try:
                exp_texto = entrada_exponente.get().strip()

                if is_empty(exp_texto):
                    messagebox.showerror("ERROR", "Debes ingresar un exponente")
                    return

                exponente = float(exp_texto)

                if base == 0 and exponente <= 0:
                    messagebox.showerror("ERROR", "No se puede elevar 0 a una potencia negativa o cero")
                    return

                resultado = base ** exponente

                if resultado == int(resultado):
                    resultado = int(resultado)

                pantalla.delete(0, tk.END)
                pantalla.insert(0, str(resultado))
                ventana_exponente.destroy()

                save_operation(entrada, str(resultado))

            except ValueError:
                messagebox.showerror("ERROR", "El exponente debe ser un número válido")
            except OverflowError:
                messagebox.showerror("ERROR", "El resultado es demasiado grande para calcularlo")
            except Exception as e:
                messagebox.showerror("ERROR", f"Error inesperado: {str(e)}")

        tk.Button(ventana_exponente, text="Calcular", command=calculate_power).pack(pady=5)
        ventana_exponente.bind('<Return>', lambda event: calculate_power())


    except ValueError:
        messagebox.showerror("ERROR", "El número base debe ser un valor numérico")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error inesperado: {str(e)}")

def integral(pantalla, ventana_principal):
    """Calculates the definite integral, opening a new window for input."""
    ventana_integral = tk.Toplevel(ventana_principal)
    ventana_integral.title("Integral Definida")
    ventana_integral.geometry("300x200")
    ventana_integral.resizable(False, False)
    ventana_integral.grab_set()

    tk.Label(ventana_integral, text="Función (usa 'x' como variable):").grid(row=0, column=0, padx=5, pady=5)
    entrada_funcion = tk.Entry(ventana_integral, width=20)
    entrada_funcion.grid(row=0, column=1, padx=5, pady=5)
    entrada_funcion.focus_set()

    tk.Label(ventana_integral, text="Límite inferior:").grid(row=1, column=0, padx=5, pady=5)
    entrada_lim_inf = tk.Entry(ventana_integral, width=10)
    entrada_lim_inf.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_integral, text="Límite superior:").grid(row=2, column=0, padx=5, pady=5)
    entrada_lim_sup = tk.Entry(ventana_integral, width=10)
    entrada_lim_sup.grid(row=2, column=1, padx=5, pady=5)

    def calculate_integral():
        try:
            funcion_str = entrada_funcion.get().strip()
            if is_empty(funcion_str):
                messagebox.showerror("ERROR", "Debes ingresar una función")
                return

            lim_inf_str = entrada_lim_inf.get().strip()
            if is_empty(lim_inf_str):
                messagebox.showerror("ERROR", "Debes ingresar el límite inferior")
                return

            lim_sup_str = entrada_lim_sup.get().strip()
            if is_empty(lim_sup_str):
                messagebox.showerror("ERROR", "Debes ingresar el límite superior")
                return

            funcion_str = funcion_str.replace('^', '**')

            if 'x' not in funcion_str:
                messagebox.showerror("ERROR", "La función debe contener la variable 'x'")
                return

            try:
                lim_inf = float(lim_inf_str)
            except ValueError:
                messagebox.showerror("ERROR", "El límite inferior debe ser un número")
                return

            try:
                lim_sup = float(lim_sup_str)
            except ValueError:
                messagebox.showerror("ERROR", "El límite superior debe ser un número")
                return

            try:
                x = symbols('x')
                expr = sympify(funcion_str)
            except SympifyError:
                messagebox.showerror("ERROR", "La función ingresada no es válida")
                return
            except Exception:
                messagebox.showerror("ERROR", "Error al procesar la función")
                return

            try:
                resultado = float(integrate(expr, (x, lim_inf, lim_sup)))

                if resultado == int(resultado):
                    resultado = int(resultado)

                pantalla.delete(0, tk.END)
                pantalla.insert(0, str(resultado))
                ventana_integral.destroy()

                save_operation(funcion_str, str(resultado))

            except ValueError:
                messagebox.showerror("ERROR", "No se pudo calcular la integral con los valores proporcionados")
            except Exception as e:
                messagebox.showerror("ERROR", f"Error al calcular la integral: {str(e)}")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error inesperado: {str(e)}")

    tk.Button(ventana_integral, text="Calcular", command=calculate_integral).grid(row=3, column=0, columnspan=2, pady=10)
    ventana_integral.bind('<Return>', lambda event: calculate_integral())