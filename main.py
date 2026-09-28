# -*- coding: utf-8 -*-
"""
Punto de Entrada Principal - Taller de Perceptron Simple Bipolar
Inteligencia Artificial - Corte 2
Universidad de Cartagena
Autores: Dago David Palmera Navarro, Julian David Camargo Padilla
"""

import sys
import os

# Incorporar la carpeta de modulos 'src' a la ruta de busqueda del interprete
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from app_gui import main

if __name__ == "__main__":
    # Iniciar la interfaz grafica interactiva
    main()
