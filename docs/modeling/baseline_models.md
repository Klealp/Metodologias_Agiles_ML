# Reporte del Modelo Baseline

Este documento contiene los resultados del modelo baseline para el proyecto de clasificación de residuos sólidos utilizando el dataset **RealWaste**.

## Descripción del modelo

El modelo baseline es una **red neuronal convolucional (CNN) diseñada desde cero**, construida con la API Funcional de Keras. Su propósito es establecer una línea de referencia del rendimiento antes de aplicar técnicas más avanzadas como Transfer Learning o Fine-Tuning.

### Arquitectura

| Componente | Detalle |
|---|---|
| Entrada | Imágenes RGB de 224 × 224 píxeles |
| Bloques convolucionales | 3 bloques, filtros: (32, 64, 128) |
| Convoluciones por bloque | 2 capas Conv2D (kernel 3×3, padding='same') |
| Normalización | Batch Normalization tras cada convolución |
| Reducción espacial | MaxPooling2D (2×2) por bloque |
| Pooling global | GlobalAveragePooling2D |
| Capas densas | Dense(512) → Dropout(0.2) → Dense(256) → Dropout(0.2) |
| Capa de salida | Dense(9, activación softmax) |
| Aumentación de datos | RandomFlip (horizontal), RandomRotation(0.15), RandomZoom(0.2) |
| Optimizador | Adam (lr = 0.001) |
| Función de pérdida | Categorical Crossentropy |
| Total de parámetros | 488,489 |

### Hiperparámetros seleccionados

Los hiperparámetros finales se obtuvieron mediante una búsqueda en cuadrícula (Grid Search) realizada en una etapa preliminar del proyecto:

| Hiperparámetro | Valor |
|---|---|
| `filters` | (32, 64, 128) |
| `dense_units` | (512, 256) |
| `dropout_rate` | 0.2 |
| `learning_rate` | 0.001 |

### Estrategia de entrenamiento

Para la evaluación del modelo base se fusionaron los conjuntos de entrenamiento y validación originales, reservando un 10 % para monitoreo durante el entrenamiento. Esto le proporciona al modelo la mayor cantidad de datos posible una vez confirmado el conjunto óptimo de hiperparámetros.

| Conjunto | Imágenes |
|---|---|
| Entrenamiento (90 %) | ~3,594 |
| Validación (10 %) | ~400 |
| Prueba (fijo, 15 %) | 713 |

- **Early Stopping**: `patience=15`, monitoreando `val_accuracy`.
- **Épocas máximas**: 50.
- **Pesos de clase**: Se aplicaron pesos balanceados para compensar el desbalance entre clases.

## Variables de entrada

Cada muestra de entrada es una imagen RGB redimensionada a **224 × 224 píxeles** y normalizada al rango [0, 1]. Los datos provienen del dataset **RealWaste**, que contiene residuos sólidos urbanos fotografiados en condiciones reales.

| Característica | Descripción |
|---|---|
| Tipo | Imagen RGB (JPEG) |
| Dimensiones | 224 × 224 × 3 |
| Normalización | División por 255.0 |
| Total de imágenes | 4,752 |
| Partición (train/val/test) | 70 % / 15 % / 15 % (estratificada por clase) |

## Variable objetivo

La variable objetivo es la **categoría de residuo** a la que pertenece cada imagen. El problema es de **clasificación multiclase** con 9 categorías:

| Índice | Clase | Muestras (test) | Peso de clase |
|---|---|---|---|
| 0 | Cardboard | 69 | 1.1441 |
| 1 | Food Organics | 62 | 1.2832 |
| 2 | Glass | 63 | 1.2570 |
| 3 | Metal | 118 | 0.6683 |
| 4 | Miscellaneous Trash | 75 | 1.0681 |
| 5 | Paper | 75 | 1.0559 |
| 6 | Plastic | 138 | 0.5730 |
| 7 | Textile Trash | 48 | 1.6647 |
| 8 | Vegetation | 65 | 1.2117 |

