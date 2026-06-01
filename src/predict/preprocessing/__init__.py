import tensorflow as tf

IMG_SIZE = 299


def preprocess_image(raw_bytes: bytes) -> tf.Tensor:
    img = tf.image.decode_jpeg(raw_bytes, channels=3)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, axis=0)
    return img
