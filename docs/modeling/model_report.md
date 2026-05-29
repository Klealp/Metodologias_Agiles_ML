# Reporte del Modelo Final

## Resumen Ejecutivo

Se desarrollaron y compararon tres modelos de clasificación de imágenes de residuos sólidos sobre el dataset **RealWaste** (4.752 imágenes, 9 clases):

| Modelo | Accuracy (test) | Parámetros | Peso en disco |
|---|---|---|---|
| Baseline CNN (desde cero) | 64.66 % | 0.49 M | 5.7 MB |
| Transfer Learning (InceptionV3) | 92.01 % | 22.33 M | 90.3 MB |
| **Fine-Tuning (InceptionV3)** | **96.91 %** | **22.33 M** | **145.8 MB** |

El modelo final seleccionado para producción es el **Fine-Tuning de InceptionV3**, que supera con amplitud el criterio de éxito del proyecto (accuracy > 75 %, F1-score ponderado > 0.75) y representa una mejora de más de 32 puntos porcentuales respecto a la línea base. Este modelo fue posteriormente reentrenado con la totalidad de los datos disponibles (`realwaste_mod`) y guardado como `model_prd.keras`.

## Descripción del Problema

La clasificación manual de residuos sólidos en vertederos es una actividad costosa, lenta y con riesgos de exposición a materiales peligrosos para los trabajadores. La instalación *Whyte's Gully Waste and Resource Recovery Centre* en Wollongong, Australia, es el contexto real del que provienen las imágenes del dataset RealWaste (Single et al., 2023).

El objetivo es automatizar la identificación de 9 categorías de residuos —*Cardboard*, *Food Organics*, *Glass*, *Metal*, *Miscellaneous Trash*, *Paper*, *Plastic*, *Textile Trash* y *Vegetation*— a partir de imágenes JPG de 524 × 524 píxeles capturadas en condiciones reales de vertedero, caracterizadas por variabilidad de iluminación, oclusiones y fondos complejos.

El criterio de éxito definido en el *Project Charter* establece una **accuracy global superior al 75 %** y un **F1-score promedio ponderado mayor a 0.75** sobre el conjunto de prueba.

## Descripción del Modelo

Se siguió un enfoque progresivo de tres etapas para el desarrollo y comparación de modelos:

### Etapa 1 — Modelo Baseline (CNN desde cero)

Red neuronal convolucional diseñada desde cero como línea de referencia. Recibe imágenes RGB de **224 × 224 px** normalizadas a [0, 1].

| Componente | Detalle |
|---|---|
| Bloques convolucionales | 3 bloques con filtros (32, 64, 128); 2 capas Conv2D por bloque |
| Normalización | Batch Normalization tras cada convolución |
| Reducción espacial | MaxPooling2D (2 × 2) por bloque |
| Pooling global | GlobalAveragePooling2D |
| Capas densas | Dense(512) → Dropout(0.2) → Dense(256) → Dropout(0.2) |
| Salida | Dense(9, softmax) |
| Aumentación | RandomFlip, RandomRotation(0.15), RandomZoom(0.2) |
| Optimizador | Adam (lr = 0.001) |
| Total parámetros | 488 K |

Los hiperparámetros se seleccionaron mediante búsqueda en cuadrícula (Grid Search). Se aplicaron pesos de clase balanceados para compensar el desbalance del dataset y EarlyStopping con `patience=15`.

### Etapa 2 — Transfer Learning (InceptionV3 congelado)

Se empleó **InceptionV3** (Szegedy et al., 2016) preentrenada en ImageNet como extractor de características, con el backbone completamente **congelado**. Las imágenes se redimensionaron a **299 × 299 px** (entrada nativa de InceptionV3) y se reescalaron de [0, 1] a [−1, 1].

Se exploró una rejilla de 24 combinaciones de hiperparámetros del clasificador (*head*):

| Hiperparámetro | Valores explorados |
|---|---|
| Learning rate | 1 × 10⁻³, 3 × 10⁻⁴, 1 × 10⁻⁴ |
| Capas densas del head | 1, 2 |
| Unidades por capa densa | 256, 512 |
| Dropout rate | 0.30, 0.50 |

El mejor clasificador encontrado se reentrenó durante 20 épocas con EarlyStopping (`patience=5`) y ReduceLROnPlateau, guardándose como `best_tl_model.keras`.

### Etapa 3 — Fine-Tuning (InceptionV3 parcialmente descongelado)

Partiendo del modelo TL entrenado, se descongelaron progresivamente las capas superiores del backbone InceptionV3 para adaptar sus pesos al dominio de residuos, siguiendo el enfoque de Single et al. (2023). El resto del backbone permaneció congelado.

Se exploró una rejilla de 6 combinaciones:

| Hiperparámetro | Valores explorados |
|---|---|
| Learning rate | 1 × 10⁻⁴, 5 × 10⁻⁵, 1 × 10⁻⁵ |
| Capas del backbone a descongelar | 20, 50 |

El modelo final (`best_ft_model.keras`) fue seleccionado con los hiperparámetros de mayor `val_accuracy` y entrenado durante 20 épocas con EarlyStopping y ReduceLROnPlateau.

### Modelo de Producción

Los hiperparámetros óptimos del modelo FT se extrajeron automáticamente del archivo guardado y se aplicaron para reentrenar sobre el dataset ampliado `realwaste_mod` con partición **90 % entrenamiento / 10 % validación**, sin conjunto de prueba independiente. El modelo resultante se almacena como `model_prd.keras`.

## Evaluación del Modelo

### Partición de datos

Se aplicó una partición **estratificada** del dataset RealWaste original para los experimentos de comparación:

