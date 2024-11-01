# order_execution/python_bindings.py

import ctypes
import os
import sys
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

class OrderExecutor:
    def __init__(self, library_path: str = None):
        if library_path is None:
            library_path = os.path.join(os.path.dirname(__file__), 'cpp', 'liborder_executor.so')
            if sys.platform == 'darwin':
                library_path = os.path.join(os.path.dirname(__file__), 'cpp', 'liborder_executor.dylib')
            elif sys.platform == 'win32':
                library_path = os.path.join(os.path.dirname(__file__), 'cpp', 'order_executor.dll')
        if not os.path.exists(library_path):
            raise FileNotFoundError(f"Order executor library not found at {library_path}")
        self.lib = ctypes.CDLL(library_path)
        self.lib.OrderExecutor_new.restype = ctypes.c_void_p
        self.lib.OrderExecutor_execute.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.OrderExecutor_execute_bulk.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int]
        self.lib.OrderExecutor_delete.argtypes = [ctypes.c_void_p]
        self.executor = self.lib.OrderExecutor_new()
        logger.info("OrderExecutor Python binding initialized.")

    def execute_order(self, order: str):
        self.lib.OrderExecutor_execute(self.executor, order.encode('utf-8'))
        logger.debug(f"Order executed: {order}")

    def execute_bulk_orders(self, orders: List[str]):
        c_orders = (ctypes.c_char_p * len(orders))()
        for i, order in enumerate(orders):
            c_orders[i] = order.encode('utf-8')
        self.lib.OrderExecutor_execute_bulk(self.executor, c_orders, len(orders))
        logger.debug(f"Bulk orders executed: {orders}")

    def __del__(self):
        try:
            self.lib.OrderExecutor_delete(self.executor)
            logger.info("OrderExecutor Python binding terminated.")
        except Exception as e:
            logger.exception(f"Error deleting OrderExecutor: {e}")
