# ANÁLISIS Y DISCUSIÓN DE RESULTADOS

El desarrollo experimental, analítico y comparativo de los dos casos de estudio propuestos permite extraer hallazgos rigurosos en torno a la dinámica de aprendizaje, la geometría de decisión, la influencia del balance de clases y la sensibilidad a las condiciones iniciales:

### 1. Comparativa de la Velocidad de Convergencia y Dinámica del Error

Tanto el experimento del condicionamiento instrumental (Caso 1) como el clasificador diagnóstico de síntomas (Caso 2, desarrollo principal) lograron converger en un número reducido y coincidente de iteraciones: **3 épocas de entrenamiento**. Sin embargo, sus curvas de aprendizaje revelan comportamientos cualitativamente disímiles:

* **En el Caso 1 (La Paloma):** Se partió de un error inicial elevado ($E_{global} = 10$, correspondiente a 5 fallos sobre 8 patrones), provocado por una orientación inicial aleatoria diametralmente opuesta a la regla de recompensa. Una vez que las primeras actualizaciones por regla delta reorientaron el vector normal, el error descendió abruptamente ($10 \to 4 \to 0$).
* **En el Caso 2 (Diagnóstico Médico):** El error se mantuvo constante en las dos primeras épocas ($E = 4 \to E = 4$) antes de caer a cero en la Época 3. Este comportamiento refleja la búsqueda del compromiso geométrico: la red ajustó primero dos vértices limítrofes, pero al hacerlo descalibró temporalmente otros dos, necesitando una segunda pasada para encontrar una pendiente que satisficiera simultáneamente a los cuatro patrones de frontera.

### 2. El Rol Determinante del Sesgo (*Bias*) frente al Balance de Clases

La comparación entre los sesgos óptimos finales calibrados ($b^*$) constituye una de las mayores evidencias sobre el comportamiento adaptativo del Perceptrón Simple:

* **Caso 1 ($b^* = +6.2$):** Presenta una severa asimetría de clases (7 patrones positivos frente a solo 1 negativo). El algoritmo compensó este desbalance incrementando sustancialmente el sesgo, lo cual desplazó el hiperplano lejos del origen y elevó el estado basal de excitación. La red aprendió que, ante la duda o en ausencia de una inhibición conjunta extrema (el patrón $P_2$), la salida por defecto debe ser $+1$.
* **Caso 2 ($b^* = +0.1 \approx 0$):** Al tratarse de un problema perfectamente simétrico (4 pacientes sanos y 4 enfermos), el plano separador óptimo no requirió ningún desplazamiento forzado respecto al centro de gravedad del hipercubo. El sesgo resultante es prácticamente nulo, indicando que la frontera pasa casi por el origen $(0,0,0)$ y que la decisión depende enteramente de la suma algebraica de los síntomas.

### 3. Coherencia Semántica y Fisiológica de los Pesos Sinápticos Calibrados

Los vectores de pesos obtenidos no representan coeficientes matemáticos arbitrarios, sino que encapsulan el significado intrínseco de cada fenómeno:

* En el condicionamiento animal, $W_2^* = +5.1$ capturó la primacía del pulsador derecho sobre el izquierdo ($W_1^* = +2.3$), mientras que el signo negativo de $W_3^* = -2.4$ recompensó la acción de picar hacia la derecha ($x_3 = -1$), ya que $(-2.4)(-1) = +2.4 > 0$.
* En el diagnóstico médico, los tres pesos convergieron a valores positivos y de magnitudes sumamente homogéneas ($W_1^* = 3.6, W_2^* = 3.3, W_3^* = 4.3$). Esto refleja que ningún síntoma individual posee mayor jerarquía clínica que otro para definir la patología, validando analíticamente la regla de decisión basada en la mayoría simple ($\ge 2$ síntomas).

### 4. Eficacia Operativa del Espacio Bipolar $\{-1, +1\}$

El uso estricto del dominio bipolar junto a la función escalón simétrica `hardlims` fue el factor determinante para asegurar la rapidez del aprendizaje. En contraste con la representación unipolar $\{0, 1\}$ (donde las entradas nulas anulan el gradiente de actualización $\Delta W_j = e \cdot 0 = 0$ y congelan los pesos), en el espacio bipolar toda entrada no nula ($+1$ ó $-1$) imparte dirección y magnitud a la corrección sináptica en cada paso donde exista error.

### 5. Sensibilidad a las Condiciones Iniciales y Dependencia del Número de Épocas

