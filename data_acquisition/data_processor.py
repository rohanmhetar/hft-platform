import asyncio
import numpy as np
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, batch_size: int = 1000, processing_interval: float = 0.5):
        self.batch_size = batch_size
        self.processing_interval = processing_interval
        self.queue = asyncio.Queue()
        self.processed_data = []
        self.lock = asyncio.Lock()

    async def enqueue_data(self, data: Dict):
        await self.queue.put(data)
        if self.queue.qsize() >= self.batch_size:
            asyncio.create_task(self.process_batch())

    async def process_batch(self):
        async with self.lock:
            batch = []
            while not self.queue.empty() and len(batch) < self.batch_size:
                batch.append(await self.queue.get())
            if batch:
                try:
                    np_data = self._convert_to_numpy(batch)
                    moving_avg = self._compute_moving_average(np_data)
                    self.processed_data.append(moving_avg)
                    logger.info(f"Processed batch of {len(batch)} data points. Moving average shape: {moving_avg.shape}")
                except Exception as e:
                    logger.exception(f"Error in processing batch: {e}")

    def _convert_to_numpy(self, batch: List[Dict]) -> np.ndarray:
        parsed_data = [self._parse_data_point(dp) for dp in batch]
        return np.array(parsed_data, dtype=np.float32)

    def _parse_data_point(self, data_point: Dict) -> List[float]:
        return [
            float(data_point.get('timestamp', 0)),
            float(data_point.get('price', 0)),
            float(data_point.get('volume', 0)),
            float(data_point.get('bid', 0)),
            float(data_point.get('ask', 0))
        ]

    def _compute_moving_average(self, data: np.ndarray) -> np.ndarray:
        window_size = 50
        prices = data[:, 1]
        cumsum = np.cumsum(np.insert(prices, 0, 0))
        moving_avg = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
        return moving_avg

    async def run_periodic_processing(self):
        while True:
            await asyncio.sleep(self.processing_interval)
            if self.queue.qsize() >= self.batch_size:
                await self.process_batch()
