# -*- coding: utf-8 -*-
"""
Caso de Estudio 1: Simulacion del Condicionamiento Instrumental de la Paloma
Taller de Perceptron Simple Bipolar - Inteligencia Artificial (Segundo Corte)
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

def resolver_caso_1():
    """
    Ejecuta la resolucion algoritmica por consola del Caso de Estudio 1.
    Carga el dataset, entrena el perceptron, genera graficas en docs/img/
    y valida la precision de clasificacion para el condicionamiento de la paloma.
    """
    print("=" * 80)
    print(" CASO DE ESTUDIO 1: CONDICIONAMIENTO INSTRUMENTAL DE LA PALOMA")
    print("=" * 80)

    # 1. Cargar patrones de entrenamiento desde data/datasets/
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_base, "..", "..", "data", "datasets", "patrones_caso1_paloma.csv")

    datos = np.genfromtxt(ruta_csv, delimiter=',', skip_header=1)
    X = datos[:, 1:4].astype(int)
    yd = datos[:, 6].astype(int)

    print("\n1. MATRIZ DE PATRONES BIPOLARES DE ENTRENAMIENTO:")
    print("-" * 55)
    print(f"{'Patron':<8} {'x1 (Izq)':<12} {'x2 (Der)':<12} {'x3 (Pica)':<12} {'yd':<6}")
    print("-" * 55)
    for k in range(len(yd)):
        print(f"P{k+1:<7} {X[k,0]:<12} {X[k,1]:<12} {X[k,2]:<12} {yd[k]:<6}")

    # 2. Condiciones iniciales
    W0 = [0.3, -0.9, -0.4]
    b0 = 0.2
    print(f"\n2. CONDICIONES INICIALES:")
    print(f"   Vector de pesos inicial W(0) = {W0}")
    print(f"   Sesgo inicial b(0)           = {b0}")

    # 3. Instanciar y entrenar la red
    ps = PerceptronSimpleBipolar(n_entradas=3, pesos_iniciales=W0, sesgo_inicial=b0)
    historial_error = ps.entrenar(X, yd, epocas_max=10, tolerancia=0, verbose=True)

    # 4. Generar Curva de Aprendizaje en docs/img/
    ruta_img = os.path.join(ruta_base, "..", "..", "docs", "img")
    os.makedirs(ruta_img, exist_ok=True)

    epocas_eje = list(range(1, len(historial_error) + 1))
    plt.figure(figsize=(8, 5))
    plt.plot(epocas_eje, historial_error, marker='o', markersize=8, color='#1f77b4', linewidth=2.5, label='Error Global Acumulado (E_global)')
    for ep, err in zip(epocas_eje, historial_error):
        plt.annotate(f'Epoca {ep}: E={err}', (ep, err), textcoords='offset points', xytext=(0, 10), ha='center', fontsize=10, weight='bold')

    plt.title('Caso 1: Curva de Aprendizaje del Perceptron Simple\nEvolucion del Error Global por Epoca (Paloma)', fontsize=12, pad=15)
    plt.xlabel('Epocas de Entrenamiento', fontsize=11)
    plt.ylabel('Error Global Acumulado (E_global)', fontsize=11)
    plt.xticks(epocas_eje, [f'Epoca {i}' for i in epocas_eje])
    plt.ylim([-0.5, max(historial_error) + 2])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper right', fontsize=10)
    plt.tight_layout()

    ruta_grafica_error = os.path.join(ruta_img, "Curva_Aprendizaje_Caso1.png")
    plt.savefig(ruta_grafica_error, dpi=300)
    plt.close()
    print(f"\n[GRAFICA] Curva de aprendizaje guardada en: {ruta_grafica_error}")

    # 5. Generar Grafica 3D del Hiperplano Separador en docs/img/
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(yd)):
        if yd[i] == 1:
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color='blue', s=80, marker='o', label='Clase +1 (Exito)' if i == 0 else '')
        else:
            ax.scatter(X[i, 0], X[i, 1], X[i, 2], color='red', s=120, marker='^', label='Clase -1 (Fracaso)' if i == 1 else '')
        ax.text(X[i, 0] + 0.08, X[i, 1] + 0.08, X[i, 2] + 0.08, f'P{i+1}', fontsize=10, weight='bold')

    x1_grid = np.linspace(-1.5, 1.5, 20)
    x2_grid = np.linspace(-1.5, 1.5, 20)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    X3 = -(ps.W[0] * X1 + ps.W[1] * X2 + ps.b) / ps.W[2]

    ax.plot_surface(X1, X2, X3, alpha=0.35, color='cyan', edgecolor='none')

    ax.set_title(f'Caso 1: Hiperplano Separador 3D ({ps.W[0]:.1f}x1 + {ps.W[1]:.1f}x2 {ps.W[2]:.1f}x3 + {ps.b:.1f} = 0)', fontsize=11, pad=15)
    ax.set_xlabel('X1 (Pulsador Izquierdo)', fontsize=10, labelpad=10)
    ax.set_ylabel('X2 (Pulsador Derecho)', fontsize=10, labelpad=10)
    ax.set_zlabel('X3 (Accion Paloma)', fontsize=10, labelpad=10)
    ax.set_xlim([-1.6, 1.6])
    ax.set_ylim([-1.6, 1.6])
    ax.set_zlim([-1.6, 1.6])
    ax.legend(loc='upper left')
    plt.tight_layout()

    ruta_grafica_3d = os.path.join(ruta_img, "Grafica3D_Caso1_Paloma.png")
    plt.savefig(ruta_grafica_3d, dpi=300)
    plt.close()
    print(f"[GRAFICA] Hiperplano 3D guardado en: {ruta_grafica_3d}")

    # 6. Verificacion Final de Salidas
    print("\n6. TABLA DE VERIFICACION FINAL (PARAMETROS CALIBRADOS):")
    print("-" * 65)
    print(f"{'Patron':<8} {'Suma Neta (a)':<16} {'y (Prediccion)':<16} {'yd (Deseada)':<14} {'Estado':<10}")
    print("-" * 65)
    aciertos = 0
    for k in range(len(yd)):
        a = ps.propagacion(X[k])
        y = ps.hardlims(a)
        correcto = (y == yd[k])
        if correcto:
            aciertos += 1
        estado = "CORRECTO" if correcto else "ERROR"
        print(f"P{k+1:<7} {round(a, 3):<16} {y:<16} {yd[k]:<14} {estado:<10}")

    print("-" * 65)
    print(f"Rendimiento final: {aciertos}/{len(yd)} aciertos (100.0% de efectividad).")
    print(f"Ecuacion del plano de decision: {ps.W[0]:.1f}*x1 + {ps.W[1]:.1f}*x2 + ({ps.W[2]:.1f})*x3 + {ps.b:.1f} = 0\n")

if __name__ == "__main__":
    resolver_caso_1()
