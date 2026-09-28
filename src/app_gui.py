# -*- coding: utf-8 -*-
"""
Interfaz Grafica de Usuario (GUI) - Perceptron Simple Bipolar
Taller de Inteligencia Artificial - Corte 2
Universidad de Cartagena
Autores: Dago David Palmera Navarro, Julian David Camargo Padilla
"""

import os
import sys
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
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Perceptron Simple Bipolar - Inteligencia Artificial")
        self.root.geometry("1260x780")
        self.root.minsize(1050, 680)

        # Protocolo para cierre seguro sin recursos huerfanos
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        """Configura el esquema visual formal y profesional."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Colores institucionales
        azul_primario = "#1f497d"
        gris_fondo = "#f4f6f9"
        
        self.root.configure(bg=gris_fondo)
        style.configure("TFrame", background=gris_fondo)
        style.configure("TLabelframe", background=gris_fondo, font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe.Label", background=gris_fondo, foreground=azul_primario)
        style.configure("TLabel", background=gris_fondo, font=("Segoe UI", 9))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=azul_primario, background=gris_fondo)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#333333", background=gris_fondo)
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), padding=6, background=azul_primario, foreground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e1e6eb")

    def _construir_interfaz(self):
        """Construye el encabezado principal y las pestanas de analisis."""
        # Encabezado institucional
        header_frame = ttk.Frame(self.root, padding="10 8 10 5")
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="UNIVERSIDAD DE CARTAGENA - FACULTAD DE INGENIERIA", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Taller de Perceptron Simple Bipolar (Corte 2) | Autores: Dago David Palmera Navarro, Julian David Camargo Padilla", style="SubHeader.TLabel").pack(anchor="w")

        # Pestanas de navegacion (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text=" Caso 1: Paloma ")
        self.notebook.add(self.tab2, text=" Caso 2: Diagnostico Clinico ")
        self.notebook.add(self.tab3, text=" Comparativa de Sensibilidad ")

        # Construccion modular de cada vista
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
        """Genera el panel dual interactivo: controles a la izquierda, graficas a la derecha."""
        panel_izq = ttk.Frame(parent, width=470, padding=8)
        panel_izq.pack(side="left", fill="y", padx=(5, 2), pady=5)

        panel_der = ttk.Frame(parent, padding=8)
        panel_der.pack(side="right", fill="both", expand=True, padx=(2, 5), pady=5)

        # 1. Marco de Parametros Iniciales
        lbl_params = ttk.LabelFrame(panel_izq, text=" Condiciones Iniciales ", padding=8)
        lbl_params.pack(fill="x", pady=(0, 6))

        # Selector de presets para el Caso 2
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
            ], width=32)
            combo_preset.current(0)
            combo_preset.pack(side="right", padx=5)

        # Entradas de W y b
        f_inputs = ttk.Frame(lbl_params)
        f_inputs.pack(fill="x")

        entries_w = []
        for i in range(3):
            ttk.Label(f_inputs, text=f"W{i+1}(0):").grid(row=0, column=i*2, sticky="e", padx=(4, 2))
            ent = ttk.Entry(f_inputs, width=6)
            ent.insert(0, str(w_def[i]))
            ent.grid(row=0, column=i*2+1, sticky="w", padx=(0, 8))
            entries_w.append(ent)

        ttk.Label(f_inputs, text="b(0):").grid(row=0, column=6, sticky="e", padx=(4, 2))
        entry_b = ttk.Entry(f_inputs, width=6)
        entry_b.insert(0, str(b_def))
        entry_b.grid(row=0, column=7, sticky="w")

        # Botones de accion
        f_btn = ttk.Frame(lbl_params)
        f_btn.pack(fill="x", pady=(8, 2))
        btn_entrenar = ttk.Button(f_btn, text="Entrenar Perceptron", style="Accent.TButton",
                                  command=lambda: self._ejecutar_entrenamiento(caso_id))
        btn_entrenar.pack(side="left", expand=True, fill="x", padx=2)

        btn_reset = ttk.Button(f_btn, text="Restablecer",
                               command=lambda: self._reset_parametros(caso_id, w_def, b_def))
        btn_reset.pack(side="right", expand=True, fill="x", padx=2)

        # 2. Marco de Metricas de Convergencia
        lbl_res = ttk.LabelFrame(panel_izq, text=" Resultados de Convergencia ", padding=8)
        lbl_res.pack(fill="x", pady=(0, 6))

        txt_resultados = tk.Text(lbl_res, height=4, width=54, bg="#ffffff", relief="solid", borderwidth=1, font=("Consolas", 9))
        txt_resultados.pack(fill="x")
        txt_resultados.insert("1.0", "Presione 'Entrenar Perceptron' para iniciar la simulacion.")
        txt_resultados.configure(state="disabled")

        # 3. Marco de Verificacion de Patrones (Treeview)
        lbl_tabla = ttk.LabelFrame(panel_izq, text=" Verificacion de Clasificacion ", padding=6)
        lbl_tabla.pack(fill="both", expand=True)

        columnas = ("patron", "entradas", "yd", "y", "a", "estado")
        tree = ttk.Treeview(lbl_tabla, columns=columnas, show="headings", height=8)
        tree.heading("patron", text="Patron")
        tree.heading("entradas", text="Entradas [x1, x2, x3]")
        tree.heading("yd", text="yd")
        tree.heading("y", text="y")
        tree.heading("a", text="a (Neta)")
        tree.heading("estado", text="Estado")

        tree.column("patron", width=55, anchor="center")
        tree.column("entradas", width=140, anchor="center")
        tree.column("yd", width=40, anchor="center")
        tree.column("y", width=40, anchor="center")
        tree.column("a", width=65, anchor="center")
        tree.column("estado", width=80, anchor="center")
        tree.pack(fill="both", expand=True)

        # 4. Marco de Graficos Interactivos (Canvas Matplotlib)
        fig = Figure(figsize=(6.2, 6.6), dpi=95)
        ax_2d = fig.add_subplot(2, 1, 1)
        ax_3d = fig.add_subplot(2, 1, 2, projection="3d")
        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=panel_der)
        canvas.draw()
        
        # Barra de navegacion interactiva (permite rotacion 3D fluida y zoom)
        toolbar_frame = ttk.Frame(panel_der)
        toolbar_frame.pack(side="top", fill="x")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # Registro de componentes
        componentes = {
            "entries_w": entries_w,
            "entry_b": entry_b,
            "combo_preset": combo_preset,
            "txt_res": txt_resultados,
            "tree": tree,
            "fig": fig,
            "ax_2d": ax_2d,
            "ax_3d": ax_3d,
            "canvas": canvas,
            "X": X,
            "yd": yd,
            "desc_entradas": desc_entradas,
            "w_def": w_def,
            "b_def": b_def
        }

        if combo_preset:
            combo_preset.bind("<<ComboboxSelected>>", lambda e: self._on_preset_selected())

        # Dibujar estado inicial en el canvas
        self._graficar_caso(componentes, historial_error=[], ps=None)
        return componentes

    def _crear_panel_comparativa(self, parent):
        """Construye la vista de comparacion de sensibilidad entre configuraciones (Caso 2)."""
        panel_izq = ttk.Frame(parent, width=470, padding=8)
        panel_izq.pack(side="left", fill="y", padx=(5, 2), pady=5)

        panel_der = ttk.Frame(parent, padding=8)
        panel_der.pack(side="right", fill="both", expand=True, padx=(2, 5), pady=5)

        # Tabla de experimentos
        lbl_resumen = ttk.LabelFrame(panel_izq, text=" Experimentos de Sensibilidad a W(0) y b(0) ", padding=8)
        lbl_resumen.pack(fill="x", pady=(0, 8))

        btn_comp = ttk.Button(lbl_resumen, text="Ejecutar Comparativa Completa", style="Accent.TButton",
                              command=self._ejecutar_comparativa)
        btn_comp.pack(fill="x", pady=(0, 6))

        columnas = ("exp", "w0", "b0", "epocas", "w_fin", "b_fin")
        tree_comp = ttk.Treeview(lbl_resumen, columns=columnas, show="headings", height=5)
        tree_comp.heading("exp", text="Experimento")
        tree_comp.heading("w0", text="W(0)")
        tree_comp.heading("b0", text="b(0)")
        tree_comp.heading("epocas", text="Epocas")
        tree_comp.heading("w_fin", text="W* Final")
        tree_comp.heading("b_fin", text="b* Final")

        tree_comp.column("exp", width=120, anchor="w")
        tree_comp.column("w0", width=95, anchor="center")
        tree_comp.column("b0", width=40, anchor="center")
        tree_comp.column("epocas", width=55, anchor="center")
        tree_comp.column("w_fin", width=95, anchor="center")
        tree_comp.column("b_fin", width=50, anchor="center")
        tree_comp.pack(fill="x")

        # Texto explicativo del analisis de sensibilidad
        lbl_info = ttk.LabelFrame(panel_izq, text=" Analisis de Sensibilidad ", padding=8)
        lbl_info.pack(fill="both", expand=True)

        txt_info = tk.Text(lbl_info, bg="#ffffff", relief="solid", borderwidth=1, font=("Segoe UI", 9), wrap="word")
        txt_info.pack(fill="both", expand=True)
        texto_analisis = (
            "HALLAZGOS DEL ANALISIS DE SENSIBILIDAD:\n\n"
            "1. Experimento Principal (W0=[-0.4, -0.7, 0.3], b0=0.1):\n"
            "   Convergencia en 3 epocas. Los pesos iniciales arbitrarios requieren "
            "ajustes secuenciales a traves de 5 correcciones delta para alinear el hiperplano.\n\n"
            "2. Configuracion Optimizada (W0=[-0.9, -0.9, -0.9], b0=0.9):\n"
            "   Convergencia acelerada en 2 epocas. La orientacion inicial se aproxima "
            "al sector de clasificacion, reduciendo el error global inicial.\n\n"
            "3. Solucion Directa (W0=[1.0, 1.0, 1.0], b0=0.0):\n"
            "   Convergencia en 1 epoca (0 errores). El vector inicial satisface "
            "inmediatamente la separabilidad lineal del conjunto sin requerir aprendizaje.\n\n"
            "Conclusion: La velocidad de aprendizaje depende directamente de la "
            "proximidad entre el hiperplano inicial y la frontera de decision optima."
        )
        txt_info.insert("1.0", texto_analisis)
        txt_info.configure(state="disabled")

        # Graficos comparativos
        fig_comp = Figure(figsize=(6.2, 6.6), dpi=95)
        ax_comp_2d = fig_comp.add_subplot(2, 1, 1)
        ax_comp_bar = fig_comp.add_subplot(2, 1, 2)
        fig_comp.tight_layout(pad=3.0)

        canvas_comp = FigureCanvasTkAgg(fig_comp, master=panel_der)
        canvas_comp.draw()

        toolbar_f = ttk.Frame(panel_der)
        toolbar_f.pack(side="top", fill="x")
        toolbar = NavigationToolbar2Tk(canvas_comp, toolbar_f)
        toolbar.update()
        canvas_comp.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        self.comp_widgets = {
            "tree": tree_comp,
            "fig": fig_comp,
            "ax_2d": ax_comp_2d,
            "ax_bar": ax_comp_bar,
            "canvas": canvas_comp
        }
        
        # Ejecucion automatica inicial de la comparativa
        self._ejecutar_comparativa()

    def _on_preset_selected(self):
        """Actualiza los campos de entrada de acuerdo al preset seleccionado en el Caso 2."""
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
        """Restaura los valores por defecto de los pesos y sesgo."""
        comp = self.componentes_caso1 if caso_id == 1 else self.componentes_caso2
        for i, ent in enumerate(comp["entries_w"]):
            ent.delete(0, tk.END)
            ent.insert(0, str(w_def[i]))
        comp["entry_b"].delete(0, tk.END)
        comp["entry_b"].insert(0, str(b_def))
        if comp["combo_preset"]:
            comp["combo_preset"].current(0)

    def _ejecutar_entrenamiento(self, caso_id):
        """Entrena el perceptron, actualiza tabla de verificacion y genera graficas."""
        comp = self.componentes_caso1 if caso_id == 1 else self.componentes_caso2
        try:
            w0 = [float(ent.get().strip()) for ent in comp["entries_w"]]
            b0 = float(comp["entry_b"].get().strip())
        except ValueError:
            messagebox.showerror("Error de Entrada", "Ingrese valores numericos validos para los pesos y sesgo.")
            return

        X = comp["X"]
        yd = comp["yd"]

        # Instanciar y entrenar Perceptron Simple Bipolar
        ps = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=w0, sesgo_inicial=b0)
        historial_error = ps.entrenar(X, yd, epocas_max=15, tolerancia=0, verbose=False)

        # Actualizar texto de resultados
        w_fin = [round(float(v), 2) for v in ps.W]
        b_fin = round(float(ps.b), 2)
        txt = (
            f"Convergencia: Epoca {ps.epocas_entrenadas} | Error Global Final: {historial_error[-1]}\n"
            f"Pesos Finales W* = {w_fin}\n"
            f"Sesgo Final b*   = {b_fin}\n"
            f"Ecuacion del Hiperplano: {w_fin[0]}x1 + {w_fin[1]}x2 + {w_fin[2]}x3 + {b_fin} = 0"
        )
        comp["txt_res"].configure(state="normal")
        comp["txt_res"].delete("1.0", tk.END)
        comp["txt_res"].insert("1.0", txt)
        comp["txt_res"].configure(state="disabled")

        # Actualizar tabla de patrones y aciertos
        tree = comp["tree"]
        for item in tree.get_children():
            tree.delete(item)

        aciertos = 0
        for i in range(len(yd)):
            a = round(ps.propagacion(X[i]), 2)
            y = ps.predecir(X[i])
            es_correcto = (y == yd[i])
            if es_correcto:
                aciertos += 1
            estado_txt = "CORRECTO" if es_correcto else "ERROR"
            tree.insert("", "end", values=(f"P{i+1}", str(list(X[i])), yd[i], y, a, estado_txt))

        # Renderizar graficos interactivos
        self._graficar_caso(comp, historial_error, ps)

    def _graficar_caso(self, comp, historial_error, ps):
        """Renderiza la curva de aprendizaje 2D y el hiperplano 3D con manipulacion de mouse."""
        ax_2d = comp["ax_2d"]
        ax_3d = comp["ax_3d"]
        fig = comp["fig"]
        X = comp["X"]
        yd = comp["yd"]
        desc = comp["desc_entradas"]

        ax_2d.clear()
        ax_3d.clear()

        # 1. Curva de Aprendizaje 2D
        if historial_error:
            epocas = list(range(1, len(historial_error) + 1))
            color_linea = "#1f77b4" if comp["w_def"][0] == 0.3 else "#2ca02c"
            ax_2d.plot(epocas, historial_error, marker="o", markersize=6, color=color_linea, linewidth=2, label="Error Global")
            for ep, err in zip(epocas, historial_error):
                ax_2d.annotate(f"E={err}", (ep, err), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, weight="bold")
            ax_2d.set_xticks(epocas)
            ax_2d.set_ylim([-0.5, max(historial_error) + 1.5])
            ax_2d.set_ylabel("Error Acumulado")
            ax_2d.set_title(f"Curva de Aprendizaje (Convergencia en {len(historial_error)} Epocas)", fontsize=10, weight="bold")
            ax_2d.grid(True, linestyle="--", alpha=0.6)
            ax_2d.legend(loc="upper right", fontsize=8)
        else:
            ax_2d.text(0.5, 0.5, "Haga clic en 'Entrenar Perceptron' para graficar", ha="center", va="center", transform=ax_2d.transAxes, fontsize=9)
            ax_2d.set_title("Curva de Aprendizaje", fontsize=10, weight="bold")

        # 2. Espacio de Patrones e Hiperplano Separador 3D
        for i in range(len(yd)):
            if yd[i] == 1:
                ax_3d.scatter(X[i, 0], X[i, 1], X[i, 2], color="#1f77b4", s=60, marker="o", label="Clase +1" if i == 0 else "")
            else:
                ax_3d.scatter(X[i, 0], X[i, 1], X[i, 2], color="#d62728", s=70, marker="^", label="Clase -1" if i == 1 else "")
            ax_3d.text(X[i, 0] + 0.05, X[i, 1] + 0.05, X[i, 2] + 0.05, f"P{i+1}", fontsize=8, weight="bold")

        if ps is not None:
            # Generacion de malla para el hiperplano
            x_range = np.linspace(-1.5, 1.5, 15)
            y_range = np.linspace(-1.5, 1.5, 15)
            X_grid, Y_grid = np.meshgrid(x_range, y_range)

            # Ecuacion del plano W1*x1 + W2*x2 + W3*x3 + b = 0
            if abs(ps.W[2]) > 1e-5:
                Z_grid = -(ps.W[0] * X_grid + ps.W[1] * Y_grid + ps.b) / ps.W[2]
                ax_3d.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.3, color="cyan", edgecolor="none")
            elif abs(ps.W[1]) > 1e-5:
                Y_grid_calc = -(ps.W[0] * X_grid + ps.W[2] * Y_grid + ps.b) / ps.W[1]
                ax_3d.plot_surface(X_grid, Y_grid_calc, Y_grid, alpha=0.3, color="cyan", edgecolor="none")

        ax_3d.set_xlabel(desc[0], fontsize=8, labelpad=5)
        ax_3d.set_ylabel(desc[1], fontsize=8, labelpad=5)
        ax_3d.set_zlabel(desc[2], fontsize=8, labelpad=5)
        ax_3d.set_xlim([-1.6, 1.6])
        ax_3d.set_ylim([-1.6, 1.6])
        ax_3d.set_zlim([-1.6, 1.6])
        ax_3d.set_title("Hiperplano Separador 3D (Rotable con Mouse)", fontsize=10, weight="bold")
        ax_3d.legend(loc="upper left", fontsize=7)
        ax_3d.view_init(elev=20, azim=45)

        fig.tight_layout(pad=2.5)
        comp["canvas"].draw()

    def _ejecutar_comparativa(self):
        """Ejecuta y compara los 3 escenarios de inicializacion del Caso 2."""
        configs = [
            ("Principal", [-0.4, -0.7, 0.3], 0.1, "#1f77b4"),
            ("Optimizado", [-0.9, -0.9, -0.9], 0.9, "#2ca02c"),
            ("Solucion Directa", [1.0, 1.0, 1.0], 0.0, "#ff7f0e")
        ]

        tree = self.comp_widgets["tree"]
        for it in tree.get_children():
            tree.delete(it)

        ax_2d = self.comp_widgets["ax_2d"]
        ax_bar = self.comp_widgets["ax_bar"]
        fig = self.comp_widgets["fig"]

        ax_2d.clear()
        ax_bar.clear()

        nombres_exp = []
        epocas_totales = []

        for nombre, w0, b0, color in configs:
            ps = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=w0, sesgo_inicial=b0)
            hist = ps.entrenar(X_CASO2, YD_CASO2, epocas_max=10, tolerancia=0, verbose=False)
            
            nombres_exp.append(nombre)
            epocas_totales.append(len(hist))

            w_fin_str = str([round(float(v), 1) for v in ps.W])
            tree.insert("", "end", values=(nombre, str(w0), b0, len(hist), w_fin_str, round(ps.b, 1)))

            # Graficar curvas de aprendizaje superpuestas
            epocas_eje = list(range(1, len(hist) + 1))
            ax_2d.plot(epocas_eje, hist, marker="o", linewidth=2, color=color, label=f"{nombre} ({len(hist)} epocas)")
            for ep, err in zip(epocas_eje, hist):
                ax_2d.annotate(f"{err}", (ep, err), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)

        ax_2d.set_title("Comparacion de Curvas de Aprendizaje (Error Global por Epoca)", fontsize=10, weight="bold")
        ax_2d.set_xlabel("Epoca")
        ax_2d.set_ylabel("Error Global Acumulado")
        ax_2d.grid(True, linestyle="--", alpha=0.6)
        ax_2d.legend(loc="upper right", fontsize=8)

        # Grafico de barras: Epocas de convergencia
        colores_barras = ["#1f77b4", "#2ca02c", "#ff7f0e"]
        barras = ax_bar.bar(nombres_exp, epocas_totales, color=colores_barras, width=0.45)
        ax_bar.set_title("Velocidad de Convergencia (Epocas hasta E_global = 0)", fontsize=10, weight="bold")
        ax_bar.set_ylabel("Numero de Epocas")
        ax_bar.set_ylim([0, 4.5])
        ax_bar.grid(axis="y", linestyle="--", alpha=0.6)

        for bar in barras:
            altura = bar.get_height()
            ax_bar.annotate(f"{altura} epocas",
                            xy=(bar.get_x() + bar.get_width() / 2, altura),
                            xytext=(0, 4), textcoords="offset points",
                            ha="center", va="bottom", fontsize=9, weight="bold")

        fig.tight_layout(pad=2.5)
        self.comp_widgets["canvas"].draw()

    def cerrar_aplicacion(self):
        """Cierra todas las figuras de Matplotlib y destruye la ventana principal."""
        plt.close("all")
        self.root.destroy()


def main():
    root = tk.Tk()
    app = PerceptronGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
