# UNIVERSIDAD DE CARTAGENA
### FACULTAD DE INGENIERÍA — PROGRAMA DE INGENIERÍA DE SISTEMAS

---

## IMPLEMENTACIÓN Y ENTRENAMIENTO DEL PERCEPTRÓN SIMPLE BIPOLAR EN PROBLEMAS DE CLASIFICACIÓN LINEAL: SIMULACIÓN DE CONDICIONAMIENTO INSTRUMENTAL Y DIAGNÓSTICO MÉDICO

**Presentado por:**  
* Dago David Palmera Navarro — Código: 0222321003  
* Julián David Camargo Padilla — Código: 0222320016  

**Docente:**  
Manuel Alejandro Ospina Alarcón  

**Asignatura:** Inteligencia Artificial  
**Semestre:** VII  
**Lugar y Fecha:** Cartagena de Indias, Septiembre de 2026  

---

## TABLA DE CONTENIDO

1. [INTRODUCCIÓN](#introducción)
2. [OBJETIVOS](#objetivos)
   * [Objetivo General](#objetivo-general)
   * [Objetivos Específicos](#objetivos-específicos)
3. [FUNDAMENTACIÓN TEÓRICA](#fundamentación-teórica)
   * [Antecedentes e Inspiración Biológica de la Neurona Artificial](#antecedentes-e-inspiración-biológica-de-la-neurona-artificial)
   * [Aprendizaje Hebbiano y Plasticidad Sináptica](#aprendizaje-hebbiano-y-plasticidad-sináptica)
   * [El Perceptrón Simple de Rosenblatt](#el-perceptrón-simple-de-rosenblatt)
   * [Geometría de la Decisión y Separabilidad Lineal](#geometría-de-la-decisión-y-separabilidad-lineal)
   * [Justificación Técnica del Dominio Bipolar frente al Unipolar](#justificación-técnica-del-dominio-bipolar-frente-al-unipolar)
   * [Algoritmo de Aprendizaje Supervisado y Regla Delta](#algoritmo-de-aprendizaje-supervisado-y-regla-delta)
4. [DESARROLLO DE LA ACTIVIDAD – CASO DE ESTUDIO 1: CONDICIONAMIENTO DE LA PALOMA](#desarrollo-de-la-actividad--caso-de-estudio-1-condicionamiento-de-la-paloma) *(Ver archivo anexo)*
5. [DESARROLLO DE LA ACTIVIDAD – CASO DE ESTUDIO 2: DIAGNÓSTICO MÉDICO POR SÍNTOMAS](#desarrollo-de-la-actividad--caso-de-estudio-2-diagnóstico-médico-por-síntomas) *(Ver archivo anexo)*
6. [ANÁLISIS Y DISCUSIÓN DE RESULTADOS](#análisis-y-discusión-de-resultados) *(Ver archivo anexo)*
7. [CONCLUSIONES](#conclusiones) *(Ver archivo anexo)*

---

## INTRODUCCIÓN

En el campo de la Inteligencia Artificial y el aprendizaje automático, las Redes Neuronales Artificiales (RNA) constituyen uno de los paradigmas más representativos de la computación bioinspirada, orientados al reconocimiento de patrones, la aproximación funcional y la toma autónoma de decisiones. Entre los modelos fundacionales destaca el Perceptrón Simple (PS), propuesto por Frank Rosenblatt en 1958, el cual formaliza una arquitectura monocapa capaz de ajustar adaptativamente sus parámetros sinápticos mediante un esquema de aprendizaje supervisado.

La capacidad operativa del Perceptrón Simple radica en su habilidad para establecer fronteras lineales de clasificación —representadas geométricamente como hiperplanos de decisión— que dividen el espacio de estados en regiones disjuntas. En este contexto, el uso de representaciones estrictamente bipolares $\{-1, +1\}$ y funciones de activación escalón simétricas (`hardlims`) aporta una ventaja matemática sustancial sobre esquemas binarios convencionales, garantizando que cada componente del vector de entrada contribuya activamente a la corrección del error sin inducir estancamientos durante la actualización por regla delta.

El presente informe consolida el diseño, entrenamiento y simulación computacional del Perceptrón Simple aplicado a dos casos de estudio con entradas tridimensionales: en primer lugar, la modelación de un experimento biológico de condicionamiento instrumental operante en una paloma; y en segundo lugar, un clasificador de diagnóstico médico preliminar basado en la concurrencia de sintomatologías clínicas. A lo largo del documento se detallan las tablas de patrones, la dinámica de calibración de pesos y sesgos, la reducción del error global a lo largo de las épocas y la visualización tridimensional del plano de separación lineal resultante.

---

## OBJETIVOS

### Objetivo General
Diseñar, implementar y evaluar un modelo de red neuronal artificial del tipo Perceptrón Simple (PS) operando en el dominio bipolar simétrico $\{-1, +1\}$, con el fin de resolver problemas de clasificación binaria linealmente separables a través de la simulación de toma de decisiones en condicionamiento instrumental y diagnóstico médico por patrones clínicos.

### Objetivos Específicos
1. Analizar los fundamentos matemáticos, biológicos y geométricos que rigen la operación de la neurona artificial y el hiperplano delimitador de clases en espacios vectoriales $\mathbb{R}^n$.
2. Formular y parametrizar las tablas de verdad y matrices de entrenamiento bajo representación bipolar $\{-1, +1\}$ para los casos de condicionamiento de la paloma y diagnóstico de sintomatología clínica.
3. Aplicar el algoritmo de entrenamiento supervisado mediante la regla delta y la función de activación bipolar `hardlims`, examinando la dinámica de corrección de pesos sinápticos ($\mathbf{W}$) y sesgo ($b$) época a época.
4. Evaluar la curva de convergencia del error global del sistema hasta alcanzar el estado de cero errores ($E_{global} = 0$), contrastando la sensibilidad del algoritmo frente a las condiciones iniciales asignadas.
5. Representar geométricamente en tres dimensiones el hiperplano de separación obtenido, verificando la partición del espacio vectorial y la correcta clasificación de los ocho estados posibles para cada caso de estudio.

---

## FUNDAMENTACIÓN TEÓRICA

### Antecedentes e Inspiración Biológica de la Neurona Artificial
Las Redes Neuronales Artificiales (RNA) surgen como una abstracción bioinspirada de los mecanismos de procesamiento de información del cerebro humano. En el sistema nervioso biológico, la neurona constituye la unidad elemental de cómputo; esta recibe impulsos electroquímicos a través de un árbol de ramificaciones denominado dendritas, acumula la diferencia de potencial dentro del cuerpo celular (soma) y, cuando la estimulación sobrepasa cierto umbral crítico de despolarización, dispara un potencial de acción que se propaga a lo largo del axón hacia otras células mediante conexiones especializadas llamadas sinapsis.

En 1943, Warren McCulloch y Walter Pitts desarrollaron el primer modelo matemático formal de una neurona. En dicha propuesta, demostraron que una unidad de umbral binario podía computar funciones lógicas fundamentales (como AND, OR y NOT). No obstante, tanto el modelo de conexión como el umbral debían establecerse de forma manual y estática, impidiendo que la neurona aprendiera a partir de la experiencia empírica.

### Aprendizaje Hebbiano y Plasticidad Sináptica
La base teórica que explica cómo un sistema neuronal modifica físicamente sus enlaces fue postulada por Donald Hebb en 1949 a través de la conocida Ley de Hebb (*Hebbian Learning*). Hebb planteó que cuando el axón de una neurona A se encuentra lo suficientemente cerca de una neurona B para excitarla y participa repetidamente en su disparo, ocurre un proceso de crecimiento o cambio metabólico en una o ambas células que incrementa la fuerza sináptica entre ellas.

Este principio, sintetizado modernamente bajo el aforismo *“cells that fire together, wire together”*, introdujo formalmente el concepto de peso variable como parámetro dinámico de memoria: aprender no consiste en almacenar datos en una dirección fija de memoria, sino en ajustar, reforzar o atenuar la conductancia o influencia mutua entre nodos interconectados.

### El Perceptrón Simple de Rosenblatt
En 1958, Frank Rosenblatt integró la concepción de la neurona formal con el principio de plasticidad de Hebb, dando origen al Perceptrón Simple (PS). A diferencia de sus predecesores, Rosenblatt dotó al modelo de una regla algorítmica de convergencia capaz de ajustar iterativamente los parámetros del sistema mediante supervisión externa, convirtiéndose en el primer modelo de red neuronal capaz de aprender a clasificar patrones de forma autónoma.

#### Anatomía Matemática del Perceptrón:
* **Vector de entrada ($\mathbf{X}$):** Representa las características observables del patrón presentado al sistema en un espacio $\mathbb{R}^n$:
  $$\mathbf{X} = [x_1, x_2, \dots, x_n]^T$$
* **Vector de Pesos Sinápticos ($\mathbf{W}$):** Modela la intensidad de cada enlace sináptico: $\mathbf{W} = [W_1, W_2, \dots, W_n]^T$. Un peso positivo ($W_j > 0$) denota una conexión excitatoria, mientras que un peso negativo ($W_j < 0$) ejerce un efecto inhibitorio sobre el disparo.
* **Sesgo o Umbral ($b$):** Parámetro escalar independiente que confiere un grado de libertad adicional de decisión a la red: $b \in \mathbb{R}$. Permite trasladar espacialmente la función de decisión respecto al origen de coordenadas, asegurando que la neurona pueda producir respuestas arbitrarias incluso cuando todas las componentes de entrada son nulas ($\mathbf{X} = \mathbf{0}$).
* **Combinación Lineal (Salida Neta, $a$):** Agrega las entradas ponderadas junto con el término de sesgo:
  $$a = \mathbf{W}^T \mathbf{X} + b = \sum_{j=1}^{n} W_j x_j + b$$
* **Función de Activación ($f$):** Mapea la suma neta escalar $a$ al espacio de decisión de salida $y \in \{-1, +1\}$.

### Geometría de la Decisión y Separabilidad Lineal
El Perceptrón Simple opera como un discriminador lineal que particiona el espacio de estados $\mathbb{R}^n$ en dos semiespacios disjuntos. La frontera geométrica donde se produce la transición de estado (cambio de clase) corresponde al lugar donde la excitación neta se anula:

$$\mathbf{W}^T \mathbf{X} + b = 0$$

Para un espacio tridimensional $\mathbb{R}^3$, como el abordado en los casos prácticos de este estudio con entradas $(x_1, x_2, x_3)$, dicha frontera conforma un hiperplano de decisión bidimensional definido analíticamente por:

$$W_1 x_1 + W_2 x_2 + W_3 x_3 + b = 0$$

* El vector de pesos $\mathbf{W} = [W_1, W_2, W_3]^T$ actúa como el **vector normal ortogonal** que define la orientación del plano.
* La magnitud y signo del sesgo $b$ determinan el desplazamiento euclidiano perpendicular del plano respecto al origen:
  $$d = \frac{|b|}{\|\mathbf{W}\|}$$
* Un conjunto de datos se denomina **linealmente separable** si existe al menos un hiperplano capaz de aislar a todos los puntos de la clase positiva ($y_d = +1$) en uno de sus semiespacios ($a \ge 0$), y a todos los puntos de la clase negativa ($y_d = -1$) en el semiespacio opuesto ($a < 0$).

### Justificación Técnica del Dominio Bipolar frente al Unipolar
En el modelado del Perceptrón Simple resulta crítico distinguir entre dos dominios de representación discreta:
* **Dominio Unipolar $\{0, 1\}$:** Utiliza la función escalón clásica:
  $$f(a) = \text{hardlim}(a) = \begin{cases} 1 & \text{si } a \ge 0 \\ 0 & \text{si } a < 0 \end{cases}$$
* **Dominio Bipolar $\{-1, +1\}$:** Utiliza la función escalón simétrica:
  $$f(a) = \text{hardlims}(a) = \begin{cases} +1 & \text{si } a \ge 0 \\ -1 & \text{si } a < 0 \end{cases}$$

#### Fundamento de la Selección Bipolar:
En esquemas unipolares $\{0, 1\}$, cuando una variable de entrada adopta el valor de inactividad ($x_j = 0$), el producto que gobierna el término de corrección en la regla de aprendizaje delta se extingue idénticamente:

$$\Delta W_j = e \cdot x_j = e \cdot 0 = 0$$

Bajo esta condición, el peso sináptico $W_j$ queda completamente congelado durante esa iteración, independientemente de que la neurona haya emitido una respuesta errónea.

Por el contrario, bajo la convención estrictamente bipolar $\{-1, +1\}$, toda variable de entrada aporta de manera permanente un valor no nulo con signo específico ($x_j \in \{-1, +1\}$). Esto garantiza que todas las componentes del vector de pesos se actualicen de manera solidaria en cada paso de aprendizaje donde exista error:

$$\Delta W_j = e \cdot (\pm 1) \ne 0$$

Esto orienta activamente el vector normal $\mathbf{W}$ y evita estancamientos numéricos, lo cual incrementa notablemente la tasa de convergencia del sistema.

### Algoritmo de Aprendizaje Supervisado y Regla Delta
El entrenamiento del Perceptrón Simple se rige por un esquema supervisado basado en pares ordenados $(\mathbf{X}_k, y_{d,k})$, donde $\mathbf{X}_k$ es el vector del patrón $k$ y $y_{d,k} \in \{-1, +1\}$ representa la salida deseada (*target*).

#### Dinámica de Corrección de Errores:
El error de clasificación individual se calcula como la discrepancia algebraica directa entre el valor objetivo y la respuesta emitida por la neurona:

$$e_k = y_{d,k} - y_k$$

En la representación bipolar simétrica con función `hardlims`, surgen exclusivamente tres escenarios discretos posibles para $e_k$:

| Salida Deseada ($y_d$) | Salida Obtenida ($y$) | Error ($e = y_d - y$) | Interpretación y Acción del Algoritmo |
| :---: | :---: | :---: | :---|
| $+1$ | $+1$ | **$0$** | **Clasificación Correcta:** No se alteran los pesos ni el sesgo ($\Delta\mathbf{W} = \mathbf{0}, \Delta b = 0$). |
| $-1$ | $-1$ | **$0$** | **Clasificación Correcta:** No se alteran los pesos ni el sesgo ($\Delta\mathbf{W} = \mathbf{0}, \Delta b = 0$). |
| $+1$ | $-1$ | **$+2$** | **Falso Negativo (falta de excitación):** La neurona debió disparar pero no superó el umbral. Se aplica: $\mathbf{W}^{(nuevo)} = \mathbf{W} + 2\mathbf{X}_k$, $b^{(nuevo)} = b + 2$. *Efecto geométrico:* Rota el vector de pesos sumándole $2\mathbf{X}_k$, acercando el hiperplano hacia la región del patrón. |
| $-1$ | $+1$ | **$-2$** | **Falso Positivo (exceso de excitación):** La neurona disparó indebidamente. Se aplica: $\mathbf{W}^{(nuevo)} = \mathbf{W} - 2\mathbf{X}_k$, $b^{(nuevo)} = b - 2$. *Efecto geométrico:* Rota el vector de pesos restándole $2\mathbf{X}_k$, alejando el hiperplano del patrón infractor. |

#### Criterio de Parada y Teorema de Rosenblatt:
En cada época completa se cuantifica el error global acumulado:

$$E_{global} = \sum_{k=1}^{N} |e_k|$$

El entrenamiento finaliza exitosamente cuando $E_{global} = 0$. Según el **Teorema de Convergencia del Perceptrón** formulado por Frank Rosenblatt, si un conjunto de patrones es linealmente separable, el algoritmo de aprendizaje garantiza converger hacia una solución separadora en un número finito de épocas, independientemente de la elección de los pesos iniciales.
