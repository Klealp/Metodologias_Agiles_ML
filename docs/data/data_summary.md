# Reporte de Datos

Este documento contiene los resultados del análisis exploratorio de datos del dataset **RealWaste**, un conjunto de imágenes de residuos sólidos clasificados en 9 categorías.

## Resumen general de los datos

| Característica | Valor |
|---|---|+
| Total de imágenes | 4 752 |
| Número de clases | 9 |
| Formato de imágenes | JPEG (`.jpg`) |
| Resolución original | 524 × 524 píxeles |
| Resolución para entrenamiento (InceptionV3) | **299 × 299 píxeles** |
| Canales de color | 3 (RGB) |
| Tamaño total del dataset original | 656.42 MB |
| Tamaño total del dataset redimensionado | 200.89 MB |

Todas las imágenes originales presentan el **mismo formato y dimensiones** (524×524 px). Para el entrenamiento con **InceptionV3**, la totalidad del dataset aumentado es redimensionada a **299×299 píxeles** mediante interpolación Lanczos y almacenada en `realwaste_mod/`. El dataset fue descargado automáticamente desde Kaggle mediante `kagglehub` y estructurado en un DataFrame con columnas `image_path` y `label`.

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

Existe un **desbalance de clases moderado**: Plastic y Metal superan las 700 imágenes, mientras que Textile Trash es la clase con menor representación. Se ilustro como se puede aplicar *data augmentation* dirigido para llevar las clases deficitarias a ~700 imágenes.

## Variables individuales

El dataset de imágenes contiene dos variables tabulares:

| Variable | Tipo | Descripción |
|---|---|---|
| `image_path` | String (ruta de archivo) | Ruta absoluta a la imagen `.jpg` en disco |
| `label` | String categórico | Clase de residuo (una de las 9 categorías) |

Las imágenes en sí son tensores de forma `(524, 524, 3)` (originales) o `(299, 299, 3)` (redimensionadas para InceptionV3) con valores de píxel en el rango [0, 255] (uint8). Para el entrenamiento se normalizan al rango [0, 1].

**Observaciones visuales relevantes:**
- La iluminación es variable entre imágenes.
- Las fotos están tomadas desde un ángulo superior al objeto.
- El tamaño de los residuos es variable tanto entre categorías como dentro de ellas.
- Estas características son inherentes al contexto real de recolección en vertederos.

## Relación entre variables explicativas y variable objetivo

Al tratarse de un problema de **clasificación de imágenes**, la relación entre el input (píxeles) y la variable objetivo (`label`) se establece a través de la red neuronal convolucional. A nivel exploratorio:

- Cada clase presenta patrones visuales distintivos (textura, color, forma), aunque con considerable variabilidad intra-clase.
- El desbalance de clases se puede mitigar mediante *data augmentation* para evitar sesgos del modelo hacia las clases mayoritarias (Plastic y Metal).
- No se aplicó análisis de correlación clásica, ya que las variables de entrada son imágenes y no variables numéricas estructuradas.
