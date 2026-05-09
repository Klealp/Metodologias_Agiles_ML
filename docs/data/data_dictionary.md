# Diccionario de datos

## Base de datos

Dataset **RealWaste** obtenido de Kaggle (joebeachcapital/realwaste). Contiene 4.752 imágenes JPG capturadas en la instalación Shoalhaven Waste Management Facility (Nowra, Australia) en condiciones reales de vertedero. Las imágenes están organizadas en subdirectorios, donde el nombre del directorio corresponde a la etiqueta de clase. Referencia: Single et al. (2023). DOI: 10.3390/a16060299.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| label | Etiqueta de clase de cada imagen, representada por el nombre del subdirectorio que la contiene | categórico | {Cardboard, Food Organics, Glass, Metal, Miscellaneous Trash, Paper, Plastic, Textile Trash, Vegetation} | Estructura de directorios en `joebeachcapital/realwaste/realwaste-main/RealWaste/` |
| Cardboard | Imágenes de residuos de cartón | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Cardboard/` — 461 imágenes |
| Food Organics | Imágenes de residuos orgánicos de alimentos | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Food Organics/` — 411 imágenes |
| Glass | Imágenes de residuos de vidrio | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Glass/` — 420 imágenes |
| Metal | Imágenes de residuos metálicos | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Metal/` — 790 imágenes |
| Miscellaneous Trash | Imágenes de residuos misceláneos no categorizables en otras clases | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Miscellaneous Trash/` — 495 imágenes |
| Paper | Imágenes de residuos de papel | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Paper/` — 500 imágenes |
| Plastic | Imágenes de residuos plásticos | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Plastic/` — 921 imágenes |
| Textile Trash | Imágenes de residuos textiles | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Textile Trash/` — 318 imágenes |
| Vegetation | Imágenes de residuos de vegetación | numpy array | (524, 524, 3) — valores de píxel en [0, 255] | Directorio `joebeachcapital/realwaste/realwaste-main/RealWaste/Vegetation/` — 436 imágenes |

- **Variable**: nombre de la variable o clase del dataset.
- **Descripción**: breve descripción del contenido de la variable o categoría.
- **Tipo de dato**: tipo de dato que contiene la variable.
- **Rango/Valores posibles**: forma del array o conjunto de valores posibles para la variable.
- **Fuente de datos**: ruta o directorio de origen dentro del dataset descargado.

