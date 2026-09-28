# -*- coding: utf-8 -*-
"""
Módulo del Perceptrón Simple Bipolar (PS)
Implementa la arquitectura monocapa con función de activación hardlims
y la regla de aprendizaje delta supervisado en dominio {-1, +1}.
"""

import numpy as np

class PerceptronSimpleBipolar:
    def __init__(self, n_entradas=3, pesos_iniciales=None, sesgo_inicial=None):
        self.n_entradas = n_entradas
        if pesos_iniciales is not None:
            self.W = np.array(pesos_iniciales, dtype=float)
        else:
            self.W = np.round(np.random.uniform(-1.0, 1.0, size=n_entradas), 2)
            
        if sesgo_inicial is not None:
            self.b = float(sesgo_inicial)
        else:
            self.b = float(np.round(np.random.uniform(0.0, 1.0), 2))
            
        self.historial_error = []
        self.epocas_entrenadas = 0

    @staticmethod
    def hardlims(a):
        return 1 if a >= 0 else -1

    def propagacion(self, X):
        return float(np.dot(self.W, X) + self.b)

    def predecir(self, X):
        a = self.propagacion(X)
        return self.hardlims(a)

    def entrenar(self, X_train, y_train, epocas_max=100, tolerancia=0, verbose=True):
        N = len(y_train)
        self.historial_error = []
        self.epocas_entrenadas = 0

        while self.epocas_entrenadas < epocas_max:
            self.epocas_entrenadas += 1
            error_global = 0

            if verbose:
                w_str = [round(float(val), 4) for val in self.W]
                print(f"\n{'='*75}")
                print(f"EPOCA {self.epocas_entrenadas} | Estado inicial: W={w_str}, b={round(self.b, 4)}")
                print(f"{'='*75}")
                print(f"{'Patron':<8} {'Entrada X':<16} {'yd':<6} {'a (neta)':<10} {'y':<6} {'Error e':<8} {'Accion de Actualizacion'}")
                print(f"{'-'*75}")

            for k in range(N):
                X_k = np.array(X_train[k], dtype=float)
                yd_k = int(y_train[k])
                
                a = self.propagacion(X_k)
                y = self.hardlims(a)
                e = yd_k - y

                accion = "Sin cambios (e = 0)"
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

            if error_global <= tolerancia:
                if verbose:
                    w_fin = [round(float(val), 4) for val in self.W]
                    print(f"\n{'*'*75}")
                    print(f"CONVERGENCIA ALCANZADA EN EPOCA {self.epocas_entrenadas}! Error Global = 0")
                    print(f"Pesos finales calibrados W* = {w_fin}, Sesgo final b* = {round(self.b, 4)}")
                    print(f"{'*'*75}\n")
                break

        return self.historial_error
