# -*- coding: utf-8 -*-
"""
Interfaz Grafica de Usuario (GUI) - Perceptron Simple Bipolar
Taller de Inteligencia Artificial - Corte 2
Universidad de Cartagena
Autores: Dago David Palmera Navarro, Julian David Camargo Padilla
"""

import os
import sys
import io
import contextlib
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Matplotlib para integracion interactiva en Tkinter
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Importar modelo del Perceptron
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from perceptron import PerceptronSimpleBipolar

# Patrones de entrenamiento estandar
X_CASO1 = np.array([
    [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
    [ 1, -1, -1], [ 1, -1, 1], [ 1, 1, -1], [ 1, 1, 1]
], dtype=int)
YD_CASO1 = np.array([1, -1, 1, 1, 1, 1, 1, 1], dtype=int)

X_CASO2 = np.array([
    [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
    [ 1, -1, -1], [ 1, -1, 1], [ 1, 1, -1], [ 1, 1, 1]
], dtype=int)
YD_CASO2 = np.array([-1, -1, -1, 1, -1, 1, 1, 1], dtype=int)


class PerceptronGUI:
    """
    Aplicacion de escritorio con Interfaz Grafica de Usuario (GUI) para el
    analisis, simulacion y entrenamiento del Perceptron Simple Bipolar.

    Integra controles de configuracion de parametros iniciales, tablas de
    verificacion por patrones, registro paso a paso de calculos y visualizacion
    interactiva de curvas de error y superficies 3D de decision con Matplotlib.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal, estilos visuales y paneles del sistema.

        Args:
            root (tk.Tk): Instancia de la ventana raiz de Tkinter.
        """
        self.root = root
        self.root.title("Sistema de Perceptron Simple Bipolar - Inteligencia Artificial (Corte 2)")
        self.root.geometry("1340x840")
        self.root.minsize(1120, 720)

        # Cierre seguro de todas las figuras de Matplotlib al salir
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        """Aplica el esquema de colores institucional y tipografias profesionales."""
        style = ttk.Style()
        style.theme_use("clam")

        azul_primario = "#1f497d"
        gris_fondo = "#f4f6f9"

        self.root.configure(bg=gris_fondo)
        style.configure("TFrame", background=gris_fondo)
        style.configure("TLabelframe", background=gris_fondo, font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe.Label", background=gris_fondo, foreground=azul_primario)
        style.configure("TLabel", background=gris_fondo, font=("Segoe UI", 9))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=azul_primario, background=gris_fondo)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#333333", background=gris_fondo)
        style.configure("BannerTitle.TLabel", font=("Segoe UI", 10, "bold"), foreground=azul_primario, background="#e8eff7")
        style.configure("BannerText.TLabel", font=("Segoe UI", 8), foreground="#222222", background="#e8eff7")
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), padding=6, background=azul_primario, foreground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e1e6eb")

    def _construir_interfaz(self):
        """Construye el encabezado principal y las pestanas de analisis."""
        header_frame = ttk.Frame(self.root, padding="12 8 12 4")
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="UNIVERSIDAD DE CARTAGENA - FACULTAD DE INGENIERIA", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Taller de Perceptron Simple Bipolar (Corte 2) | Autores: Dago David Palmera Navarro, Julian David Camargo Padilla", style="SubHeader.TLabel").pack(anchor="w")

        # Pestañas principales
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text=" Caso 1: Condicionamiento Paloma ")
        self.notebook.add(self.tab2, text=" Caso 2: Diagnostico Clinico ")
        self.notebook.add(self.tab3, text=" Comparativa de Sensibilidad (Caso 2: Diagnostico) ")

        # Construccion de los paneles de cada caso
        self.componentes_caso1 = self._crear_panel_caso(
            parent=self.tab1,
            caso_id=1,
            titulo="Caso 1: Condicionamiento Instrumental de la Paloma",
            desc_entradas=["x1 (Pulsador Izq)", "x2 (Pulsador Der)", "x3 (Accion Pica)"],
            w_def=[0.3, -0.9, -0.4],
            b_def=0.2,
            X=X_CASO1,
            yd=YD_CASO1
        )

        self.componentes_caso2 = self._crear_panel_caso(
            parent=self.tab2,
            caso_id=2,
            titulo="Caso 2: Sistema de Diagnostico Medico por Sintomas",
            desc_entradas=["x1 (Fiebre)", "x2 (Cefalea)", "x3 (Fatiga)"],
            w_def=[-0.4, -0.7, 0.3],
            b_def=0.1,
            X=X_CASO2,
            yd=YD_CASO2,
            tiene_presets=True
        )

        self._crear_panel_comparativa(self.tab3)

    def _crear_panel_caso(self, parent, caso_id, titulo, desc_entradas, w_def, b_def, X, yd, tiene_presets=False):
        """
        Genera el panel interactivo dual para un caso de estudio.

        Args:
            parent (ttk.Frame): Contenedor padre de la pestana.
            caso_id (int): Identificador del caso (1 para Paloma, 2 para Diagnostico).
            titulo (str): Titulo descriptivo del problema.
            desc_entradas (list): Etiquetas legibles de las senales de entrada.
            w_def (list): Vector de pesos por defecto W(0).
            b_def (float): Valor de sesgo por defecto b(0).
            X (np.ndarray): Matriz de patrones de entrenamiento.
            yd (np.ndarray): Vector de salidas deseadas.
            tiene_presets (bool): Habilita el selector de inicializaciones predefinidas.

        Retorna:
            dict: Diccionario con referencias a los widgets, figuras y lienzos interactivos.
        """
        panel_izq = ttk.Frame(parent, width=500, padding=8)
        panel_izq.pack(side="left", fill="y", padx=(4, 2), pady=4)

        panel_der = ttk.Frame(parent, padding=8)
        panel_der.pack(side="right", fill="both", expand=True, padx=(2, 4), pady=4)

        # 1. Condiciones Iniciales
        lbl_params = ttk.LabelFrame(panel_izq, text=" Condiciones Iniciales ", padding=8)
        lbl_params.pack(fill="x", pady=(0, 6))

        combo_preset = None
        if tiene_presets:
            f_preset = ttk.Frame(lbl_params)
            f_preset.pack(fill="x", pady=(0, 6))
            ttk.Label(f_preset, text="Configuracion:").pack(side="left")
            combo_preset = ttk.Combobox(f_preset, state="readonly", values=[
                "Experimento Principal (3 Epocas)",
                "Configuracion Optimizada (2 Epocas)",
                "Solucion Directa (1 Epoca)",
                "Personalizado"
            ], width=34)
            combo_preset.current(0)
            combo_preset.pack(side="right", padx=5)

        f_inputs = ttk.Frame(lbl_params)
        f_inputs.pack(fill="x")

        entries_w = []
        for i in range(3):
            ttk.Label(f_inputs, text=f"W{i+1}(0):").grid(row=0, column=i*2, sticky="e", padx=(4, 2))
            ent = ttk.Entry(f_inputs, width=6)
            ent.insert(0, str(w_def[i]))
            ent.grid(row=0, column=i*2+1, sticky="w", padx=(0, 6))
            entries_w.append(ent)

        ttk.Label(f_inputs, text="b(0):").grid(row=0, column=6, sticky="e", padx=(4, 2))
        entry_b = ttk.Entry(f_inputs, width=6)
        entry_b.insert(0, str(b_def))
        entry_b.grid(row=0, column=7, sticky="w")

        f_btn = ttk.Frame(lbl_params)
        f_btn.pack(fill="x", pady=(8, 2))
        btn_entrenar = ttk.Button(f_btn, text="Entrenar Perceptron", style="Accent.TButton",
                                  command=lambda: self._ejecutar_entrenamiento(caso_id))
        btn_entrenar.pack(side="left", expand=True, fill="x", padx=2)

        btn_reset = ttk.Button(f_btn, text="Restablecer",
                               command=lambda: self._reset_parametros(caso_id, w_def, b_def))
        btn_reset.pack(side="right", expand=True, fill="x", padx=2)

        # 2. Resumen de Convergencia con boton para expandir log
        lbl_res = ttk.LabelFrame(panel_izq, text=" Resultados de Convergencia ", padding=8)
        lbl_res.pack(fill="x", pady=(0, 6))

        txt_resultados = tk.Text(lbl_res, height=3, width=54, bg="#ffffff", relief="solid", borderwidth=1, font=("Consolas", 9))
        txt_resultados.pack(fill="x", pady=(0, 4))
        txt_resultados.insert("1.0", "Presione 'Entrenar Perceptron' para iniciar la simulacion.")
        txt_resultados.configure(state="disabled")

        btn_expandir_log = ttk.Button(lbl_res, text="Expandir Log Detallado de Calculos en Ventana Completa",
                                      command=lambda: self._abrir_ventana_log(caso_id))
        btn_expandir_log.pack(fill="x")

        # 3. Sub-Notebook en panel izquierdo: Tabla de Verificacion y Log Integrado
        sub_nb_izq = ttk.Notebook(panel_izq)
        sub_nb_izq.pack(fill="both", expand=True)

        tab_tabla = ttk.Frame(sub_nb_izq)
        tab_log = ttk.Frame(sub_nb_izq)
        sub_nb_izq.add(tab_tabla, text=" Tabla de Verificacion ")
        sub_nb_izq.add(tab_log, text=" Log de Epocas ")

        # Tabla de Verificacion de Patrones
        columnas = ("patron", "entradas", "yd", "y", "a", "estado")
        tree = ttk.Treeview(tab_tabla, columns=columnas, show="headings", height=8)
        tree.heading("patron", text="Patron")
        tree.heading("entradas", text="Entradas [x1, x2, x3]")
        tree.heading("yd", text="yd")
        tree.heading("y", text="y")
        tree.heading("a", text="a (Neta)")
        tree.heading("estado", text="Estado")

        tree.column("patron", width=50, anchor="center")
        tree.column("entradas", width=145, anchor="center")
        tree.column("yd", width=38, anchor="center")
        tree.column("y", width=38, anchor="center")
        tree.column("a", width=65, anchor="center")
        tree.column("estado", width=75, anchor="center")
        tree.pack(fill="both", expand=True)

        # Log de Epocas integrado con Scrollbars
        f_log_text = ttk.Frame(tab_log)
        f_log_text.pack(fill="both", expand=True)
        scroll_y = ttk.Scrollbar(f_log_text, orient="vertical")
        scroll_x = ttk.Scrollbar(f_log_text, orient="horizontal")
        txt_log_embed = tk.Text(f_log_text, wrap="none", font=("Consolas", 8), bg="#ffffff",
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=txt_log_embed.yview)
        scroll_x.config(command=txt_log_embed.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        txt_log_embed.pack(side="left", fill="both", expand=True)
        txt_log_embed.insert("1.0", "El registro detallado de calculos se mostrara tras ejecutar el entrenamiento.")
        txt_log_embed.configure(state="disabled")

        # 4. Panel Derecho: Sub-Notebook con Vistas de Graficas
        sub_nb_der = ttk.Notebook(panel_der)
        sub_nb_der.pack(fill="both", expand=True)

        tab_3d = ttk.Frame(sub_nb_der)
        tab_2d = ttk.Frame(sub_nb_der)
        tab_dual = ttk.Frame(sub_nb_der)

        sub_nb_der.add(tab_3d, text=" Hiperplano 3D (Vista Principal Grande) ")
        sub_nb_der.add(tab_2d, text=" Curva de Aprendizaje 2D ")
        sub_nb_der.add(tab_dual, text=" Vista Dual (2D + 3D) ")

        # 4.1 Vista 3D Grande (Espaciosa, sin compresion)
        fig_3d = Figure(figsize=(7.5, 7.0), dpi=100)
        ax_3d_only = fig_3d.add_subplot(1, 1, 1, projection="3d")
        fig_3d.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.06)
        canvas_3d = FigureCanvasTkAgg(fig_3d, master=tab_3d)
        canvas_3d.draw()
        tb_frame_3d = ttk.Frame(tab_3d)
        tb_frame_3d.pack(side="top", fill="x")
        tb_3d = NavigationToolbar2Tk(canvas_3d, tb_frame_3d)
        tb_3d.update()
        canvas_3d.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # 4.2 Vista 2D Grande
        fig_2d = Figure(figsize=(7.5, 7.0), dpi=100)
        ax_2d_only = fig_2d.add_subplot(1, 1, 1)
        fig_2d.tight_layout(pad=3.0)
        canvas_2d = FigureCanvasTkAgg(fig_2d, master=tab_2d)
        canvas_2d.draw()
        tb_frame_2d = ttk.Frame(tab_2d)
        tb_frame_2d.pack(side="top", fill="x")
        tb_2d = NavigationToolbar2Tk(canvas_2d, tb_frame_2d)
        tb_2d.update()
        canvas_2d.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # 4.3 Vista Dual (3D con 65% de altura y 2D con 35%)
        fig_dual = Figure(figsize=(7.5, 7.0), dpi=100)
        ax_dual_2d = fig_dual.add_subplot(2, 1, 1)
        ax_dual_3d = fig_dual.add_subplot(2, 1, 2, projection="3d")
        fig_dual.tight_layout(pad=3.0)
        canvas_dual = FigureCanvasTkAgg(fig_dual, master=tab_dual)
        canvas_dual.draw()
        tb_frame_dual = ttk.Frame(tab_dual)
        tb_frame_dual.pack(side="top", fill="x")
        tb_dual = NavigationToolbar2Tk(canvas_dual, tb_frame_dual)
        tb_dual.update()
        canvas_dual.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # Estructura del caso
        componentes = {
            "entries_w": entries_w,
            "entry_b": entry_b,
            "combo_preset": combo_preset,
            "txt_res": txt_resultados,
            "txt_log_embed": txt_log_embed,
            "tree": tree,
            "sub_nb_der": sub_nb_der,
            "fig_3d": fig_3d,
            "ax_3d_only": ax_3d_only,
            "canvas_3d": canvas_3d,
            "fig_2d": fig_2d,
            "ax_2d_only": ax_2d_only,
            "canvas_2d": canvas_2d,
            "fig_dual": fig_dual,
            "ax_dual_2d": ax_dual_2d,
            "ax_dual_3d": ax_dual_3d,
            "canvas_dual": canvas_dual,
            "X": X,
            "yd": yd,
            "desc_entradas": desc_entradas,
            "w_def": w_def,
            "b_def": b_def,
            "ultimo_log": ""
        }

        if combo_preset:
            combo_preset.bind("<<ComboboxSelected>>", lambda e: self._on_preset_selected())

        # Renderizar vista inicial de los graficos
        self._graficar_caso(componentes, historial_error=[], ps=None)
        return componentes

    def _crear_panel_comparativa(self, parent):
        """
        Construye la vista de sensibilidad exclusiva para el Caso 2 (Diagnostico Clinico).

        Args:
            parent (ttk.Frame): Contenedor padre de la pestana de comparativa.
        """
        # Banner informativo de contexto claro
        banner = ttk.Frame(parent, padding="10 8 10 8")
        banner.pack(fill="x", padx=6, pady=(4, 6))

        # Cuadro de distincion conceptual
        banner_box = tk.Frame(banner, bg="#e8eff7", relief="solid", borderwidth=1, padx=10, pady=8)
        banner_box.pack(fill="x")

        ttk.Label(banner_box,
                  text="ESTUDIO DE SENSIBILIDAD A LAS CONDICIONES INICIALES W(0) Y b(0) [CASO 2: DIAGNOSTICO MEDICO]",
                  style="BannerTitle.TLabel").pack(anchor="w")

        texto_aclaratorio = (
            "Esta seccion evalua la sensibilidad del Perceptron Simple Bipolar ante tres configuraciones de inicializacion "
            "sinaptica sobre el MISMO dataset de 8 pacientes del Caso 2 (Fiebre, Cefalea y Fatiga).\n"
            "Demuestra como la cercania geometrica del hiperplano inicial respecto a la frontera de decision permite "
            "reducir el aprendizaje de 3 epocas (inicializacion general) a 2 epocas (optimizada) o 1 epoca (solucion directa).\n"
            "*Nota de claridad: El Caso 1 (Paloma) no forma parte de esta comparativa ya que cuenta con sus condiciones fijas de Skinner."
        )
        ttk.Label(banner_box, text=texto_aclaratorio, style="BannerText.TLabel", justify="left").pack(anchor="w", pady=(3, 0))

        # Panel inferior dual
        f_cuerpo = ttk.Frame(parent)
        f_cuerpo.pack(fill="both", expand=True, padx=4, pady=4)

        panel_izq = ttk.Frame(f_cuerpo, width=500, padding=6)
        panel_izq.pack(side="left", fill="y", padx=(2, 2))

        panel_der = ttk.Frame(f_cuerpo, padding=6)
        panel_der.pack(side="right", fill="both", expand=True, padx=(2, 2))

        # Tabla de experimentos
        lbl_resumen = ttk.LabelFrame(panel_izq, text=" Configuraciones Evaluadas en el Caso 2 ", padding=8)
        lbl_resumen.pack(fill="x", pady=(0, 6))

        btn_comp = ttk.Button(lbl_resumen, text="Ejecutar Comparativa de Sensibilidad", style="Accent.TButton",
                              command=self._ejecutar_comparativa)
        btn_comp.pack(fill="x", pady=(0, 6))

        columnas = ("exp", "w0", "b0", "epocas", "w_fin", "b_fin")
        tree_comp = ttk.Treeview(lbl_resumen, columns=columnas, show="headings", height=5)
        tree_comp.heading("exp", text="Experimento (Caso 2)")
        tree_comp.heading("w0", text="W(0)")
        tree_comp.heading("b0", text="b(0)")
        tree_comp.heading("epocas", text="Epocas")
        tree_comp.heading("w_fin", text="W* Final")
        tree_comp.heading("b_fin", text="b* Final")

        tree_comp.column("exp", width=140, anchor="w")
        tree_comp.column("w0", width=95, anchor="center")
        tree_comp.column("b0", width=40, anchor="center")
        tree_comp.column("epocas", width=55, anchor="center")
        tree_comp.column("w_fin", width=95, anchor="center")
        tree_comp.column("b_fin", width=50, anchor="center")
        tree_comp.pack(fill="x")

        # Analisis teorico
        lbl_info = ttk.LabelFrame(panel_izq, text=" Analisis de Sensibilidad Dinamica ", padding=8)
        lbl_info.pack(fill="both", expand=True)

        txt_info = tk.Text(lbl_info, bg="#ffffff", relief="solid", borderwidth=1, font=("Segoe UI", 9), wrap="word")
        txt_info.pack(fill="both", expand=True)
        texto_analisis = (
            "ANALISIS COMPARATIVO DE SENSIBILIDAD (CASO 2):\n\n"
            "1. Experimento Principal (W0=[-0.4, -0.7, 0.3], b0=0.1):\n"
            "   Requiere 3 epocas completas. El hiperplano parte en una orientacion "
            "arbitraria, acumulando un error de E=4 en la epoca 1, E=4 en la epoca 2, "
            "y alcanzando la convergencia perfecta (E=0) en la epoca 3 tras 5 correcciones delta.\n\n"
            "2. Configuracion Optimizada (W0=[-0.9, -0.9, -0.9], b0=0.9):\n"
            "   Acelera la convergencia a 2 epocas. Al orientar los tres pesos sinapticos "
            "negativos con un sesgo positivo alto, el error inicial se reduce a solo E=2, "
            "logrando la calibracion en solo una correccion adicional.\n\n"
            "3. Solucion Directa (W0=[1.0, 1.0, 1.0], b0=0.0):\n"
            "   Convergencia en 1 epoca (0 errores). El vector de pesos ya apunta en la "
            "direccion optima de clasificacion mayoritaria, verificando los 8 patrones "
            "desde el inicio sin requerir ajustes.\n\n"
            "Principio Matematico Clave: En el Perceptron Simple, la velocidad de "
            "aprendizaje es directamente proporcional a la proximidad angular y lineal "
            "del vector normal inicial respecto al cono de soluciones separadoras."
        )
        txt_info.insert("1.0", texto_analisis)
        txt_info.configure(state="disabled")

        # Sub-Notebook en panel derecho para comparativa
        sub_nb_comp = ttk.Notebook(panel_der)
        sub_nb_comp.pack(fill="both", expand=True)

        tab_comp_curvas = ttk.Frame(sub_nb_comp)
        tab_comp_barras = ttk.Frame(sub_nb_comp)
        tab_comp_dual = ttk.Frame(sub_nb_comp)

        sub_nb_comp.add(tab_comp_curvas, text=" Curvas de Aprendizaje Superpuestas ")
        sub_nb_comp.add(tab_comp_barras, text=" Velocidad de Convergencia (Barras) ")
        sub_nb_comp.add(tab_comp_dual, text=" Vista Comparativa Dual ")

        # Curvas superpuestas
        fig_curvas = Figure(figsize=(7.5, 6.8), dpi=100)
        ax_curvas = fig_curvas.add_subplot(1, 1, 1)
        fig_curvas.tight_layout(pad=3.0)
        canvas_curvas = FigureCanvasTkAgg(fig_curvas, master=tab_comp_curvas)
        canvas_curvas.draw()
        tb_f1 = ttk.Frame(tab_comp_curvas)
        tb_f1.pack(side="top", fill="x")
        NavigationToolbar2Tk(canvas_curvas, tb_f1).update()
        canvas_curvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # Barras
        fig_barras = Figure(figsize=(7.5, 6.8), dpi=100)
        ax_barras = fig_barras.add_subplot(1, 1, 1)
        fig_barras.tight_layout(pad=3.0)
        canvas_barras = FigureCanvasTkAgg(fig_barras, master=tab_comp_barras)
        canvas_barras.draw()
        tb_f2 = ttk.Frame(tab_comp_barras)
        tb_f2.pack(side="top", fill="x")
        NavigationToolbar2Tk(canvas_barras, tb_f2).update()
        canvas_barras.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # Dual
        fig_dual_comp = Figure(figsize=(7.5, 6.8), dpi=100)
        ax_d1 = fig_dual_comp.add_subplot(2, 1, 1)
        ax_d2 = fig_dual_comp.add_subplot(2, 1, 2)
        fig_dual_comp.tight_layout(pad=3.0)
        canvas_dual_comp = FigureCanvasTkAgg(fig_dual_comp, master=tab_comp_dual)
        canvas_dual_comp.draw()
        tb_f3 = ttk.Frame(tab_comp_dual)
        tb_f3.pack(side="top", fill="x")
        NavigationToolbar2Tk(canvas_dual_comp, tb_f3).update()
        canvas_dual_comp.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        self.comp_widgets = {
            "tree": tree_comp,
            "fig_curvas": fig_curvas,
            "ax_curvas": ax_curvas,
            "canvas_curvas": canvas_curvas,
            "fig_barras": fig_barras,
            "ax_barras": ax_barras,
            "canvas_barras": canvas_barras,
            "fig_dual_comp": fig_dual_comp,
            "ax_d1": ax_d1,
            "ax_d2": ax_d2,
            "canvas_dual_comp": canvas_dual_comp
        }

        self._ejecutar_comparativa()

    def _on_preset_selected(self):
        """Carga los valores de los experimentos en los campos de entrada del Caso 2."""
        combo = self.componentes_caso2["combo_preset"]
        idx = combo.current()
        presets = [
            ([-0.4, -0.7, 0.3], 0.1),
            ([-0.9, -0.9, -0.9], 0.9),
            ([1.0, 1.0, 1.0], 0.0)
        ]
        if idx < 3:
            w, b = presets[idx]
            for i, ent in enumerate(self.componentes_caso2["entries_w"]):
                ent.delete(0, tk.END)
                ent.insert(0, str(w[i]))
            ent_b = self.componentes_caso2["entry_b"]
            ent_b.delete(0, tk.END)
            ent_b.insert(0, str(b))

    def _reset_parametros(self, caso_id, w_def, b_def):
        """Restaura los valores por defecto del caso seleccionado."""
        comp = self.componentes_caso1 if caso_id == 1 else self.componentes_caso2
        for i, ent in enumerate(comp["entries_w"]):
            ent.delete(0, tk.END)
            ent.insert(0, str(w_def[i]))
        comp["entry_b"].delete(0, tk.END)
        comp["entry_b"].insert(0, str(b_def))
        if comp["combo_preset"]:
            comp["combo_preset"].current(0)

    def _ejecutar_entrenamiento(self, caso_id):
        """
        Entrena el perceptron, captura el log completo y refresca interfaz y graficos.

        Args:
            caso_id (int): Identificador del caso a entrenar (1 o 2).
        """
        comp = self.componentes_caso1 if caso_id == 1 else self.componentes_caso2
        try:
            w0 = [float(ent.get().strip()) for ent in comp["entries_w"]]
            b0 = float(comp["entry_b"].get().strip())
        except ValueError:
            messagebox.showerror("Error de Entrada", "Ingrese valores numericos validos para los pesos y sesgo.")
            return

        X = comp["X"]
        yd = comp["yd"]

        # Instanciar y capturar salida detallada de calculos (identica a terminal)
        ps = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=w0, sesgo_inicial=b0)

        buffer_log = io.StringIO()
        with contextlib.redirect_stdout(buffer_log):
            historial_error = ps.entrenar(X, yd, epocas_max=15, tolerancia=0, verbose=True)

        comp["ultimo_log"] = buffer_log.getvalue()

        # Actualizar resumen de convergencia
        w_fin = [round(float(v), 2) for v in ps.W]
        b_fin = round(float(ps.b), 2)
        txt_res = (
            f"Convergencia: Epoca {ps.epocas_entrenadas} | Error Global Final: {historial_error[-1]}\n"
            f"Pesos Finales W* = {w_fin} | Sesgo Final b* = {b_fin}\n"
            f"Ecuacion del Hiperplano: {w_fin[0]}x1 + {w_fin[1]}x2 + {w_fin[2]}x3 + {b_fin} = 0"
        )
        comp["txt_res"].configure(state="normal")
        comp["txt_res"].delete("1.0", tk.END)
        comp["txt_res"].insert("1.0", txt_res)
        comp["txt_res"].configure(state="disabled")

        # Actualizar log integrado
        comp["txt_log_embed"].configure(state="normal")
        comp["txt_log_embed"].delete("1.0", tk.END)
        comp["txt_log_embed"].insert("1.0", comp["ultimo_log"])
        comp["txt_log_embed"].configure(state="disabled")

        # Actualizar tabla de patrones con formato entero limpio [x1, x2, x3]
        tree = comp["tree"]
        for item in tree.get_children():
            tree.delete(item)

        for i in range(len(yd)):
            a = round(ps.propagacion(X[i]), 2)
            y = ps.predecir(X[i])
            estado_txt = "CORRECTO" if (y == yd[i]) else "ERROR"
            # Formato de entrada limpio como enteros estandar
            entradas_limpias = f"[{int(X[i, 0])}, {int(X[i, 1])}, {int(X[i, 2])}]"
            tree.insert("", "end", values=(f"P{i+1}", entradas_limpias, yd[i], y, a, estado_txt))

        # Renderizar en todas las vistas graficas
        self._graficar_caso(comp, historial_error, ps)

    def _abrir_ventana_log(self, caso_id):
        """
        Abre una ventana emergente maximizable con el log completo de operaciones.

        Args:
            caso_id (int): Identificador del caso de estudio (1 o 2).
        """
        comp = self.componentes_caso1 if caso_id == 1 else self.componentes_caso2
        log_contenido = comp.get("ultimo_log", "")

        if not log_contenido:
            messagebox.showinfo("Sin Datos", "Ejecute primero el entrenamiento para generar el registro de calculos.")
            return

        ventana_log = tk.Toplevel(self.root)
        nombre_caso = "Caso 1: Paloma" if caso_id == 1 else "Caso 2: Diagnostico"
        ventana_log.title(f"Memorias de Calculo Detalladas (Log de Epocas) - {nombre_caso}")
        ventana_log.geometry("1020x680")
        ventana_log.minsize(800, 500)

        # Encabezado de la ventana
        f_top = ttk.Frame(ventana_log, padding=10)
        f_top.pack(fill="x")
        ttk.Label(f_top, text=f"REGISTRO DETALLADO DE MULTIPLICACIONES, SUMAS NETAS Y ACTUALIZACIONES DELTA ({nombre_caso.upper()})",
                  font=("Segoe UI", 10, "bold"), foreground="#1f497d").pack(side="left")

        def copiar_portapapeles():
            ventana_log.clipboard_clear()
            ventana_log.clipboard_append(log_contenido)
            messagebox.showinfo("Copiado", "Registro de calculos copiado al portapapeles.")

        btn_copiar = ttk.Button(f_top, text="Copiar al Portapapeles", command=copiar_portapapeles)
        btn_copiar.pack(side="right", padx=5)

        # Area de texto con scroll
        f_cuerpo = ttk.Frame(ventana_log, padding=10)
        f_cuerpo.pack(fill="both", expand=True)

        sc_y = ttk.Scrollbar(f_cuerpo, orient="vertical")
        sc_x = ttk.Scrollbar(f_cuerpo, orient="horizontal")
        txt_modal = tk.Text(f_cuerpo, wrap="none", font=("Consolas", 9), bg="#ffffff",
                            yscrollcommand=sc_y.set, xscrollcommand=sc_x.set)
        sc_y.config(command=txt_modal.yview)
        sc_x.config(command=txt_modal.xview)
        sc_y.pack(side="right", fill="y")
        sc_x.pack(side="bottom", fill="x")
        txt_modal.pack(side="left", fill="both", expand=True)

        txt_modal.insert("1.0", log_contenido)
        txt_modal.configure(state="disabled")

    def _graficar_caso(self, comp, historial_error, ps):
        """
        Dibuja en las tres vistas: 3D ampliada, 2D ampliada y Vista Dual.

        Args:
            comp (dict): Diccionario de componentes del caso activo.
            historial_error (list): Errores globales acumulados por epoca.
            ps (PerceptronSimpleBipolar, opcional): Modelo entrenado para calcular el hiperplano.
        """
        X = comp["X"]
        yd = comp["yd"]
        desc = comp["desc_entradas"]
        color_linea = "#1f77b4" if comp["w_def"][0] == 0.3 else "#2ca02c"

        # 1. Dibujar Vista 3D Grande (ax_3d_only)
        self._dibujar_espacio_3d(comp["ax_3d_only"], X, yd, desc, ps, titulo="Hiperplano Separador 3D (Manipulable con Raton)")
        comp["fig_3d"].subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.06)
        comp["canvas_3d"].draw()

        # 2. Dibujar Vista 2D Grande (ax_2d_only)
        self._dibujar_curva_2d(comp["ax_2d_only"], historial_error, color_linea, "Curva de Aprendizaje del Perceptron (Error Global vs Epocas)")
        comp["fig_2d"].tight_layout(pad=3.0)
        comp["canvas_2d"].draw()

        # 3. Dibujar Vista Dual
        self._dibujar_curva_2d(comp["ax_dual_2d"], historial_error, color_linea, "Curva de Aprendizaje")
        self._dibujar_espacio_3d(comp["ax_dual_3d"], X, yd, desc, ps, titulo="Hiperplano Separador 3D")
        comp["fig_dual"].tight_layout(pad=2.8)
        comp["canvas_dual"].draw()

    def _dibujar_curva_2d(self, ax, historial_error, color_linea, titulo):
        """
        Renderiza la curva de error en un eje cartesiano bidimensional.

        Args:
            ax (matplotlib.axes.Axes): Eje cartesiano donde se graficara la serie.
            historial_error (list): Registro del error global acumulado por epoca.
            color_linea (str): Codigo de color en formato hexadecimal.
            titulo (str): Titulo explicativo del grafico.
        """
        ax.clear()
        if historial_error:
            epocas = list(range(1, len(historial_error) + 1))
            ax.plot(epocas, historial_error, marker="o", markersize=7, color=color_linea, linewidth=2.2, label="Error Global")
            for ep, err in zip(epocas, historial_error):
                ax.annotate(f"E={err}", (ep, err), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=9, weight="bold")
            ax.set_xticks(epocas)
            ax.set_ylim([-0.5, max(historial_error) + 1.5])
            ax.set_ylabel("Error Acumulado (E_global)", fontsize=9)
            ax.set_xlabel("Epocas de Entrenamiento", fontsize=9)
            ax.set_title(titulo, fontsize=10, weight="bold")
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend(loc="upper right", fontsize=8)
        else:
            ax.text(0.5, 0.5, "Presione 'Entrenar Perceptron' para graficar", ha="center", va="center", transform=ax.transAxes, fontsize=10)
            ax.set_title(titulo, fontsize=10, weight="bold")

    def _dibujar_espacio_3d(self, ax, X, yd, desc, ps, titulo):
        """
        Renderiza los puntos bipolares y la superficie del hiperplano separador en 3D.

        Args:
            ax (mpl_toolkits.mplot3d.Axes3D): Eje tridimensional interactivo.
            X (np.ndarray): Matriz de entradas del problema de tamano (N, 3).
            yd (np.ndarray): Vector de etiquetas deseadas de longitud N.
            desc (list): Etiquetas representativas de las variables [x1, x2, x3].
            ps (PerceptronSimpleBipolar, opcional): Red entrenada para derivar el plano separador.
            titulo (str): Titulo superior de la grafica 3D.
        """
        ax.clear()
        for i in range(len(yd)):
            if yd[i] == 1:
                ax.scatter(X[i, 0], X[i, 1], X[i, 2], color="#1f77b4", s=70, marker="o", label="Clase +1" if i == 0 else "")
            else:
                ax.scatter(X[i, 0], X[i, 1], X[i, 2], color="#d62728", s=80, marker="^", label="Clase -1" if i == 1 else "")
            ax.text(X[i, 0] + 0.06, X[i, 1] + 0.06, X[i, 2] + 0.06, f"P{i+1}", fontsize=9, weight="bold")

        if ps is not None:
            x_range = np.linspace(-1.5, 1.5, 18)
            y_range = np.linspace(-1.5, 1.5, 18)
            X_grid, Y_grid = np.meshgrid(x_range, y_range)

            # Ecuacion W1*x1 + W2*x2 + W3*x3 + b = 0
            if abs(ps.W[2]) > 1e-5:
                Z_grid = -(ps.W[0] * X_grid + ps.W[1] * Y_grid + ps.b) / ps.W[2]
                ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.35, color="cyan", edgecolor="none")
            elif abs(ps.W[1]) > 1e-5:
                Y_grid_calc = -(ps.W[0] * X_grid + ps.W[2] * Y_grid + ps.b) / ps.W[1]
                ax.plot_surface(X_grid, Y_grid_calc, Y_grid, alpha=0.35, color="cyan", edgecolor="none")

        ax.set_xlabel(desc[0], fontsize=8, labelpad=6)
        ax.set_ylabel(desc[1], fontsize=8, labelpad=6)
        ax.set_zlabel(desc[2], fontsize=8, labelpad=6)
        ax.set_xlim([-1.6, 1.6])
        ax.set_ylim([-1.6, 1.6])
        ax.set_zlim([-1.6, 1.6])
        ax.set_title(titulo, fontsize=10, weight="bold")
        ax.legend(loc="upper left", fontsize=8)
        ax.view_init(elev=20, azim=45)

    def _ejecutar_comparativa(self):
        """
        Ejecuta y compara los tres escenarios de convergencia del Caso 2 (Diagnostico).
        """
        configs = [
            ("1. Principal", [-0.4, -0.7, 0.3], 0.1, "#1f77b4"),
            ("2. Optimizado", [-0.9, -0.9, -0.9], 0.9, "#2ca02c"),
            ("3. Solucion Directa", [1.0, 1.0, 1.0], 0.0, "#ff7f0e")
        ]

        tree = self.comp_widgets["tree"]
        for it in tree.get_children():
            tree.delete(it)

        nombres_exp = []
        epocas_totales = []
        historiales = []
        colores = []

        for nombre, w0, b0, color in configs:
            ps = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=w0, sesgo_inicial=b0)
            hist = ps.entrenar(X_CASO2, YD_CASO2, epocas_max=10, tolerancia=0, verbose=False)

            nombres_exp.append(nombre)
            epocas_totales.append(len(hist))
            historiales.append(hist)
            colores.append(color)

            w_fin_str = str([round(float(v), 1) for v in ps.W])
            tree.insert("", "end", values=(nombre, str(w0), b0, len(hist), w_fin_str, round(ps.b, 1)))

        # Dibujar en vista Curvas Superpuestas
        self._dibujar_curvas_superpuestas(self.comp_widgets["ax_curvas"], nombres_exp, historiales, colores)
        self.comp_widgets["fig_curvas"].tight_layout(pad=3.0)
        self.comp_widgets["canvas_curvas"].draw()

        # Dibujar en vista Barras
        self._dibujar_barras_convergencia(self.comp_widgets["ax_barras"], nombres_exp, epocas_totales, colores)
        self.comp_widgets["fig_barras"].tight_layout(pad=3.0)
        self.comp_widgets["canvas_barras"].draw()

        # Dibujar en Vista Dual Comparativa
        self._dibujar_curvas_superpuestas(self.comp_widgets["ax_d1"], nombres_exp, historiales, colores)
        self._dibujar_barras_convergencia(self.comp_widgets["ax_d2"], nombres_exp, epocas_totales, colores)
        self.comp_widgets["fig_dual_comp"].tight_layout(pad=2.8)
        self.comp_widgets["canvas_dual_comp"].draw()

    def _dibujar_curvas_superpuestas(self, ax, nombres, historiales, colores):
        """
        Renderiza la evolucion del error de los tres experimentos del Caso 2.

        Args:
            ax (matplotlib.axes.Axes): Eje cartesiano de destino.
            nombres (list): Nombres de las tres configuraciones evaluadas.
            historiales (list): Listas de error por epoca de cada experimento.
            colores (list): Codigos hexadecimales de color para cada serie.
        """
        ax.clear()
        for nom, hist, col in zip(nombres, historiales, colores):
            epocas_eje = list(range(1, len(hist) + 1))
            ax.plot(epocas_eje, hist, marker="o", markersize=6, linewidth=2.2, color=col, label=f"{nom} ({len(hist)} ep)")
            for ep, err in zip(epocas_eje, hist):
                ax.annotate(f"{err}", (ep, err), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)

        ax.set_title("Comparacion de Curvas de Aprendizaje (Caso 2: Diagnostico)", fontsize=10, weight="bold")
        ax.set_xlabel("Epoca de Entrenamiento", fontsize=9)
        ax.set_ylabel("Error Global Acumulado (E_global)", fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8)

    def _dibujar_barras_convergencia(self, ax, nombres, epocas_totales, colores):
        """
        Renderiza el grafico de barras comparativo de velocidad de convergencia.

        Args:
            ax (matplotlib.axes.Axes): Eje cartesiano de destino.
            nombres (list): Etiquetas de cada configuracion evaluada.
            epocas_totales (list): Cantidad de epocas hasta converger (E=0).
            colores (list): Codigos hexadecimales de color para cada barra.
        """
        ax.clear()
        barras = ax.bar(nombres, epocas_totales, color=colores, width=0.45)
        ax.set_title("Velocidad de Convergencia por Configuracion Inicial (Caso 2)", fontsize=10, weight="bold")
        ax.set_ylabel("Numero de Epocas hasta Converger", fontsize=9)
        ax.set_ylim([0, 4.2])
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        for bar in barras:
            altura = bar.get_height()
            ax.annotate(f"{altura} epocas",
                        xy=(bar.get_x() + bar.get_width() / 2, altura),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, weight="bold")

    def cerrar_aplicacion(self):
        """
        Cierra todas las figuras de Matplotlib de forma limpia y destruye la ventana.
        Evita fugas de memoria y procesos huerfanos al salir del programa.
        """
        plt.close("all")
        self.root.destroy()


def main():
    """
    Punto de entrada principal para inicializar la aplicacion Tkinter.
    """
    root = tk.Tk()
    app = PerceptronGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
