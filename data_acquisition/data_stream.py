import asyncio
import websockets
import json
import numpy as np
from data_processor import DataProcessor
from utils.logger import get_logger

logger = get_logger(__name__)

class DataStream:
    def __init__(self, uri: str, processor: DataProcessor, reconnect_interval: int = 5):
        self.uri = uri
        self.processor = processor
        self.reconnect_interval = reconnect_interval
        self.websocket = None
        self.connected = False

    async def connect(self):
        while True:
            try:
                logger.info(f"Attempting to connect to data stream at {self.uri}")
                async with websockets.connect(self.uri) as websocket:
                    self.websocket = websocket
                    self.connected = True
                    logger.info(f"Connected to data stream at {self.uri}")
                    await self.receive()
            except (websockets.exceptions.ConnectionClosedError, 
                    websockets.exceptions.InvalidURI,
                    ConnectionRefusedError) as e:
                logger.error(f"Connection error: {e}. Reconnecting in {self.reconnect_interval} seconds.")
                self.connected = False
                await asyncio.sleep(self.reconnect_interval)
            except Exception as e:
                logger.exception(f"Unexpected error: {e}")
                self.connected = False
                await asyncio.sleep(self.reconnect_interval)

    async def receive(self):
        async for message in self.websocket:
            try:
                data = json.loads(message)
                await self.processor.enqueue_data(data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e} - Message: {message}")
            except Exception as e:
                logger.exception(f"Error processing message: {e}")

    def start(self):
        asyncio.create_task(self.connect())
