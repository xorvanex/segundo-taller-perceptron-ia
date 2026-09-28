# SEGUNDO TALLER: REDES NEURONALES - PERCEPTRÓN SIMPLE (PS)
### *Modelado, Simulación y Entrenamiento en Dominio Bipolar con Función Hardlims*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Universidad-De%20Cartagena-red?style=for-the-badge" alt="Unicartagena"/>
  <img src="https://img.shields.io/badge/Materia-Inteligencia%20Artificial-blue?style=for-the-badge" alt="Materia"/>
  <img src="https://img.shields.io/badge/Convergencia-100%25%20(E%3D0)-brightgreen?style=for-the-badge" alt="Convergencia"/>
</p>

---

## 🏛️ Información Institucional y Académica
* **Institución:** Universidad de Cartagena
* **Facultad:** Facultad de Ingeniería
* **Programa:** Ingeniería de Sistemas — Semestre VII
* **Asignatura:** Inteligencia Artificial (Segundo Corte)
* **Docente:** Manuel Alejandro Ospina Alarcón
* **Autores:**
  * **Dago David Palmera Navarro** — Cód. `0222321003`
  * **Julián David Camargo Padilla** — Cód. `0222320016`
* **Fecha:** Septiembre de 2026

---

## 📖 Tabla de Contenido
1. [Descripción General](#-descripción-general)
2. [Fundamento Matemático del Modelo](#-fundamento-matemático-del-modelo)
3. [Casos de Estudio Abordados](#-casos-de-estudio-abordados)
4. [Estructura Modular del Proyecto](#-estructura-modular-del-proyecto)
5. [Requisitos y Configuración del Entorno](#-requisitos-y-configuración-del-entorno)
6. [Guía de Ejecución de los Programas](#-guía-de-ejecución-de-los-programas)
7. [Resultados y Comparativa de Convergencia](#-resultados-y-comparativa-de-convergencia)
8. [Matriz de Entregables](#-matriz-de-entregables)
9. [Licencia](#-licencia)

---

## 📌 Descripción General

Este repositorio contiene el desarrollo analítico, matemático, algorítmico y computacional del **Segundo Taller Evaluativo de Inteligencia Artificial**, enfocado en la implementación y entrenamiento supervisado de una Red Neuronal Artificial tipo **Perceptrón Simple (PS)**.

El sistema opera bajo una convención estrictamente **bipolar $\{-1, +1\}$**, empleando la función de activación escalón simétrica `hardlims` y optimización sináptica mediante la **Regla Delta**. Se resuelven dos problemas reales de clasificación en tres dimensiones ($\mathbb{R}^3$):
1. **Condicionamiento Instrumental de la Paloma:** Simulación de aprendizaje por refuerzo y toma de decisiones animal en una caja de Skinner con pulsadores luminosos.
2. **Diagnóstico Médico por Síntomas:** Sistema clínico de apoyo a la decisión que diagnostica patologías según la concurrencia de síntomas (Fiebre, Cefalea y Fatiga), evaluando adicionalmente la sensibilidad del algoritmo frente a distintas condiciones iniciales (convergencia en 3, 2 y 1 épocas).

---

## 📐 Fundamento Matemático del Modelo

El Perceptrón Simple actúa como un clasificador lineal discriminativo que aprende a separar el hipercubo bipolar $\{-1, +1\}^3$ mediante un hiperplano bidimensional:

1. **Combinación Lineal (Salida Neta $a$):**
   $$a = \mathbf{W}^T \mathbf{X} + b = \sum_{j=1}^{3} W_j x_j + b = W_1 x_1 + W_2 x_2 + W_3 x_3 + b$$
2. **Función de Activación Bipolar (`hardlims`):**
   $$y = \text{hardlims}(a) = \begin{cases} +1 & \text{si } a \ge 0 \\ -1 & \text{si } a < 0 \end{cases}$$
3. **Cálculo del Error Discreto:**
   $$e = y_d - y \in \{-2,\ 0,\ +2\}$$
4. **Regla de Aprendizaje Delta Supervisada:**
   $$\mathbf{W}^{(nuevo)} = \mathbf{W}^{(actual)} + e \cdot \mathbf{X}$$
   $$b^{(nuevo)} = b^{(actual)} + e$$
5. **Criterio de Parada:** Cero errores globales en una época completa ($E_{global} = \sum |e_k| = 0$).

> **Ventaja del Dominio Bipolar:** Al no existir entradas en cero ($x_j \ne 0$), ningún peso queda congelado durante las actualizaciones por error ($\Delta W_j \ne 0$), dinamizando activamente la reorientación del vector normal en cada iteración.

---

## 🔬 Casos de Estudio Abordados

| Característica | Caso 1: Condicionamiento de la Paloma | Caso 2: Diagnóstico Médico por Síntomas |
| :--- | :--- | :--- |
| **Entradas ($x_1, x_2, x_3$)** | $x_1$: Pulsador Izq, $x_2$: Pulsador Der, $x_3$: Acción Paloma | $x_1$: Fiebre, $x_2$: Cefalea, $x_3$: Fatiga |
| **Codificación Bipolar** | $+1$: Encendido / Pica Izq \| $-1$: Apagado / Pica Der | $+1$: Presenta síntoma \| $-1$: No presenta síntoma |
| **Criterio de Decisión** | Luces encendidas $\to$ Éxito (+1); Ambas apagadas $\to$ Picar Der (+1) | Concurrencia de $\ge 2$ síntomas $\to$ Enfermo (+1); $< 2$ $\to$ Sano (-1) |
| **Distribución de Clases** | Asimétrica (7 éxitos frente a 1 fracaso) | Simétrica balanceada (4 sanos frente a 4 enfermos) |
| **Condición Inicial Principal** | $\mathbf{W}^{(0)} = [0.3, -0.9, -0.4]^T,\ b^{(0)} = 0.2$ | $\mathbf{W}^{(0)} = [-0.4, -0.7, 0.3]^T,\ b^{(0)} = 0.1$ |
| **Épocas de Convergencia** | **3 Épocas** ($E: 10 \to 4 \to 0$) | **3 Épocas** ($E: 4 \to 4 \to 0$) |
| **Parámetros Finales** | $\mathbf{W}^* = [2.3, 5.1, -2.4]^T,\ b^* = 6.2$ | $\mathbf{W}^* = [3.6, 3.3, 4.3]^T,\ b^* = 0.1$ |
| **Ecuación del Hiperplano** | $2.3x_1 + 5.1x_2 - 2.4x_3 + 6.2 = 0$ | $3.6x_1 + 3.3x_2 + 4.3x_3 + 0.1 = 0$ |
| **Precisión Final** | **100% (8/8 patrones)** | **100% (8/8 patrones)** |

---

## Estructura Modular del Proyecto

```text
segundo-taller-perceptron-ia
 ┣ data
 ┃ ┣ datasets                                       # Matrices numericas en formato CSV
 ┃ ┃ ┣ patrones_caso1_paloma.csv
 ┃ ┃ ┗ patrones_caso2_diagnostico.csv
 ┃ ┗ enunciados                                     # Documentos de la catedra
 ┃   ┣ Caso de estudio 1 PS.pdf
 ┃   ┣ Caso de estudio 2 PS.pdf
 ┃   ┗ Informacion_actidad.txt
 ┃
 ┣ docs
 ┃ ┣ Taller_Percetron_Simple_IA_PALMERA_CAMARGO.docx # Documento formal de entrega en Word
 ┃ ┣ Memorias_Calculo_Perceptron_Corte2.xlsx       # Libro Excel con calculos paso a paso
 ┃ ┣ img                                            # Visualizaciones vectoriales generadas
 ┃ ┃ ┣ Curva_Aprendizaje_Caso1.png
 ┃ ┃ ┣ Grafica3D_Caso1_Paloma.png
 ┃ ┃ ┣ Curva_Aprendizaje_Caso2.png
 ┃ ┃ ┗ Grafica3D_Caso2_Diagnostico.png
 ┃ ┗ md                                             # Memorias analiticas en Markdown
 ┃   ┣ Introduccion_Objetivos_y_Fundamentacion.md   # Marco teorico, portada e introduccion
 ┃   ┣ Memoria Calculo Caso 1 - Condicionamiento Paloma.md
 ┃   ┣ Memoria Calculo Caso 2 - Diagnostico Medico.md
 ┃   ┗ Analisis_y_Conclusiones.md                   # Analisis global y conclusiones
 ┃
 ┣ src
 ┃ ┣ __init__.py                                    # Inicializador del paquete Python
 ┃ ┣ perceptron.py                                  # Clase central PerceptronSimpleBipolar
 ┃ ┣ app_gui.py                                     # Interfaz Grafica de Usuario (GUI Tkinter + Matplotlib)
 ┃ ┗ consola                                        # Modulo de ejecucion directa por terminal
 ┃   ┣ __init__.py
 ┃   ┣ caso_1_paloma.py                             # Script consola Caso 1 (La Paloma)
 ┃   ┣ caso_2_diagnostico.py                        # Script consola Caso 2 (Diagnostico)
 ┃   ┗ generar_excel_memorias.py                    # Generador del archivo .xlsx
 ┃
 ┣ main.py                                          # Lanzador principal de la aplicacion GUI
 ┣ .gitignore                                       # Exclusiones de Git (venv, pycache)
 ┣ requirements.txt                                 # Dependencias del proyecto
 ┣ LICENSE                                          # Licencia MIT
 ┗ README.md                                        # Instructivo y documentacion principal
```

---

## Requisitos y Configuracion del Entorno

### 1. Prerrequisitos
* **Python 3.8 o superior** instalado en el sistema.

### 2. Creacion y Activacion del Entorno Virtual (Opcional pero recomendado)
En PowerShell (Windows):
```powershell
python -m venv venv
.\venv\Scripts\activate
```
En Bash (macOS / Linux):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacion de Dependencias
```bash
pip install -r requirements.txt
```
*Librerias principales empleadas:*
* `numpy` (Algebra lineal, matrices y calculo vectorial)
* `matplotlib` (Trazado de curvas de error y superficies 3D interactivas)
* `openpyxl` (Generacion programatica de hojas de calculo Excel)

---

## Guia de Ejecucion de los Programas

### 1. Interfaz Grafica de Usuario (Recomendado)
Inicia la aplicacion de escritorio completa con simulacion en tiempo real, tablas de verificacion y visualizaciones 3D interactivas (rotables con el raton):
```bash
python main.py
```
*o alternativamente:*
```bash
python src/app_gui.py
```
* **Caracteristicas de la GUI:**
  * Pestaña Caso 1 (Paloma): Modificacion interactiva de pesos y sesgo inicial, verificacion de 8 patrones y renderizado de curva 2D e hiperplano 3D.
  * Pestaña Caso 2 (Diagnostico): Selector de presets (3, 2 y 1 epocas) o parametros personalizados con clasificador interactivo.
  * Pestaña Comparativa de Sensibilidad: Curvas superpuestas y grafico de barras de velocidad de convergencia.
  * Visualizacion interactiva con `FigureCanvasTkAgg` y `NavigationToolbar2Tk`: permite rotar la nube de puntos y el plano 3D con el cursor. Cierre limpio sin dejar archivos residuales ni fugas de memoria.

### 2. Scripts de Consola (Ejecucion Terminal)

#### Caso 1: Condicionamiento de la Paloma
Entrena el perceptron para el caso de Skinner, reporta cada epoca por consola y genera las figuras correspondientes:
```bash
python src/consola/caso_1_paloma.py
```

#### Caso 2: Diagnostico Medico por Sintomas
Ejecuta el experimento clinico principal (3 epocas) y la experimentacion comparativa de sensibilidad (2 y 1 epocas):
```bash
python src/consola/caso_2_diagnostico.py
```

#### Regenerar el Libro Excel de Memorias de Calculo (.xlsx)
Genera el archivo con las tablas numericas tabuladas de todas las iteraciones:
```bash
python src/consola/generar_excel_memorias.py
```

---

## 📊 Resultados y Comparativa de Convergencia

### Estudio Comparativo de Sensibilidad a las Condiciones Iniciales (Caso 2)
El repositorio incluye el análisis de cómo la selección del punto de partida modula la velocidad de convergencia:

| Experimento | Condición Inicial $\mathbf{W}^{(0)}$ | Sesgo $b^{(0)}$ | Trayectoria del Error ($E_{global}$) | Épocas | Parámetros Calibrados ($\mathbf{W}^*,\ b^*$) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Principal (Aleatorio)** | $[-0.4, -0.7, 0.3]^T$ | $0.1$ | $4 \longrightarrow 4 \longrightarrow 0$ | **3 Épocas** | $\mathbf{W}^* = [3.6, 3.3, 4.3]^T,\ b^* = 0.1$ |
| **2. Optimizado** | $[-0.9, -0.9, -0.9]^T$ | $0.9$ | $2 \longrightarrow 0$ | **2 Épocas** | $\mathbf{W}^* = [1.1, 1.1, 1.1]^T,\ b^* = -1.1$ |
| **3. Solución Directa** | $[1.0, 1.0, 1.0]^T$ | $0.0$ | $0$ | **1 Época** | $\mathbf{W}^* = [1.0, 1.0, 1.0]^T,\ b^* = 0.0$ |

---

## 📦 Matriz de Entregables

| Entregable | Formato | Ubicación | Descripción |
| :--- | :---: | :--- | :--- |
| **Informe Final Escrito** | `.docx` | `docs/Taller_Percetron_Simple_IA_PALMERA_CAMARGO.docx` | Documento formal consolidado con portada, introducción, teoría y casos |
| **Memorias en Hoja de Cálculo**| `.xlsx` | `docs/Memorias_Calculo_Perceptron_Corte2.xlsx` | Registro paso a paso de cada multiplicación, suma neta y corrección |
| **Memorias Técnicas** | `.md` | `docs/md/` | Archivos Markdown modulares para consulta y trazabilidad |
| **Código Fuente** | `.py` | `src/` | Algoritmos de entrenamiento y simulación modular |
| **Datasets** | `.csv` | `data/datasets/` | Matrices bipolares de los 8 patrones por caso |
| **Visualizaciones 2D y 3D** | `.png` | `docs/img/` | Curvas de aprendizaje e hiperplanos de decisión en 3D (300 DPI) |

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la Licencia MIT. Consulte el archivo [LICENSE](LICENSE) para más detalles.
