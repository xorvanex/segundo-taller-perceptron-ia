# SEGUNDO TALLER: REDES NEURONALES - PERCEPTRON SIMPLE (PS)
### Modelado, Simulacion y Entrenamiento en Dominio Bipolar con Funcion Hardlims

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Universidad-De%20Cartagena-red?style=for-the-badge" alt="Unicartagena"/>
  <img src="https://img.shields.io/badge/Materia-Inteligencia%20Artificial-blue?style=for-the-badge" alt="Materia"/>
  <img src="https://img.shields.io/badge/Convergencia-100%25%20(E%3D0)-brightgreen?style=for-the-badge" alt="Convergencia"/>
</p>

---

## DOCUMENTO OFICIAL DE ENTREGA (INFORME FINAL EN PDF)

> **Acceso directo al informe academico consolidado:**  
> El documento formal de entrega con la fundamentacion teorica completa, planteamientos, tablas de verdad, memorias de calculo paso a paso para todas las epocas, analisis comparativo de sensibilidad a condiciones iniciales y conclusiones se encuentra disponible en formato PDF en el siguiente enlace:  
>
> -> **[Descargar / Ver Documento Formal de Entrega (PDF)](docs/Taller_Percetron_Simple_IA_PALMERA_CAMARGO.pdf)**  
>
> *Archivo:* `docs/Taller_Percetron_Simple_IA_PALMERA_CAMARGO.pdf` (3.5 MB, documento final con portada institucional, tablas y graficas de 300 DPI).

---

## Informacion Institucional y Academica

* **Institucion:** Universidad de Cartagena
* **Facultad:** Facultad de Ingenieria
* **Programa:** Ingenieria de Sistemas — Semestre VII
* **Asignatura:** Inteligencia Artificial (Segundo Corte)
* **Docente:** Manuel Alejandro Ospina Alarcon
* **Autores:**
  * **Dago David Palmera Navarro** — Codigo Estudiantil `0222321003`
  * **Julian David Camargo Padilla** — Codigo Estudiantil `0222320016`
* **Ponderacion:** 7 puntos de la calificacion definitiva del corte
* **Fecha de Entrega:** Lunes 28 de septiembre de 2026

---

## Tabla de Contenido

