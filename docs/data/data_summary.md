# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos del dataset **RealWaste**, un conjunto de imágenes de residuos sólidos clasificados en 9 categorías.

## Resumen general de los datos

| Característica | Valor |
|---|---|
| Total de imágenes | 4 752 |
| Número de clases | 9 |
| Formato de imágenes | JPEG (`.jpg`) |
| Resolución | 524 × 524 píxeles |
| Canales de color | 3 (RGB) |
| Tamaño total del dataset | 656.42 MB |

Todas las imágenes presentan el **mismo formato y dimensiones**, lo que elimina la necesidad de redimensionamiento previo al entrenamiento. El dataset fue descargado automáticamente desde Kaggle mediante `kagglehub` y estructurado en un DataFrame con columnas `image_path` y `label`.

**Clases disponibles:**
Cardboard, Food Organics, Glass, Metal, Miscellaneous Trash, Paper, Plastic, Textile Trash, Vegetation.

## Resumen de calidad de los datos

| Aspecto | Resultado |
|---|---|
| Valores faltantes en `image_path` | 0 |
| Valores faltantes en `label` | 0 |
| Imágenes ilegibles o con formato no reconocido | 0 |
| Imágenes vacías (tamaño 0) | 0 |
| Imágenes constantes (píxeles idénticos) | 0 |
| Duplicados | No detectados |

El dataset se encuentra en **excelente estado de calidad**: no presenta valores nulos, archivos corruptos ni imágenes problemáticas. La consistencia en formato y resolución facilita el pipeline de preprocesamiento. No se requirieron acciones de limpieza estructural más allá del rebalanceo de clases.

## Variable objetivo

- **Nombre:** `label`
- **Tipo:** Categórica (clasificación multiclase)
- **Número de categorías:** 9

**Distribución de clases (dataset original):**

| Clase | N.º de imágenes |
|---|---|
| Plastic | > 700 |
| Metal | > 700 |
| Paper | < 700 |
| Miscellaneous Trash | < 700 |
| Cardboard | < 700 |
| Vegetation | < 700 |
| Glass | < 700 |
| Food Organics | < 700 |
| Textile Trash | < 700 (menor frecuencia) |

Existe un **desbalance de clases moderado**: Plastic y Metal superan las 700 imágenes, mientras que Textile Trash es la clase con menor representación. Se aplicó *data augmentation* dirigido para llevar las clases deficitarias a ~700 imágenes, generando 1 859 imágenes adicionales.

**Distribución de probabilidad de aumento por clase:**

| Clase | Probabilidad de aumento |
|---|---|
| Plastic | 0.00% |
| Metal | 0.00% |
| Paper | 10.76% |
| Miscellaneous Trash | 11.03% |
| Cardboard | 12.86% |
| Vegetation | 14.20% |
| Glass | 15.06% |
| Food Organics | 15.55% |
| Textile Trash | 20.55% |

## Variables individuales

El dataset de imágenes contiene dos metavariables tabulares:

| Variable | Tipo | Descripción |
|---|---|---|
| `image_path` | String (ruta de archivo) | Ruta absoluta a la imagen `.jpg` en disco |
| `label` | String categórico | Clase de residuo (una de las 9 categorías) |

Las imágenes en sí son tensores de forma `(524, 524, 3)` con valores de píxel en el rango [0, 255] (uint8). Para el entrenamiento se normalizan al rango [0, 1].

**Observaciones visuales relevantes:**
- Los residuos pueden aparecer sobre distintas superficies con colores similares.
- La iluminación es variable entre imágenes.
- Las fotos están tomadas desde un ángulo superior al objeto.
- El tamaño de los residuos es variable tanto entre categorías como dentro de ellas.
- Estas características son inherentes al contexto real de recolección en vertederos.

## Ranking de variables

Dado que el dataset es de imágenes (variables no tabulares), el ranking de importancia de características se realizará a nivel de píxeles/canales durante la etapa de modelado (p. ej., mediante mapas de activación o técnicas de interpretabilidad como Grad-CAM). No obstante, a nivel de metadatos:

- La variable `label` es la única variable predictora estructurada disponible para análisis estadístico clásico.
- La distribución de clases es el factor más relevante para el diseño del pipeline de entrenamiento, dado el desbalance identificado.

## Relación entre variables explicativas y variable objetivo

Al tratarse de un problema de **clasificación de imágenes**, la relación entre el input (píxeles) y la variable objetivo (`label`) se establece a través de la red neuronal convolucional. A nivel exploratorio:

- Cada clase presenta patrones visuales distintivos (textura, color, forma), aunque con considerable variabilidad intra-clase.
- La superposición visual entre algunas clases (p. ej., Paper vs. Cardboard, o Plastic vs. Miscellaneous Trash) anticipa que el modelo requerirá representaciones de alto nivel para discriminarlas.
- El desbalance de clases fue mitigado mediante *data augmentation* para evitar sesgos del modelo hacia las clases mayoritarias (Plastic y Metal).
- No se aplicó análisis de correlación clásica, ya que las variables de entrada son imágenes y no variables numéricas estructuradas.
