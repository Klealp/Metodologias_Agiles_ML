# Clasificación de Residuos con Machine Learning

Proyecto de clasificación de imágenes de residuos sólidos — Programa de Formación en ML y Data Science, Universidad Nacional de Colombia.

**Dataset:** [RealWaste](https://www.kaggle.com/datasets/joebeachcapital/realwaste) — 4 752 imágenes JPG (524×524×3) en 9 clases de residuos.

**Integrantes:** Kevin Andres Leal Perez · Dairo Enrique Morales Jimenez · Sergio Andres Sierra Garcia

---

## Instalación

```bash
pip install -e .
```

Ejecutar una vez desde la raíz. Habilita imports limpios desde cualquier notebook o script:

```python
from scripts.data_acquisition.main import load_dataset
from scripts.preprocessing.main import preprocess_dataset
```

## Login NAS

net use Z: "\\192.168.0.12\data-metodologias" /user:"usuario" "contraseña" /persistent:yes

## Módulos

| Módulo | Función | Descripción |
|---|---|---|
| `scripts.data_acquisition.main` | `load_dataset()` | Descarga RealWaste desde Kaggle. Retorna `(df, path)`. |
| `scripts.preprocessing.main` | `preprocess_dataset(df)` | Balancea clases minoritarias con data augmentation. Retorna `df_augmented`. |

## Agregar un módulo nuevo

1. Crear carpeta en `scripts/` con `__init__.py`.
2. Agregar el `.py` con las funciones.
3. Importar con `from scripts.<carpeta>.<archivo> import <funcion>`.


## Pruebas

*\Metodologias_Agiles_ML> python scripts/data_acquisition/main.py

Warning: Looks like you're using an outdated `kagglehub` version (installed: 0.3.13), please consider upgrading to the latest version (1.0.0).
Dataset cargado: 4752 imágenes en 9 clases
Ruta: C:\Users\*\.cache\kagglehub\datasets\joebeachcapital\realwaste\versions\1\realwaste-main\RealWaste
label
Plastic                921
Metal                  790
Paper                  500
Miscellaneous Trash    495
Cardboard              461
Vegetation             436
Glass                  420
Food Organics          411
Textile Trash          318
Name: count, dtype: int64
*\ Metodologias_Agiles_ML> python scripts/preprocessing/main.py

026-05-16 00:40:12.574719: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-05-16 00:40:14.506281: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
Warning: Looks like you're using an outdated `kagglehub` version (installed: 0.3.13), please consider upgrading to the latest version (1.0.0).
Imágenes a generar: 1859
2026-05-16 00:40:17.867638: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
  500/1859 imágenes generadas
  1000/1859 imágenes generadas
  1500/1859 imágenes generadas
Distribución final:
label
Plastic                921
Metal                  790
Cardboard              710
Food Organics          710
Paper                  703
Textile Trash          697
Glass                  697
Vegetation             697
Miscellaneous Trash    686
Name: count, dtype: int64