1. [Documento Oficial de Entrega (PDF)](#documento-oficial-de-entrega-informe-final-en-pdf)
2. [Informacion Institucional y Academica](#informacion-institucional-y-academica)
3. [Descripcion General](#descripcion-general)
4. [Fundamento Matematico del Modelo](#fundamento-matematico-del-modelo)
5. [Casos de Estudio Abordados](#casos-de-estudio-abordados)
6. [Estructura y Guia del Directorio del Proyecto](#estructura-y-guia-del-directorio-del-proyecto)
7. [Requisitos y Configuracion del Entorno](#requisitos-y-configuracion-del-entorno)
8. [Guia de Ejecucion de los Programas](#guia-de-ejecucion-de-los-programas)
9. [Resultados y Comparativa de Convergencia](#resultados-y-comparativa-de-convergencia)
10. [Matriz de Entregables](#matriz-de-entregables)
11. [Licencia](#licencia)

---

## Descripcion General

Este proyecto contiene el desarrollo integral (analitico, matematico, algoritmico y computacional) del **Segundo Taller Evaluativo de Inteligencia Artificial**, enfocado en el diseno, implementacion y entrenamiento supervisado de una Red Neuronal Artificial tipo **Perceptron Simple (PS)**.

El sistema opera estrictamente bajo una convencion **bipolar {-1, +1}**, utilizando la funcion de activacion escalon simetrica `hardlims(a)` y optimizacion de pesos sinapticos mediante la **Regla Delta**. Se abordan dos problemas de clasificacion y separabilidad lineal en el espacio tridimensional (R^3):

1. **Condicionamiento Instrumental de la Paloma (Caso 1):** Modelado de toma de decisiones y aprendizaje operante animal en una caja experimental de Skinner equipada con pulsadores luminosos izquierdo y derecho.
2. **Sistema de Diagnostico Medico por Sintomas (Caso 2):** Clasificador clinico que discrimina la presencia o ausencia de patologia segun la concurrencia de sintomas (Fiebre, Cefalea y Fatiga), evaluando adicionalmente la sensibilidad del algoritmo ante tres configuraciones de condiciones iniciales (convergencia en 3, 2 y 1 epocas).

---

## Fundamento Matematico del Modelo

El Perceptron Simple actua como un clasificador lineal discriminativo que aprende a particionar el hipercubo bipolar {-1, +1}^3 mediante un plano de separacion bidimensional:

1. **Combinacion Lineal (Suma Ponderada Neta):**
   $$a = \mathbf{W}^T \mathbf{X} + b = \sum_{j=1}^{3} W_j x_j + b = W_1 x_1 + W_2 x_2 + W_3 x_3 + b$$

2. **Funcion de Activacion Bipolar (`hardlims`):**
   $$y = \text{hardlims}(a) = \begin{cases} +1 & \text{si } a \ge 0 \\ -1 & \text{si } a < 0 \end{cases}$$

3. **Calculo del Error Discreto de Clasificacion:**
   $$e = y_d - y \in \{-2,\ 0,\ +2\}$$

4. **Regla de Actualizacion Delta Supervisada:**
   $$\mathbf{W}^{(nuevo)} = \mathbf{W}^{(actual)} + e \cdot \mathbf{X}$$
   $$b^{(nuevo)} = b^{(actual)} + e$$

5. **Criterio de Parada y Convergencia:**
   Error global nulo en una epoca completa:
   $$E_{global} = \sum_{k=1}^{8} |e_k| = 0$$

> **Ventaja del Dominio Bipolar:** Al no existir entradas en cero ($x_j \ne 0$), ningun peso queda congelado durante las actualizaciones por error ($\Delta W_j \ne 0$). Toda iteracion con error reorienta el vector normal en el espacio tridimensional.

---

## Casos de Estudio Abordados

| Caracteristica | Caso 1: Condicionamiento Paloma | Caso 2: Diagnostico Medico (Principal) |
| :--- | :--- | :--- |
| **Variables de Entrada ($x_1, x_2, x_3$)** | $x_1$: Pulsador Izq, $x_2$: Pulsador Der, $x_3$: Accion Paloma | $x_1$: Fiebre, $x_2$: Cefalea, $x_3$: Fatiga |
| **Codificacion Bipolar** | $+1$: Encendido / Pica Izq \| $-1$: Apagado / Pica Der | $+1$: Presenta sintoma \| $-1$: Ausente |
| **Criterio de Decision** | Luces encendidas -> Exito (+1); Ambas apagadas -> Picar Der (+1) | Concurrencia de >= 2 sintomas -> Enfermo (+1); < 2 -> Sano (-1) |
| **Distribucion de Clases** | Asimetrica (7 exitos vs. 1 fracaso) | Simetrica balanceada (4 sanos vs. 4 enfermos) |
| **Condiciones Iniciales** | $\mathbf{W}^{(0)} = [0.3, -0.9, -0.4]^T,\ b^{(0)} = 0.2$ | $\mathbf{W}^{(0)} = [-0.4, -0.7, 0.3]^T,\ b^{(0)} = 0.1$ |
| **Epocas de Convergencia** | **3 Epocas** ($E: 10 \to 4 \to 0$) | **3 Epocas** ($E: 4 \to 4 \to 0$) |
| **Pesos Finales Calibrados** | $\mathbf{W}^* = [2.3, 5.1, -2.4]^T,\ b^* = 6.2$ | $\mathbf{W}^* = [3.6, 3.3, 4.3]^T,\ b^* = 0.1$ |
| **Ecuacion del Hiperplano** | $2.3x_1 + 5.1x_2 - 2.4x_3 + 6.2 = 0$ | $3.6x_1 + 3.3x_2 + 4.3x_3 + 0.1 = 0$ |
| **Efectividad Final** | **100% (8/8 patrones clasificados con exactitud)** | **100% (8/8 patrones clasificados con exactitud)** |

---

## Estructura y Guia del Directorio del Proyecto

Para garantizar orden y claridad en la evaluacion, el proyecto esta organizado modularmente en carpetas tematicas:

```text
segundo-taller-perceptron-ia/
│
├── data/                                   # Datos y enunciados del taller
│   ├── datasets/                           # Matrices de entrenamiento en CSV
│   │   ├── patrones_caso1_paloma.csv       # Tabla de verdad del Caso 1
│   │   └── patrones_caso2_diagnostico.csv  # Tabla de verdad del Caso 2
│   └── enunciados/                         # Guias academicas oficiales
│       ├── Caso de estudio 1 PS.pdf        # Enunciado oficial Caso 1
│       ├── Caso de estudio 2 PS.pdf        # Enunciado oficial Caso 2
│       └── Informacion_actidad.txt         # Pautas y rubrica institucional
│
├── docs/                                   # Documentacion formal de entrega
│   ├── Taller_Percetron_Simple_IA_PALMERA_CAMARGO.pdf  # INFORME FINAL OFICIAL EN PDF
│   ├── Memorias_Calculo_Perceptron_Corte2.xlsx         # Libro Excel con calculos aritmeticos paso a paso
│   ├── img/                                # Figuras generadas en alta resolucion (300 DPI)
│   │   ├── Curva_Aprendizaje_Caso1.png     # Curva de error Caso 1 (10 -> 4 -> 0)
│   │   ├── Grafica3D_Caso1_Paloma.png      # Hiperplano separador 3D Caso 1
│   │   ├── Curva_Aprendizaje_Caso2.png     # Curva de error Caso 2 (4 -> 4 -> 0)
│   │   └── Grafica3D_Caso2_Diagnostico.png # Hiperplano separador 3D Caso 2
│   └── md/                                 # Memorias tecnicas de calculo en formato Markdown
│       ├── Introduccion_Objetivos_y_Fundamentacion.md
│       ├── Memoria Calculo Caso 1 - Condicionamiento Paloma.md
│       ├── Memoria Calculo Caso 2 - Diagnostico Medico.md
│       └── Analisis_y_Conclusiones.md
│
├── src/                                    # Codigo fuente de la aplicacion
│   ├── __init__.py                         # Inicializador del paquete
│   ├── perceptron.py                       # Clase central PerceptronSimpleBipolar (algoritmo puro)
│   ├── app_gui.py                          # Interfaz Grafica de Usuario interactiva (Tkinter + Matplotlib 3D)
│   └── consola/                            # Scripts de consola para ejecucion directa por terminal
│       ├── __init__.py
│       ├── caso_1_paloma.py                # Script ejecutable de consola para el Caso 1
│       ├── caso_2_diagnostico.py           # Script ejecutable de consola para el Caso 2 y sensibilidad
│       └── generar_excel_memorias.py       # Script generador del libro Excel de memorias
│
├── main.py                                 # Punto de entrada principal (lanza la GUI)
├── requirements.txt                        # Lista de dependencias de Python
├── LICENSE                                 # Licencia MIT del proyecto
├── .gitignore                              # Archivos excluidos de control de versiones
└── README.md                               # Guia de usuario y documentacion del repositorio
```

---

## Requisitos y Configuracion del Entorno

### 1. Requisitos Previos
* **Python 3.8 o superior** instalado en el sistema.

### 2. Creacion y Activacion del Entorno Virtual (Recomendado)
En PowerShell (Windows):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

En Bash (Linux / macOS):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacion de Dependencias
Ejecute el siguiente comando para instalar las librerias requeridas:
```bash
pip install -r requirements.txt
```

*Librerias utilizadas:*
* `numpy`: Calculo matricial, algebra lineal y operaciones vectoriales.
* `matplotlib`: Renderizado de curvas de convergencia 2D e hiperplanos 3D interactivos.
* `openpyxl`: Generacion y formato programatico de la hoja de calculo Excel de memorias de calculo.

---

## Guia de Ejecucion de los Programas

### 1. Interfaz Grafica de Usuario Interactiva (Recomendado)

Inicie la aplicacion de escritorio completa con simulacion dinamica, tablas de evaluacion y visualizaciones tridimensionales rotables interactivamente con el raton:

```bash
python main.py
```
*(O alternativamente: `python src/app_gui.py`)*

**Caracteristicas principales de la GUI:**
* **Pestana Caso 1 (Paloma):** Permite configurar pesos y sesgo inicial, entrenar el perceptron en tiempo real, visualizar la trayectoria de las epocas, ver la tabla de 8 patrones y explorar la grafica 3D del hiperplano de decision de forma interactiva (rotacion, zoom y desplazamiento).
* **Pestana Caso 2 (Diagnostico):** Permite seleccionar entre los 3 presets de sensibilidad (3, 2 o 1 epocas) o ingresar valores manuales. Muestra la tabla de evaluacion clinica y el hiperplano que separa pacientes sanos de enfermos.
* **Pestana Comparativa de Sensibilidad:** Presenta graficos comparativos superpuestos de la evolucion del error y diagrama de barras con la velocidad de convergencia segun las condiciones iniciales.
* **Cierre limpio:** Al cerrar la ventana, la aplicacion libera todos los recursos de memoria sin dejar archivos temporales residuales.

### 2. Scripts de Consola (Ejecucion Terminal)

Si prefiere ejecutar los modelos directamente en la consola sin abrir la interfaz grafica:

#### Ejecutar Caso 1: Condicionamiento de la Paloma
Entrena el Perceptron para el problema de la paloma, imprime la traza de cada epoca en consola y genera las figuras en `docs/img/`:
```bash
python src/consola/caso_1_paloma.py
```

#### Ejecutar Caso 2: Diagnostico Medico por Sintomas
Ejecuta el experimento clinico principal (3 epocas) y la experimentacion comparativa de sensibilidad (2 y 1 epocas), imprimiendo la tabla consolidada:
```bash
python src/consola/caso_2_diagnostico.py
```

#### Regenerar el Libro Excel de Memorias de Calculo
Genera programaticamente el archivo `docs/Memorias_Calculo_Perceptron_Corte2.xlsx` con todas las sumatorias, activaciones y ajustes:
```bash
python src/consola/generar_excel_memorias.py
```

---

## Resultados y Comparativa de Convergencia

### Estudio Comparativo de Sensibilidad a las Condiciones Iniciales (Caso 2)

Para evaluar en profundidad la sensibilidad del algoritmo de aprendizaje supervisado frente a la orientacion inicial del hiperplano separador, se ejecutaron tres experimentos sobre el mismo conjunto de 8 perfiles clinicos:

| Experimento | Condicion Inicial $\mathbf{W}^{(0)}$ | Sesgo Inicial $b^{(0)}$ | Trayectoria del Error ($E_{global}$) | Epocas | Parametros Calibrados Finales ($\mathbf{W}^*,\ b^*$) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Principal (Aleatorio)** | $[-0.4, -0.7, 0.3]^T$ | $0.1$ | $4 \longrightarrow 4 \longrightarrow 0$ | **3 Epocas** | $\mathbf{W}^* = [3.6, 3.3, 4.3]^T,\ b^* = 0.1$ |
| **2. Optimizado** | $[-0.9, -0.9, -0.9]^T$ | $0.9$ | $2 \longrightarrow 0$ | **2 Epocas** | $\mathbf{W}^* = [1.1, 1.1, 1.1]^T,\ b^* = -1.1$ |
| **3. Solucion Directa** | $[1.0, 1.0, 1.0]^T$ | $0.0$ | $0$ | **1 Epoca** | $\mathbf{W}^* = [1.0, 1.0, 1.0]^T,\ b^* = 0.0$ |

**Conclusiones tecnicas destacadas:**
1. **Velocidad de Convergencia:** El numero de epocas no es un parametro rigido del dataset, sino que depende de la cercania de las condiciones iniciales a la region de separacion valida.
2. **Rol del Sesgo (*Bias*):** En el Caso 1, ante un desbalance de clases (7 exitos vs. 1 fracaso), el sesgo aumento a $b^* = 6.2$ para desplazar el hiperplano y elevar la excitacion basal. En el Caso 2, al ser clases perfectamente balanceadas (4 vs. 4), el sesgo convergio a $b^* = 0.1 \approx 0$, manteniendo el plano cerca del origen.
3. **Significado de los Pesos:** En el Caso 2, los tres pesos finales resultaron similares ($3.6, 3.3, 4.3$), corroborando analiticamente que los tres sintomas tienen la misma importancia relativa en el diagnostico clinico.

---

## Matriz de Entregables

| Entregable | Formato | Ubicacion | Descripcion |
| :--- | :---: | :--- | :--- |
| **Informe Final Escrito** | `PDF` | [docs/Taller_Percetron_Simple_IA_PALMERA_CAMARGO.pdf](docs/Taller_Percetron_Simple_IA_PALMERA_CAMARGO.pdf) | Documento formal consolidado con portada institucional, teoria, memorias y conclusiones |
| **Memorias en Hoja de Calculo** | `Excel (.xlsx)` | `docs/Memorias_Calculo_Perceptron_Corte2.xlsx` | Registro aritmetico tabular de cada multiplicacion, combinacion lineal y correccion |
| **Memorias Tecnicas en Markdown** | `Markdown (.md)` | `docs/md/` | Memorias modulares para consulta y trazabilidad rapida |
| **Codigo Fuente del Algoritmo** | `Python (.py)` | `src/perceptron.py` | Clase PerceptronSimpleBipolar con propagacion, hardlims y regla delta |
| **Interfaz Grafica Interactiva** | `Python / Tkinter` | `main.py` o `src/app_gui.py` | Aplicacion de escritorio interactiva con graficas 3D rotables |
| **Scripts de Consola** | `Python (.py)` | `src/consola/` | Scripts de ejecucion terminal automatizada para ambos casos |
| **Matrices de Datos** | `CSV (.csv)` | `data/datasets/` | Conjuntos de datos bipolares de entrenamiento (8 patrones por caso) |
| **Graficas en Alta Resolucion** | `PNG (300 DPI)` | `docs/img/` | Curvas de aprendizaje 2D y superficies de decision 3D |

---

## Licencia

Este proyecto se distribuye bajo los terminos de la Licencia MIT. Consulte el archivo [LICENSE](LICENSE) para mas detalles.
