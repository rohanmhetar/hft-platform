# predictive_modeling/model.py

import tensorflow as tf
from tensorflow.keras import layers, models
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)

class PredictiveModel:
    def __init__(self, input_shape: Tuple[int, ...]):
        self.input_shape = input_shape
        self.model = self.build_model()
        logger.info(f"Predictive model initialized with input shape: {self.input_shape}")

    def build_model(self) -> tf.keras.Model:
        model = models.Sequential()
        model.add(layers.Input(shape=self.input_shape))
        model.add(layers.Conv1D(64, kernel_size=3, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Dropout(0.3))
        
        model.add(layers.Conv1D(128, kernel_size=3, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Dropout(0.3))
        
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dropout(0.4))
        model.add(layers.Dense(1, activation='linear'))
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        logger.info("Predictive model built and compiled.")
        return model

    def predict(self, data: tf.Tensor) -> tf.Tensor:
        predictions = self.model.predict(data)
        logger.debug(f"Predictions made: {predictions.shape}")
        return predictions

    def get_model(self) -> tf.keras.Model:
        return self.model
