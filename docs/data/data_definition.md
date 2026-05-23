# Definición de los datos

## Origen de los datos

Los datos provienen del dataset **RealWaste**, disponible públicamente en Kaggle bajo el identificador [`joebeachcapital/realwaste`](https://www.kaggle.com/datasets/joebeachcapital/realwaste). El dataset fue recolectado con el propósito de representar condiciones reales de clasificación de residuos en vertederos, capturando imágenes desde un ángulo superior sobre superficies con variabilidad de iluminación y tamaño de los objetos.

La descarga se realiza de forma automática mediante la biblioteca `kagglehub`, que gestiona el _fetching_ en Kaggle y el almacenamiento en caché local.

## Especificación de los scripts para la carga de datos

| Script | Propósito |
|---|---|
| `scripts/eda/M5U3_2_exploratory_data_analysis.ipynb` | Carga del dataset, construcción del DataFrame con rutas e etiquetas, análisis exploratorio |
| `scripts/preprocessing/M5U3_2_data_preprocessing.ipynb` | Preparación y limpieza: rebalanceo de clases mediante *data augmentation* y redimensionamiento a 299×299 px para InceptionV3 |

La carga se realiza con el siguiente flujo:

```python
import kagglehub
path = kagglehub.dataset_download("joebeachcapital/realwaste")
path = os.path.join(path, 'realwaste-main', 'RealWaste')
```

A partir de las carpetas por clase se construye un DataFrame con columnas `image_path` y `label`.

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

- **Ruta de descarga automática (caché local):**
  ```
  C:\Users\<usuario>\.cache\kagglehub\datasets\joebeachcapital\realwaste\versions\1\realwaste-main\RealWaste\
  ```

- **Almacenamiento con dvc en carpeta local**
  ```
  realwaste/ (en carpeta local, gestionada por dvc con repositorio remoto NAS accedido a través de VPN)
  ```

- **Estructura de directorios:**
  ```
  RealWaste/
  ├── Cardboard/          (imágenes .jpg)
  ├── Food Organics/      (imágenes .jpg)
  ├── Glass/              (imágenes .jpg)
  ├── Metal/              (imágenes .jpg)
  ├── Miscellaneous Trash/ (imágenes .jpg)
  ├── Paper/              (imágenes .jpg)
  ├── Plastic/            (imágenes .jpg)
  ├── Textile Trash/      (imágenes .jpg)
  └── Vegetation/         (imágenes .jpg)
  ```

- **Formato de archivos:** JPEG (`.jpg`), resolución uniforme de **524 × 524 píxeles**, 3 canales RGB.
- **Tamaño total:** 656.42 MB.
- **Convención de nombres de archivo:** `<Clase>_<número>.jpg` (ej. `Cardboard_1.jpg`).

- **Procedimientos de transformación y limpieza:**
  - Verificación de integridad: archivos ilegibles, imágenes vacías o constantes.
  - Rebalanceo de clases minoritarias (< 700 imágenes) mediante *data augmentation* con transformaciones aleatorias (brillo, contraste, rotación, traslación, zoom, flip, ruido gaussiano, entre otras).
  - **Redimensionamiento**: la totalidad del dataset (`df`) se redimensiona de 524×524 a **299×299 píxeles** (3 canales RGB) utilizando interpolación Lanczos. Las imágenes resultantes se almacenan en `realwaste_mod/` conservando la estructura de carpetas por clase, y el DataFrame correspondiente es `df_resized`. Esta resolución es la requerida por la arquitectura **InceptionV3**.

### Base de datos de destino

El proyecto no emplea una base de datos relacional como destino. Los datos procesados se mantienen en memoria (DataFrame de pandas  `df_resized`) durante la ejecución del pipeline.

- Las imágenes originales y aumentadas permanecen en `realwaste/` (gestionado por `dvc`).
- Las imágenes redimensionadas a 299×299 se almacenan en `realwaste_mod/`, listas para ser consumidas por el pipeline de entrenamiento con **InceptionV3**.
