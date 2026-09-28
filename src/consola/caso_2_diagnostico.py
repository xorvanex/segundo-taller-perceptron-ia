# -*- coding: utf-8 -*-
"""
Caso de Estudio 2: Sistema de Diagnóstico Médico Basado en Síntomas
Taller de Perceptrón Simple Bipolar - Inteligencia Artificial (Segundo Corte)
Universidad de Cartagena
Estudiante: Dago David Palmera Navarro
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Agregar directorio padre (src/) al path para importar perceptron
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from perceptron import PerceptronSimpleBipolar

def resolver_caso_2():
    print("=" * 80)
    print(" CASO DE ESTUDIO 2: DIAGNOSTICO MEDICO BASADO EN SINTOMAS")
    print("=" * 80)

    # 1. Cargar patrones de entrenamiento desde data/datasets/
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_base, "..", "..", "data", "datasets", "patrones_caso2_diagnostico.csv")

    datos = np.genfromtxt(ruta_csv, delimiter=',', skip_header=1)
    # Columnas: paciente(0), x1(1), x2(2), x3(3), sintomas(4), diagnostico(5), yd(6)
    X = datos[:, 1:4].astype(int)
    yd = datos[:, 6].astype(int)

    print("\n1. MATRIZ DE PATRONES CLINICOS BIPOLARES:")
    print("-" * 65)
    print(f"{'Paciente':<10} {'x1 (Fiebre)':<14} {'x2 (Cefalea)':<14} {'x3 (Fatiga)':<14} {'yd':<6}")
    print("-" * 65)
    for k in range(len(yd)):
        print(f"P{k+1:<9} {X[k,0]:<14} {X[k,1]:<14} {X[k,2]:<14} {yd[k]:<6}")

    # =========================================================================
    # EXPERIMENTO PRINCIPAL: INICIALIZACION GENERAL (CONVERGENCIA EN 3 EPOCAS)
    # =========================================================================
    W0 = [-0.4, -0.7, 0.3]
    b0 = 0.1
    print(f"\n2. CONDICIONES INICIALES (EXPERIMENTO PRINCIPAL):")
    print(f"   Vector de pesos inicial W(0) = {W0}")
    print(f"   Sesgo inicial b(0)           = {b0}")

    ps_principal = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=W0, sesgo_inicial=b0)
    historial_error = ps_principal.entrenar(X, yd, epocas_max=10, tolerancia=0, verbose=True)

    # 3. Guardar Curva de Aprendizaje Principal en docs/img/
    ruta_img = os.path.join(ruta_base, "..", "..", "docs", "img")
    os.makedirs(ruta_img, exist_ok=True)

    epocas_eje = list(range(1, len(historial_error) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(epocas_eje, historial_error, marker='s', markersize=8, color='#2ca02c', linewidth=2.5, label='Error Global Acumulado (E_global)')
    for ep, err in zip(epocas_eje, historial_error):
        plt.annotate(f'Epoca {ep}: E={err}', (ep, err), textcoords='offset points', xytext=(0, 10), ha='center', fontsize=10, weight='bold')

    plt.title('Caso 2: Curva de Aprendizaje del Perceptron Simple\nEvolucion del Error Global por Epoca (Diagnostico Clinico)', fontsize=12, pad=15)
    plt.xlabel('Epocas de Entrenamiento', fontsize=11)
    plt.ylabel('Error Global Acumulado (E_global)', fontsize=11)
    plt.xticks(epocas_eje, [f'Epoca {i}' for i in epocas_eje])
    plt.ylim([-0.5, max(historial_error) + 2])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper right', fontsize=10)
    plt.tight_layout()

    ruta_grafica_error = os.path.join(ruta_img, "Curva_Aprendizaje_Caso2.png")
    plt.savefig(ruta_grafica_error, dpi=300)
    plt.close()
    print(f"\n[GRAFICA] Curva de aprendizaje guardada en: {ruta_grafica_error}")

    # 4. Guardar Gráfica 3D del Hiperplano Separador en docs/img/
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(yd)):
        if yd[i] == 1:
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color='#d62728', s=90, marker='o', label='Clase +1 (Enfermo)' if i == 3 else '')
        else:
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color='#1f77b4', s=90, marker='^', label='Clase -1 (Sano)' if i == 0 else '')
        ax.text(X[i, 0] + 0.08, X[i, 1] + 0.08, X[i, 2] + 0.08, f'P{i+1}', fontsize=10, weight='bold')

    x1_grid = np.linspace(-1.5, 1.5, 20)
    x2_grid = np.linspace(-1.5, 1.5, 20)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    X3 = -(ps_principal.W[0] * X1 + ps_principal.W[1] * X2 + ps_principal.b) / ps_principal.W[2]

    ax.plot_surface(X1, X2, X3, alpha=0.35, color='orange', edgecolor='none')

    ax.set_title(f'Caso 2: Hiperplano Separador 3D ({ps_principal.W[0]:.1f}x1 + {ps_principal.W[1]:.1f}x2 + {ps_principal.W[2]:.1f}x3 + {ps_principal.b:.1f} = 0)', fontsize=11, pad=15)
    ax.set_xlabel('X1 (Fiebre)', fontsize=10, labelpad=10)
    ax.set_ylabel('X2 (Cefalea)', fontsize=10, labelpad=10)
    ax.set_zlabel('X3 (Fatiga)', fontsize=10, labelpad=10)
    ax.set_xlim([-1.6, 1.6])
    ax.set_ylim([-1.6, 1.6])
    ax.set_zlim([-1.6, 1.6])
    ax.legend(loc='upper left')
    plt.tight_layout()

    ruta_grafica_3d = os.path.join(ruta_img, "Grafica3D_Caso2_Diagnostico.png")
    plt.savefig(ruta_grafica_3d, dpi=300)
    plt.close()
    print(f"[GRAFICA] Hiperplano 3D guardado en: {ruta_grafica_3d}")

    # =========================================================================
    # EXPERIMENTACION COMPARATIVA: CONVERGENCIA EN 2 Y 1 EPOCAS
    # =========================================================================
    print("\n" + "=" * 80)
    print(" EXPERIMENTACION COMPARATIVA DE SENSIBILIDAD A LAS CONDICIONES INICIALES")
    print("=" * 80)

    # Caso 2 Epocas
    W_2ep = [-0.9, -0.9, -0.9]
    b_2ep = 0.9
    ps_2ep = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=W_2ep, sesgo_inicial=b_2ep)
    print("\n--> Entrenando Configuracion Optimizada (W0=[-0.9, -0.9, -0.9], b0=0.9)...")
    hist_2ep = ps_2ep.entrenar(X, yd, epocas_max=10, tolerancia=0, verbose=False)
    print(f"    Convergencia en: {len(hist_2ep)} epocas | Historial de error: {hist_2ep}")
    print(f"    Pesos finales W* = {[round(float(v), 2) for v in ps_2ep.W]}, b* = {round(ps_2ep.b, 2)}")

    # Caso 1 Epoca
    W_1ep = [1.0, 1.0, 1.0]
    b_1ep = 0.0
    ps_1ep = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=W_1ep, sesgo_inicial=b_1ep)
    print("\n--> Evaluando Configuracion de Solucion Directa (W0=[1.0, 1.0, 1.0], b0=0.0)...")
    hist_1ep = ps_1ep.entrenar(X, yd, epocas_max=10, tolerancia=0, verbose=False)
    print(f"    Convergencia en: {len(hist_1ep)} epocas | Historial de error: {hist_1ep}")
    print(f"    Pesos finales W* = {[round(float(v), 2) for v in ps_1ep.W]}, b* = {round(ps_1ep.b, 2)}")

    # Tabla Resumen Comparativo
    print("\n" + "-" * 75)
    print("TABLA COMPARATIVA CONSOLIDADA DE EXPERIMENTOS (CASO 2):")
    print("-" * 75)
    print(f"{'Experimento':<24} {'W(0)':<20} {'b(0)':<8} {'Epocas':<8} {'W* Final':<20} {'b* Final':<8}")
    print("-" * 75)
    print(f"{'1. Principal (Aleatorio)':<24} {str(W0):<20} {b0:<8} {len(historial_error):<8} {str([round(float(v),1) for v in ps_principal.W]):<20} {round(ps_principal.b,1):<8}")
    print(f"{'2. Optimizado':<24} {str(W_2ep):<20} {b_2ep:<8} {len(hist_2ep):<8} {str([round(float(v),1) for v in ps_2ep.W]):<20} {round(ps_2ep.b,1):<8}")
    print(f"{'3. Solucion Directa':<24} {str(W_1ep):<20} {b_1ep:<8} {len(hist_1ep):<8} {str([round(float(v),1) for v in ps_1ep.W]):<20} {round(ps_1ep.b,1):<8}")
    print("-" * 75 + "\n")

if __name__ == "__main__":
    resolver_caso_2()
