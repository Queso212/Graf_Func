import flet as ft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import base64 
import sympy as sp
import math
import re

def main(page: ft.Page):
    page.title = "Calculadora de ecuaciones cuadraticas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 600
    
    ## Rango de X
    x_min = -10
    x_max = 10
    
    def grafica(function_str, x_min, x_max):
        try:
            function_str = function_str.replace("^", "**")
            
            #Funciones elementales
            function_str = function_str.replace("sin", "np.sin")
            function_str = function_str.repalce("cos", "np.cos")
            function_str = function_str.repalce("tan", "np.tan")
            function_str = function_str.repalce("log", "np.log10")
            function_str = function_str.repalce("ln", "np.log")
            function_str = function_str.repalce("exp", "np.exp")
            function_str = function_str.repalce("sqrt", "np.sqrt")
            function_str = function_str.repalce("pi", "np.pi")
            
            #Definir Constante, dado la ausencia de x
            if 'x' not in function_str:
                function_str = f"{function_str} + 0*x"
                
            #Funcion que sale apartir del dato del usuario
            def f(x):
                return eval(function_str)
            
            
            x = np.linspace(x_min, x_max, 1000)
            y = f(x)
            
            #Grafica la figura
            fig, ax = plt.subplots(figsize =(8,5))
            ax.plot(x, y, 'b-', linewidth = 2)
            ax.grid(True, linestyle='--', alpha = 0.7)
            ax.axhline(y=0, color = 'k', linestyle='-', alpha=0.3)
            ax.axhline(x=0, color = 'k', linestyle='-', alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'Grafica de funcion: {function_input.value}')
            
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            
            graph_image.src_base64 = img_base64
            result_text.value = f"Funcion graficada: f(x) = {function_input.value}"
            result_text.color = "green"
            page.update()
            
        except Exception as e:
            result_text.value = f"Error: {str(e)}"
            result_text.color = "red"
            graph_image.src_base64 = None
            page.update()
            
    def Actualiza_rango(e):
        nonlocal x_min, x_max
        try:
            x_min = float(x_min_input.value)
            x_max = float(x_max_input.value)
            
            if x_min >= x_max:
                result_text.value = "Valor minimo de la funcion supera al maximo"
                result_text.color = "red"
                page.update()
                return
            if function_input.value:
                grafica(function_input.value, x_min, x_max)
                
        except ValueError:
            result_text.value = "Ingrese valores numéricos válidos para el rango."
            result_text.color = "red"
            page.update()
            
    def trazado(e):
        if not function_input.value:
            result_text.value = "Ingrese una funcion"
            result_text.color = "red"
            page.update()
            return
        
        grafica(function_input.value, x_min, x_max)
        
    examples = [
        "x^2",
        "sin(x)",
        "cos(x)",
        "tan(x)",
        "x^3 - 3*x",
        "exp(x)",
        "log(x)",
        "sqrt(x)",
        "1/x"
    ]
        
    def use_example(e):
        function_input.value = dropdown_examples.value
        trazado(None)
        page.update()
    
    #Interfaz Grafica
    title_text = ft.Text("Graficador de funciones", size = 28, weight = ft.FontWeight.BOLD)
    instrucciones = ft.Text(
        "Ingrese una funcion en terminos de x: ",
        size = 14, color = "white"
    )
    
    function_input = ft.TextField(
        label = "Funcion f(x)",
        hint_text = "Ejemplo: x^2 + 2*x -1",
        width = 400,
        on_submit = trazado
    )
    dropdown_examples = ft.Dropdown(
        label="Ejemplos",
        width=200,
        options=[ft.dropdown.Option(example) for example in examples],
    )
    
    boton_graficar = ft.ElevatedButton(
        text = "Graficar",
        on_click = grafica,
        icon = ft.icons.SHOW_CHART
    )
    
    x_min_input = ft.TextField(
        label = "Valor minimo de x",
        value = str(x_min),
        width = 150,
        on_submit = Actualiza_rango
    )
       
    
    x_max_input = ft.TextField(
        label = "Valor maximo de x",
        value = str(x_max),
        width = 150,
        on_submit = Actualiza_rango
    )
    
    boton_rango = ft.ElevatedButton(
        text = "Actualizar rango",
        on_click = Actualiza_rango
    )
    
    result_text = ft.Text("", size = 16)
    
    graph_image = ft.Image(
        width = 700,
        height = 400,
        fit = ft.ImageFit.CONTAIN
    )
    
    page.add(
        ft.Column(
            [
                title_text,
                instrucciones,
                ft.Row(
                    [function_input],
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [boton_graficar],
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
                ft.Text("Cambiar el rango: ", size = 16),
                ft.Row(
                   [x_min_input, x_max_input, boton_rango],
                   alignment = ft.MainAxisAlignment.CENTER 
                ),
                result_text,
                graph_image
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )
ft.app(target = main)