La experimentación comparativa desarrollada en el Caso 2 (convergencia en 3, 2 y 1 épocas) aportó una conclusión metodológica fundamental: **el número de épocas no es una propiedad estática del conjunto de datos, sino que depende de la proximidad inicial del hiperplano respecto a la cuenca de atracción de soluciones válidas**:

* Cuando los pesos iniciales nacen desorientados (Experimento Principal, $W^{(0)} = [-0.4, -0.7, 0.3]^T$), el algoritmo requiere **3 épocas** para efectuar múltiples correcciones angulares.
* Con una inicialización simétrica que produce una corrección temprana favorable (Experimento 2, $W^{(0)} = [-0.9, -0.9, -0.9]^T, b^{(0)} = 0.9$), la primera actualización en $P_1$ basta para orientar correctamente el plano, alcanzando la convergencia en solo **2 épocas**.
* Finalmente, si los pesos iniciales coinciden analíticamente con una partición válida (Experimento 3, $W^{(0)} = [1, 1, 1]^T, b^{(0)} = 0$), el Perceptrón no experimenta ningún error en la primera pasada, convergiendo de forma inmediata en **1 época**. Esto demuestra que una inicialización adecuada puede acelerar drásticamente el proceso de entrenamiento sin alterar la matriz de patrones ni la regla delta.

---
---

# CONCLUSIONES

1. **Validez del Perceptrón Simple como Clasificador Lineal en $\mathbb{R}^3$:**  
   Se demostró formal y computacionalmente que tanto la conducta instrumental de la paloma como la inferencia diagnóstica por acumulación de síntomas son problemas **estrictamente linealmente separables**. Una arquitectura monocapa compuesta por una sola neurona artificial bipolar fue plenamente capaz de trazar hiperplanos separadores en $\mathbb{R}^3$, logrando una efectividad del $100\%$ ($8/8$ patrones correctos) con error residual nulo ($E_{global} = 0$).

2. **Convergencia y Robustez de la Regla Delta Bipolar:**  
   La regla de aprendizaje supervisada demostró una alta velocidad de adaptación, orientando el vector normal $\mathbf{W}$ y trasladando el sesgo $b$ desde parámetros de partida completamente aleatorios hasta el espacio de solución en un número reducido de iteraciones, confirmando en la práctica el Teorema de Convergencia del Perceptrón formulado por Rosenblatt.

3. **Influencia Crítica del Sesgo (*Bias*) según la Distribución de Clases:**  
   El sesgo evidenció su papel como grado de libertad imprescindible para el ajuste geométrico del modelo: ante distribuciones asimétricas (Caso 1, proporción 7:1) adoptó un valor fuertemente positivo ($b^* = 6.2$) para desplazar la frontera y elevar el umbral basal de disparo; mientras que ante distribuciones simétricas balanceadas (Caso 2, proporción 4:4) se situó en valores prácticamente nulos ($b^* = 0.1$), ubicando la frontera en proximidad directa al origen de coordenadas.

4. **Sensibilidad de la Velocidad de Convergencia a las Condiciones Iniciales:**  
   El estudio comparativo realizado en el Caso 2 evidenció que la cantidad de épocas requeridas (variando entre 1, 2 y 3 épocas) está fuertemente supeditada a la orientación geométrica de partida de $\mathbf{W}^{(0)}$ y $b^{(0)}$. Aunque la convergencia hacia error cero está teóricamente garantizada para problemas separables, la elección o cercanía de los pesos iniciales respecto a la región de separación modula drásticamente el tiempo de cómputo y el número de ajustes necesarios.

5. **Significado Fisiológico y Semántico de los Pesos Sinápticos:**  
   Los parámetros finales aprendidos por el Perceptrón guardan una estricta coherencia con la naturaleza de los problemas reales modelados: ponderan cuantitativamente la relevancia de los estímulos ambientales en la toma de decisiones animal y reflejan la equivalencia patológica de los síntomas en la detección clínica de enfermedad.

6. **Alcance y Limitaciones Teóricas del Modelo Monocapa:**  
   Si bien el Perceptrón Simple bipolar resolvió exitosamente ambos casos de estudio tridimensionales, su capacidad de generalización está estrictamente limitada a funciones linealmente separables. Para conjuntos de datos con fronteras complejas, disyunciones exclusivas (XOR) o regiones no lineales, se hace indispensable la transición hacia Perceptrones Multicapa (MLP) dotados de capas ocultas, funciones de activación continuas diferenciables y entrenamiento por retropropagación del error (*backpropagation*).
