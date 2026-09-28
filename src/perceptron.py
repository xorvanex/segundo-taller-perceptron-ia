# -*- coding: utf-8 -*-
"""
Modulo del Perceptron Simple Bipolar (PS)
Implementa la arquitectura monocapa con funcion de activacion hardlims
y la regla de aprendizaje delta supervisado en dominio bipolar {-1, +1}.
"""

import numpy as np


class PerceptronSimpleBipolar:
    """
    Red Neuronal Monocapa tipo Perceptron Simple Bipolar.

    Atributos:
        n_entradas (int): Numero de senales de entrada de la red.
        W (np.ndarray): Vector de pesos sinapticos [w1, w2, ..., wn].
        b (float): Termino de sesgo (polarizacion independiente).
        historial_error (list): Registro del error global acumulado por epoca.
        epocas_entrenadas (int): Contador total de epocas ejecutadas.
    """

    def __init__(self, n_entradas=3, pesos_iniciales=None, sesgo_inicial=None):
        """
        Inicializa los pesos sinapticos y el sesgo de la neurona.

        Args:
            n_entradas (int): Dimension del vector de caracteristicas de entrada.
            pesos_iniciales (list|np.ndarray, opcional): Vector inicial W(0).
            sesgo_inicial (float, opcional): Valor escalar del sesgo inicial b(0).
        """
        self.n_entradas = n_entradas

        # Inicializacion de pesos definidos o aleatorios en [-1.0, 1.0]
        if pesos_iniciales is not None:
            self.W = np.array(pesos_iniciales, dtype=float)
        else:
            self.W = np.round(np.random.uniform(-1.0, 1.0, size=n_entradas), 2)

        # Inicializacion de sesgo definido o aleatorio en [0.0, 1.0]
        if sesgo_inicial is not None:
            self.b = float(sesgo_inicial)
        else:
            self.b = float(np.round(np.random.uniform(0.0, 1.0), 2))

        self.historial_error = []
        self.epocas_entrenadas = 0

    @staticmethod
    def hardlims(a):
        """
        Funcion de activacion escalon simetrica (hardlims).

        Retorna:
            int: +1 si la suma neta a >= 0, de lo contrario -1.
        """
        return 1 if a >= 0 else -1

    def propagacion(self, X):
        """
        Calcula la combinacion lineal ponderada de las entradas (suma neta a).

        Formula:
            a = W^T * X + b = sum(wi * xi) + b
        """
        return float(np.dot(self.W, X) + self.b)

    def predecir(self, X):
        """
        Clasifica un vector de entrada aplicando hardlims sobre la suma neta.

        Retorna:
            int: Salida bipolar predicha {-1, +1}.
        """
        a = self.propagacion(X)
        return self.hardlims(a)

    def entrenar(self, X_train, y_train, epocas_max=100, tolerancia=0, verbose=True):
        """
        Ejecuta el entrenamiento supervisado mediante la Regla de Aprendizaje Delta.

        Args:
            X_train (np.ndarray): Matriz de patrones de entrenamiento de tamano (N, n_entradas).
            y_train (np.ndarray): Vector de salidas deseadas yd de longitud N en {-1, +1}.
            epocas_max (int): Limite maximo de ciclos de entrenamiento.
            tolerancia (int): Umbral de error global acumulado para detener el proceso.
            verbose (bool): Si es True, imprime la traza tabular detallada paso a paso.

        Retorna:
            list: Historial de error global acumulado al cierre de cada epoca.
        """
        N = len(y_train)
        self.historial_error = []
        self.epocas_entrenadas = 0

        while self.epocas_entrenadas < epocas_max:
            self.epocas_entrenadas += 1
            error_global = 0

            # Encabezado formal de la epoca en curso
            if verbose:
                w_str = [round(float(val), 4) for val in self.W]
                print(f"\n{'='*75}")
                print(f"EPOCA {self.epocas_entrenadas} | Estado inicial: W={w_str}, b={round(self.b, 4)}")
                print(f"{'='*75}")
                print(f"{'Patron':<8} {'Entrada X':<16} {'yd':<6} {'a (neta)':<10} {'y':<6} {'Error e':<8} {'Accion de Actualizacion'}")
                print(f"{'-'*75}")

            # Evaluacion secuencial de cada patron del conjunto de datos
            for k in range(N):
                X_k = np.array(X_train[k], dtype=float)
                yd_k = int(y_train[k])

                # Propagacion y activacion
                a = self.propagacion(X_k)
                y = self.hardlims(a)
                e = yd_k - y

                accion = "Sin cambios (e = 0)"
                # Correccion sinaptica por Regla Delta si existe discrepancia
                if e != 0:
                    delta_W = e * X_k
                    self.W += delta_W
                    self.b += e
                    error_global += abs(e)
                    dw_str = [round(float(val), 2) for val in delta_W]
                    accion = f"Actualizacion: dW={dw_str}, db={e}"

                if verbose:
                    x_str = str([int(val) for val in X_k])
                    print(f"P{k+1:<7} {x_str:<16} {yd_k:<6} {round(a, 3):<10} {y:<6} {e:<8} {accion}")

            self.historial_error.append(error_global)

            if verbose:
                print(f"\n--> Fin de EPOCA {self.epocas_entrenadas} | Error Global Acumulado (E_global) = {error_global}")

            # Criterio de parada: convergencia alcanzada sin errores globales
            if error_global <= tolerancia:
                if verbose:
                    w_fin = [round(float(val), 4) for val in self.W]
                    print(f"\n{'*'*75}")
                    print(f"CONVERGENCIA ALCANZADA EN EPOCA {self.epocas_entrenadas}! Error Global = 0")
                    print(f"Pesos finales calibrados W* = {w_fin}, Sesgo final b* = {round(self.b, 4)}")
                    print(f"{'*'*75}\n")
                break

        return self.historial_error
