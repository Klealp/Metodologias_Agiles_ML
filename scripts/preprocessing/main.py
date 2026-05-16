import os
import random
import warnings
import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

from scripts.data_acquisition.main import load_dataset


def _apply_random_transform(image: tf.Tensor) -> tf.Tensor:
    transformations = [
        lambda img: keras.layers.RandomBrightness(factor=0.3)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomContrast(factor=0.3)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomSaturation(factor=(0.5, 1.5))(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomHue(factor=0.1)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomRotation(factor=0.15)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomZoom(height_factor=0.2)(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomFlip(mode="horizontal")(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomFlip(mode="vertical")(img[tf.newaxis])[0],
        lambda img: keras.layers.RandomShear(x_factor=0.1, y_factor=0.1)(img[tf.newaxis])[0],
        lambda img: keras.layers.GaussianNoise(stddev=0.05)(img[tf.newaxis], training=True)[0],
    ]
    return random.choice(transformations)(image)


def preprocess_dataset(
    df: pd.DataFrame,
    target_count: int = 700,
    output_dir: str = "data/augmented",
) -> pd.DataFrame:
    """
    Balancea el dataset mediante data augmentation en las clases con menos de
    target_count imágenes y guarda las imágenes generadas en disco.

    Args:
        df           : DataFrame con columnas ['image_path', 'label'].
        target_count : Número objetivo de imágenes por clase minoritaria.
        output_dir   : Carpeta raíz donde se guardan las imágenes aumentadas.

    Returns:
        DataFrame balanceado con rutas reales a todas las imágenes.
    """
    conteos = df.groupby("label")["image_path"].count()

    diferencias = (target_count - conteos).clip(lower=0)
    n_aumentos = int(diferencias.sum())
    probabilidades = diferencias / diferencias.sum()

    print(f"Imágenes a generar: {n_aumentos}")

    records = []
    for i in range(n_aumentos):
        category = np.random.choice(conteos.index, p=probabilidades)
        img_path = np.random.choice(df[df["label"] == category]["image_path"])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            image = tf.convert_to_tensor(
                np.array(Image.open(img_path)) / 255.0, dtype=tf.float32
            )

        augmented = _apply_random_transform(image)

        save_dir = os.path.join(output_dir, category)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"aug_{i}_{os.path.basename(img_path)}")
        Image.fromarray((augmented.numpy() * 255).astype(np.uint8)).save(save_path)

        records.append({"image_path": save_path, "label": category})

        if (i + 1) % 500 == 0:
            print(f"  {i + 1}/{n_aumentos} imágenes generadas")

    df_augmented = pd.concat([df, pd.DataFrame(records)], ignore_index=True)
    print("Distribución final:")
    print(df_augmented["label"].value_counts())
    return df_augmented


if __name__ == "__main__":
    df, _ = load_dataset()
    df_augmented = preprocess_dataset(df)