## Evaluación del modelo

### Métricas de evaluación

Se emplearon las siguientes métricas sobre el **conjunto de prueba (713 imágenes)**:

- **Accuracy** – proporción global de predicciones correctas.
- **Precision** – fracción de predicciones positivas que son verdaderamente positivas (por clase).
- **Recall** – fracción de muestras reales de una clase que el modelo identificó correctamente.
- **F1-score** – media armónica de precision y recall; útil ante desbalance de clases.
- **Macro avg** – promedio no ponderado de las métricas por clase.
- **Weighted avg** – promedio ponderado por la cantidad de muestras por clase.

### Resultados de evaluación

**Accuracy global en test: 0.6942 (69.42 %)**

| Clase | Precision | Recall | F1-score | Support |
|---|---|---|---|---|
| Cardboard | 0.6250 | 0.7971 | 0.7006 | 69 |
| Food Organics | 0.8864 | 0.6290 | 0.7358 | 62 |
| Glass | 0.7812 | 0.7937 | 0.7874 | 63 |
| Metal | 0.7596 | 0.6695 | 0.7117 | 118 |
| Miscellaneous Trash | 0.5208 | 0.3333 | 0.4065 | 75 |
| Paper | 0.8103 | 0.6267 | 0.7068 | 75 |
| Plastic | 0.6581 | 0.7391 | 0.6962 | 138 |
| Textile Trash | 0.4930 | 0.7292 | 0.5882 | 48 |
| Vegetation | 0.7778 | 0.9692 | 0.8630 | 65 |
| **macro avg** | **0.7014** | **0.6985** | **0.6885** | 713 |
| **weighted avg** | **0.7038** | **0.6942** | **0.6893** | 713 |

## Análisis de los resultados

### Fortalezas

- **Vegetation** es la clase con mejor desempeño (F1 = 0.8630), beneficiada por patrones visuales distintivos (color y textura).
- **Glass** muestra un comportamiento equilibrado entre precision y recall (F1 = 0.7874).
- La aumentación de datos y los pesos de clase contribuyen a mitigar parcialmente el desbalance del dataset.
- El modelo es ligero (488,489 parámetros), lo que facilita su entrenamiento sin hardware especializado.

### Debilidades

- **Miscellaneous Trash** presenta el peor F1-score (0.4065) con un recall muy bajo (0.3333): el modelo no logra distinguir esta clase de las demás con suficiente consistencia, debido a que es una mezcla heterogénea de materiales.
- **Textile Trash** también tiene un F1 bajo (0.5882), reflejando dificultades para aprender representaciones visuales específicas con pocos ejemplos (48 muestras en test).
- La accuracy global de **64.66 %** es insuficiente para un escenario productivo de clasificación de residuos donde los errores tienen consecuencias operativas directas.
- Una CNN entrenada desde cero con un dataset de 4,752 imágenes carece del conocimiento visual previo que puede aportar una red preentrenada en ImageNet (millones de imágenes).

## Conclusión

El modelo baseline CNN alcanza una accuracy de **64.66 %** en el conjunto de prueba, lo que representa una línea base funcional pero claramente mejorable.

La comparación exhaustiva del modelo de línea base contra modelos más avanzados (Transfer Learning y Fine-Tuning) se realiza en el reporte `model_report.md`, donde se evidencia una mejora significativa al aprovechar arquitecturas preentrenadas como InceptionV3.

## Referencias

- Single, S., Iranmanesh, S., & Raad, R. (2023). RealWaste: A Novel Real-Life Data Set for Landfill Waste Classification Using Deep Learning. Algorithms, 16(6), 299. https://doi.org/10.3390/info14120633
- Beach, J. (2023). RealWaste Dataset. Kaggle. Recuperado de https://www.kaggle.com/datasets/joebeachcapital/realwaste