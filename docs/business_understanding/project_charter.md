# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Clasificación Automática de Residuos en Vertederos mediante Fine-Tuning de InceptionV3

## Objetivo del Proyecto

El objetivo principal del proyecto es desarrollar un sistema de clasificación de imágenes de residuos sólidos mediante la técnica de **fine-tuning** sobre la arquitectura **InceptionV3** pre-entrenada en ImageNet, aplicado al conjunto de datos **RealWaste** (Single et al., 2023). El sistema clasificará imágenes capturadas en condiciones reales de vertedero en 9 categorías de residuos, con el fin de optimizar los procesos de separación y reciclaje en instalaciones de gestión de residuos sólidos urbanos, reduciendo la intervención manual y los riesgos para los trabajadores.

## Alcance del Proyecto

### Incluye:

- El proyecto utiliza el conjunto de datos **RealWaste**, disponible en Kaggle ([joebeachcapital/realwaste](https://www.kaggle.com/datasets/joebeachcapital/realwaste/data)), compuesto por **4.752 imágenes JPG** (524 × 524 píxeles) capturadas en la instalación Whyte’s Gully Waste and Resource Recovery Centre’s landfill site located in Wollongong, New South Wales, Australia. Las imágenes están distribuidas en 9 clases: *Cardboard* (461), *Food Organics* (411), *Glass* (420), *Metal* (790), *Miscellaneous Trash* (495), *Paper* (500), *Plastic* (921), *Textile Trash* (318) y *Vegetation* (436).
- Al finalizar el proyecto se espera obtener un modelo de deep learning basado en **fine-tuning de InceptionV3** capaz de clasificar residuos con alta precisión. Los entregables incluyen: el modelo entrenado y guardado, un informe con métricas de rendimiento (exactitud global, precisión, recall, F1-score y matriz de confusión por clase) y un modelo desplegado que permita la clasificación automática de residuos en tiempo real usando la cámara de un dispositivo móvil.
- El proyecto se considerará exitoso si el modelo alcanza una **exactitud global superior al 75%** en el conjunto de prueba y un **F1-score promedio ponderado mayor a 0,75**.

### Excluye:

- El proyecto no contempla el entrenamiento de una arquitectura CNN desde cero. El enfoque es exclusivamente de transfer learning mediante fine-tuning de InceptionV3. Tampoco se incluye la clasificación de categorías de residuos fuera de las 9 clases definidas en RealWaste.

## Metodología

La metodología seguirá el marco **CRISP-DM** de forma iterativa. En la fase de *entendimiento del negocio* se definen los objetivos y el alcance del proyecto. En la fase de *entendimiento de los datos* se realizará un Análisis Exploratorio de Datos (EDA) exhaustivo: distribución de clases, análisis de dimensiones y visualización de muestras representativas. La fase de *preparación de datos* contemplará el preprocesamiento de imágenes, redimensionamiento a 299 × 299 px (entrada requerida por InceptionV3), normalización y data augmentation (rotaciones, volteos, zoom). 

El *modelado* aplicará **Transfer Learning** mediante fine-tuning de **InceptionV3**: primero se entrenarán únicamente las capas añadidas con la base congelada y, posteriormente, se descongelarán gradualmente las capas superiores para adaptar los pesos al dominio de clasificación de residuos, siguiendo el enfoque de Single et al. (2023). Finalmente, el modelo será *evaluado* con métricas estándar de clasificación multiclase sobre el conjunto de prueba.

## Cronograma

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos | 1 semana | lun 4 – dom 10 de mayo del 2026 |
| Preprocesamiento, análisis exploratorio | 1 semana | lun 11 – dom 17 de mayo del 2026 |
| Modelamiento y fine-tuning de InceptionV3 | 1 semana | lun 18 – dom 24 de mayo del 2026 |
| Despliegue | 1 semana | lun 25 – dom 31 de mayo del 2026 |
| Evaluación y entrega final | 1 semana | lun 1 – dom 7 de junio del 2026 |

## Equipo del Proyecto

- **Científico de Datos:** Kevin Andres Leal Perez
- **Científico de Datos:** Dairo Enrique Morales Jimenez
- **Científico de Datos:** Sergio Andres Sierra Garcia

## Presupuesto

| Categoría de Gasto | Descripción | Costo Estimado (USD) | Notas / Consideraciones |
| :----------------- | :---------- | :------------------- | :---------------------- |
| **I. Personal** | | | |
| Científico de Datos (Kevin Leal) | Diseño del esquema de fine-tuning, optimización de hiperparámetros y análisis de resultados. | $4,000 | 1.5 meses a tiempo parcial |
| Científico de Datos (Dairo Morales) | Implementación de código, experimentos y preprocesamiento de imágenes. | $4,000 | 1.5 meses a tiempo parcial |
| Científico de Datos (Sergio Sierra) | EDA, evaluación del modelo y documentación técnica. | $4,000 | 1.5 meses a tiempo parcial |
| **II. Infraestructura y Software** | | | |
| Plataforma Cloud (GPU) | Google Colab Pro para entrenamiento del modelo. | $800 | ~100 horas de GPU |
| Almacenamiento Cloud | NAS para el dataset y checkpoints del modelo. | $1000 | ~50 GB por 1.5 meses |
| Licencias de Software | Python, TensorFlow/Keras, scikit-learn (open-source). | $0 | Sin costo de licencias. |
| **III. Misceláneos** | | | |
| Investigación y Desarrollo | Lectura del artículo de referencia y pruebas de concepto del fine-tuning. | $500 | Exploración de la arquitectura InceptionV3. |
| Gestión de Proyecto | Coordinación, reuniones y documentación. | $300 | Porcentaje del tiempo del equipo. |
| Contingencias | Fondo para imprevistos (~10 % del total estimado). | $1,460 | Buffer para gastos inesperados. |
| **TOTAL ESTIMADO DEL PROYECTO** | | **$16,060** | |

## Stakeholders

- Los stakeholders clave son las **plantas de recuperación de materiales**, empresas de gestión de residuos sólidos urbanos y organismos gubernamentales de medio ambiente interesados en la automatización de la clasificación de residuos a escala industrial.
- Los expertos en gestión ambiental e ingeniería de residuos actúan como validadores del conocimiento de dominio, asegurando que las categorías de clasificación sean relevantes para los procesos reales de separación y reciclaje.
- Las expectativas de los stakeholders se centran en obtener un modelo funcional y preciso que automatice la identificación de los 9 tipos de residuos del dataset RealWaste, reduciendo la dependencia de la clasificación manual y los riesgos de exposición a materiales peligrosos.

## Aprobaciones

- **Kevin Andres Leal Perez** — Científico de Datos
- **Dairo Enrique Morales Jimenez** — Científico de Datos
- **Sergio Andres Sierra Garcia** — Científico de Datos
- Fecha de aprobación: 14 de mayo de 2026

## Referencias

- Single, S., Iranmanesh, S., & Raad, R. (2023). RealWaste: A Novel Real-Life Data Set for Landfill Waste Classification Using Deep Learning. Algorithms, 16(6), 299. https://doi.org/10.3390/info14120633
- Beach, J. (2023). RealWaste Dataset. Kaggle. Recuperado de https://www.kaggle.com/datasets/joebeachcapital/realwaste
