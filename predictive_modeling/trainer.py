# predictive_modeling/trainer.py

import numpy as np
import tensorflow as tf
from model import PredictiveModel
from utils.logger import get_logger
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

class Trainer:
    def __init__(self, model: PredictiveModel):
        self.model = model
        self.history = None
        logger.info("Trainer initialized.")

    def prepare_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42):
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        logger.info(f"Data split into training and validation sets with test size {test_size}.")

    def train(self, epochs: int = 50, batch_size: int = 32):
        if not hasattr(self, 'X_train'):
            raise AttributeError("Data not prepared. Call prepare_data() before training.")
        self.history = self.model.get_model().fit(
            self.X_train, self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.X_val, self.y_val),
            callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
                tf.keras.callbacks.ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)
            ],
            verbose=1
        )
        logger.info(f"Model training completed for {epochs} epochs.")

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        results = self.model.get_model().evaluate(X_test, y_test, verbose=0)
        evaluation = {metric: value for metric, value in zip(self.model.get_model().metrics_names, results)}
        logger.info(f"Model evaluation results: {evaluation}")
        return evaluation

    def save_model(self, filepath: str):
        self.model.get_model().save(filepath)
        logger.info(f"Model saved to {filepath}.")

    def load_model(self, filepath: str):
        self.model.model = tf.keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}.")
