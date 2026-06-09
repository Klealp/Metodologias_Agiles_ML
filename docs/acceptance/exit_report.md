# Informe de salida

## Resumen Ejecutivo

El proyecto **Clasificación Automática de Residuos en Vertederos mediante Fine-Tuning de InceptionV3** desarrolló un sistema de deep learning capaz de clasificar imágenes de residuos sólidos en las 9 categorías del dataset **RealWaste**. El modelo final alcanzó un **accuracy del 96.91 %** en el conjunto de prueba, superando ampliamente el criterio de éxito definido en el *Project Charter* (accuracy > 75 % y F1-score ponderado > 0.75). El modelo fue desplegado como una aplicación web funcional que permite clasificar residuos en tiempo real mediante carga de imágenes o captura con cámara.

## Resultados del proyecto

- **Entendimiento de los datos:** Se realizó un EDA exhaustivo sobre las 4.752 imágenes JPG (524×524 px, 9 clases) del dataset RealWaste. Los datos resultaron de excelente calidad (sin nulos, corruptos ni duplicados), con un desbalance moderado de clases (Plastic y Metal > 700; Textile Trash con menor representación).
- **Preparación de datos:** Se trató el problema de clases desbalanceadas asignando **pesos más grandes a las clases minoritarias** y se redimensionaron las imágenes a 299×299 px (entrada nativa de InceptionV3) mediante interpolación Lanczos.
- **Modelamiento:** Se desarrollaron y compararon tres modelos en un enfoque progresivo:

  | Modelo | Accuracy (test) | Parámetros |
  |---|---|---|
  | Baseline CNN (desde cero) | 64.66 % | 0.49 M |
  | Transfer Learning (InceptionV3) | 92.01 % | 22.33 M |
  | **Fine-Tuning (InceptionV3)** | **96.91 %** | **22.33 M** |

- **Modelo final vs. baseline:** El modelo de Fine-Tuning seleccionado para producción (`model_prd.keras`) representa una mejora de más de **32 puntos porcentuales** respecto a la línea base, con un F1-score superior a 0.92 en todas las clases y un rendimiento uniforme incluso en las categorías más difíciles.
- **Despliegue:** Se implementó la aplicación en una máquina on premise mediante contenedores Docker (frontend React/Nginx + API FastAPI/TensorFlow), accesible localmente y de forma remota a través de un túnel Cloudflare en [realwaste.sierrainnovate.com](https://realwaste.sierrainnovate.com) y con una API con Endpoint en el dominio: [eprealwaste.sierrainnovate.com](https://eprealwaste.sierrainnovate.com/docs).

## Lecciones aprendidas

- **Datos:** La calidad y consistencia del dataset RealWaste facilitó el pipeline de preprocesamiento; el principal reto fue el desbalance de clases, mitigado eficazmente con pesos de clase balanceados.
- **Modelamiento:** El *transfer learning* sobre arquitecturas preentrenadas en ImageNet supera con amplitud a una CNN entrenada desde cero cuando el dataset es de tamaño moderado (~4.752 imágenes). El fine-tuning progresivo (descongelar solo las capas superiores partiendo del modelo TL) resultó determinante para el salto final de rendimiento.
- **Clases difíciles:** *Miscellaneous Trash* y *Food Organics* concentran los errores residuales, debido a su heterogeneidad y variabilidad visual.
- **Despliegue:** La contenerización con Docker Compose y el uso de un túnel Cloudflare permitieron exponer el servicio de forma segura sin abrir puertos directamente a Internet.
- **Recomendaciones para futuros proyectos:** Evaluar arquitecturas más livianas (p. ej. EfficientNetV2) para despliegue móvil, incorporar imágenes de otros sitios de vertedero para mejorar la generalización a variaciones en las condiciones en que es tomada la foto del residuo, y aplicar *data augmentation* avanzada en las clases de menor desempeño.

## Impacto del proyecto

El sistema automatiza la identificación de los 9 tipos de residuos del dataset, reduciendo la dependencia de la clasificación manual y los riesgos de exposición a materiales peligrosos para los trabajadores de las plantas de recuperación de materiales. Al optimizar la separación y el reciclaje, aporta valor directo a empresas de gestión de residuos sólidos urbanos y organismos ambientales interesados en la automatización a escala industrial.

Como áreas de mejora y oportunidades futuras se identifican: la migración a una nube pública (AWS) con autoescalado y balanceo de carga para gestionar picos de demanda, la incorporación de mecanismos de protección (AWS WAF) y la ampliación del dataset con datos de múltiples instalaciones.

## Conclusiones

- El modelo de **Fine-Tuning de InceptionV3** cumplió y superó ampliamente los objetivos del proyecto, alcanzando una **accuracy del 96.91 %** y un F1-score uniforme y elevado en todas las clases.
- Se entregó un producto completo y funcional: desde el análisis de datos y el modelamiento hasta un sistema desplegado y accesible en producción.
- Para futuros proyectos se recomienda priorizar enfoques de transfer learning, atender desde el inicio el balance de clases y considerar la eficiencia computacional del modelo cuando el destino sea un despliegue con recursos limitados.

## Agradecimientos

Agradecemos al equipo de profesores del curso de Metodologías Agiles para el Desarrollo de Software por sus enseñanzas en todas las etapas del curso. Un reconocimiento especial a los autores del dataset **RealWaste** (Single et al., 2023) por poner a disposición un conjunto de datos de condiciones reales, y a los stakeholders y expertos en gestión ambiental que validaron la relevancia de las categorías de clasificación.

## Referencias

- Single, S., Iranmanesh, S., & Raad, R. (2023). RealWaste: A Novel Real-Life Data Set for Landfill Waste Classification Using Deep Learning. Algorithms, 16(6), 299. https://doi.org/10.3390/info14120633
- Beach, J. (2023). RealWaste Dataset. Kaggle. Recuperado de https://www.kaggle.com/datasets/joebeachcapital/realwaste
