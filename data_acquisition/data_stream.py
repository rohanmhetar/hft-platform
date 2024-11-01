# data_acquisition/data_stream.py

import asyncio
import websockets
import json
import numpy as np
from data_processor import DataProcessor
from utils.logger import get_logger
import yaml
import os

logger = get_logger(__name__)

class DataStream:
    def __init__(self, provider: str, config: dict, processor: DataProcessor, reconnect_interval: int = 5):
        self.provider = provider
        self.config = config
        self.processor = processor
        self.reconnect_interval = reconnect_interval
        self.websocket = None
        self.connected = False

    async def connect(self):
        if self.provider == "polygon":
            await self.connect_polygon()
        else:
            logger.error(f"Unsupported data provider: {self.provider}")

    async def connect_polygon(self):
        uri = self.config['polygon']['websocket_uri']
        api_key = self.config['polygon']['api_key']
        headers = {"Authorization": f"Bearer {api_key}"}
        while True:
            try:
                logger.info(f"Connecting to Polygon WebSocket at {uri}")
                async with websockets.connect(uri, extra_headers=headers) as websocket:
                    self.websocket = websocket
                    self.connected = True
                    logger.info("Connected to Polygon WebSocket.")
                    
                    # Subscribe to relevant channels (e.g., trades for specific symbols)
                    subscribe_message = {
                        "action": "subscribe",
                        "params": "T.*"  # Subscribe to all trade updates
                    }
                    await websocket.send(json.dumps(subscribe_message))
                    logger.info("Subscribed to trade updates.")

                    await self.receive_polygon()
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

    async def receive_polygon(self):
        async for message in self.websocket:
            try:
                data = json.loads(message)
                if 'ev' in data and data['ev'] == 'T':  # Trade event
                    trade_data = {
                        'timestamp': data.get('t', 0),
                        'price': data.get('p', 0.0),
                        'volume': data.get('s', 0),
                        'bid': data.get('bp', 0.0),
                        'ask': data.get('ap', 0.0)
                    }
                    await self.processor.enqueue_data(trade_data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e} - Message: {message}")
            except Exception as e:
                logger.exception(f"Error processing message: {e}")

    def start(self):
        asyncio.create_task(self.connect())
