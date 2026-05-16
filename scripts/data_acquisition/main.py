import os
import pandas as pd
import kagglehub


def load_dataset() -> tuple[pd.DataFrame, str]:
    """
    Descarga el dataset RealWaste desde Kaggle y construye un DataFrame con las
    rutas de las imágenes y sus etiquetas.

    Returns:
        df   : DataFrame con columnas ['image_path', 'label'].
        path : Ruta local al directorio raíz del dataset (RealWaste/).
    """
    base = kagglehub.dataset_download("joebeachcapital/realwaste")
    path = os.path.join(base, "realwaste-main", "RealWaste")

    records = [
        {"image_path": os.path.join(path, category, img_name), "label": category}
        for category in os.listdir(path)
        for img_name in os.listdir(os.path.join(path, category))
    ]

    df = pd.DataFrame(records)
    return df, path


if __name__ == "__main__":
    df, path = load_dataset()
    print(f"Dataset cargado: {len(df)} imágenes en {df['label'].nunique()} clases")
    print(f"Ruta: {path}")
    print(df["label"].value_counts())