| Conjunto | Proporción | Imágenes |
|---|---|---|
| Entrenamiento | 70 % | 3,326 |
| Validación | 15 % | 713 |
| Prueba | 15 % | 713 |

### Métricas utilizadas

- **Accuracy** — proporción global de predicciones correctas.
- **Precision** — fracción de predicciones positivas que son correctas (por clase).
- **Recall** — fracción de muestras reales de cada clase identificadas correctamente.
- **F1-score** — media armónica de Precision y Recall.
- **Macro avg** — promedio no ponderado de las métricas por clase.
- **Weighted avg** — promedio ponderado por número de muestras de cada clase.

### Resultados comparativos

#### Accuracy global en el conjunto de prueba

| Modelo | Accuracy |
|---|---|
| Baseline (CNN) | 64.66 % |
| Transfer Learning | 92.01 % |
| **Fine-Tuning (InceptionV3)** | **96.91 %** |

El modelo de Fine-Tuning supera el criterio de éxito definido (> 75 %) por un amplio margen y mejora en **4.9%** al modelo de Transfer Learning.

#### Precision por clase

Los tres modelos muestran una progresión clara en precision. El Baseline presenta mayor variabilidad entre clases (rango 0.40–0.80), con *Textile Trash* como la clase de menor precisión. El modelo de Transfer Learning eleva todos los valores por encima de 0.83, y el Fine-Tuning los concentra por encima de 0.93 en todas las clases.

#### Recall por clase

El patrón es similar: en el Baseline, *Miscellaneous Trash* tiene el recall más bajo (0.45); los modelos basados en InceptionV3 logran recall superior a 0.75 en todas las clases, con Fine-Tuning superando 0.87 incluso en la clase más difícil.

#### F1-score por clase

- **Baseline**: rango 0.49–0.79; mayor dispersión.
- **Transfer Learning**: rango 0.80–0.97; mejora sistemática.
- **Fine-Tuning**: rango 0.92–0.99; rendimiento uniforme en todas las clases.

### Matrices de confusión

Las matrices de confusión normalizadas por fila (proporción de muestras reales clasificadas en cada categoría predicha) confirman la evolución:

- **Baseline**: errores frecuentes entre clases visualmente similares (e.g., *Miscellaneous Trash* confundido con *Plastic*, *Textile Trash* con otras clases).
- **Transfer Learning**: diagonal dominante con valores ≥ 0.75 en la mayoría de clases; persistencia de confusión en *Miscellaneous Trash*.
- **Fine-Tuning**: diagonal prácticamente perfecta (≥ 0.87 en todas las clases); confusiones residuales únicamente en *Miscellaneous Trash* y *Food Organics*.

### Complejidad del modelo

| Modelo | Parámetros totales | Entrenables | No entrenables | Peso en disco |
|---|---|---|---|---|
| Baseline (CNN) | 488,489 | 487,593 | 896 | 5.7 MB |
| Transfer Learning | 22,330,665 | 527,369 | 21,803,296 | 90.3 MB |
| Fine-Tuning (InceptionV3) | 22,330,665 | 7,700,681 | 14,629,984 | 145.8 MB |

## Conclusiones y Recomendaciones

### Puntos fuertes

- El modelo de **Fine-Tuning de InceptionV3** alcanza una **accuracy de 96.91 %** y un F1-score superior a 0.92 en todas las clases, superando ampliamente el umbral de éxito del proyecto.
- La estrategia de fine-tuning progresivo (partir del modelo TL entrenado y descongelar solo las capas superiores) resultó eficaz para adaptar InceptionV3 al dominio de residuos con un dataset de tamaño moderado (4.752 imágenes).
- La aplicación de pesos de clase balanceados fue determinante para mitigar el impacto del desbalance entre categorías (_Plastic_: 921 imágenes vs. _Textile Trash_: 318 imágenes).
- El rendimiento uniforme entre clases en el modelo de Fine-Tuning indica que el modelo generaliza bien incluso para clases minoritarias y visualmente heterogéneas como *Miscellaneous Trash*.

### Puntos débiles y limitaciones

- *Miscellaneous Trash* y *Food Organics* son las clases con menor F1-score incluso en el mejor modelo, lo cual es esperable dado que la primera es una mezcla heterogénea de materiales y la segunda presenta alta variabilidad visual.
- El modelo requiere imágenes de **299 × 299 px** y un peso en disco de 145.8 MB, lo que puede ser una restricción para despliegue en dispositivos con recursos limitados.
- El dataset está limitado a residuos de un único sitio de vertedero en Australia; la generalización a instalaciones con condiciones visuales muy distintas puede requerir reentrenamiento o ajustes adicionales.

### Recomendaciones

- Para el despliegue móvil, evaluar el uso de arquitecturas más eficientes en parámetros como **EfficientNetV2** para mantener alta accuracy con menor huella computacional.
- Explorar técnicas de **data augmentation avanzada** específicamente para las clases de menor rendimiento (*Miscellaneous Trash*, *Food Organics*) para mejorar la robustez del modelo.
- En futuras iteraciones, incorporar imágenes de otros sitios de vertedero para mejorar la capacidad de generalización del modelo.

## Referencias

- Single, S., Iranmanesh, S., & Raad, R. (2023). RealWaste: A Novel Real-Life Data Set for Landfill Waste Classification Using Deep Learning. *Information*, 14(12), 633. https://doi.org/10.3390/info14120633
- Beach, J. (2023). RealWaste Dataset. Kaggle. Recuperado de https://www.kaggle.com/datasets/joebeachcapital/realwaste
- Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., & Wojna, Z. (2016). Rethinking the Inception Architecture for Computer Vision. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 2818–2826. https://doi.org/10.1109/CVPR.2016.308