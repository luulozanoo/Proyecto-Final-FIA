# Proyecto-Final-FIA

# 🏰 Misión Camboya: Recuperación del Coronel Kurtz

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![numpy](https://img.shields.io/badge/numpy-Data-013243.svg?logo=numpy)](https://numpy.org/)
[![matplotlib](https://img.shields.io/badge/matplotlib-Plots-11557c.svg)](https://matplotlib.org/)

> **Tres desafíos. Un coronel perdido. Una misión imposible.**
>
> Proyecto final de Fundamentos de la Inteligencia Artificial implementado en Python, donde el Capitán Willard debe rescatar al Coronel Kurtz atravesando un palacio peligroso, un templo laberíntico y un río con corrientes impredecibles. Cada desafío pone a prueba un paradigma distinto de IA: búsqueda lógica, inferencia probabilística y procesos de decisión de Markov.

---

## 🗺️ Estructura del proyecto

```
📁 proyecto/
├── kurtz.py          # Punto de entrada principal — menú y orquestación
├── parte1.py         # Palacio Peligroso — Búsqueda lógica (BFS)
├── parte2.py         # Templo Tenebroso — Inferencia bayesiana (A*)
├── parte2MDP.py      # Río Nebuloso — Proceso de Decisión de Markov
└── requirements.txt  # Dependencias del proyecto
```

---

## 🧩 Los tres desafíos

### 🏰 Parte 1 — Palacio Peligroso (Búsqueda Lógica)

Un tablero 6×6 con precipicios, un soldado, una salida y el Coronel Kurtz ocultos aleatoriamente. El agente percibe estímulos en celdas adyacentes (brisa, ronquido, resplandor) y razona para navegar de forma segura.

- **Modo guiado:** el usuario toma las decisiones apoyándose en las deducciones del sistema
- **Agente BFS:** búsqueda en anchura con cola FIFO para encontrar el camino más corto a través de celdas seguras

### 🏦 Parte 2 — Templo Tenebroso (Inferencia Bayesiana)

Laberinto con múltiples trampas por celda (fuego, pinchos, dardos) y un soldado. El agente aplica la regla de Bayes actualizando probabilidades posteriores en cada movimiento mediante mapas de calor.

- **Modo guiado:** visualización de mapas de calor y recomendaciones de celdas seguras en tiempo real
- **Agente A\*:** búsqueda heurística (distancia Manhattan) que minimiza el riesgo acumulado

### ⛵ Parte 3 — Río Nebuloso (MDP)

Cruzar un río con corrientes aleatorias e islas peligrosas modelado como Proceso de Decisión de Markov. Se obtiene la política óptima mediante el algoritmo Value Iteration con la ecuación de Bellman.

- **3 escenarios** con distintos valores de gamma y semilla para ilustrar el impacto de los parámetros
- Visualización del mapa de utilidad y política óptima en cada iteración

---

## ⚙️ Cómo ejecutar el proyecto en local

1. **Clona el repositorio:**

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

2. **Crea y activa un entorno virtual (recomendado):**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Lanza la aplicación:**

```bash
python kurtz.py
```

El menú interactivo te guiará por los tres desafíos. Pulsa `Z` en cualquier momento para saltar al siguiente.

---

## 🛠️ Tecnologías y Requisitos

Proyecto desarrollado puramente en Python. Las dependencias necesarias son:

```text
numpy
matplotlib
seaborn
```

---

## 📬 Contacto

Proyecto desarrollado como trabajo final de la asignatura **Fundamentos de la Inteligencia Artificial**.

* 👤 **Autora:** Lucía Lozano Isac
* 🎓 **Universidad:** Madrid, enero 2026

---

> *"No estaba aquí para rescatar al Coronel Kurtz. Estaba aquí para poner a prueba cuánta IA cabía en una selva."*
