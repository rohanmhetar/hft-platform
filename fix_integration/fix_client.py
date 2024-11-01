# fix_integration/fix_client.py

import quickfix as fix
from fix_session import FixSession
from utils.logger import get_logger

logger = get_logger(__name__)

class FixClient:
    def __init__(self, config_file: str):
        self.session_settings = fix.SessionSettings(config_file)
        self.application = FixSession()
        self.store_factory = fix.FileStoreFactory(self.session_settings)
        self.log_factory = fix.FileLogFactory(self.session_settings)
        self.initiator = fix.SocketInitiator(
            self.application,
            self.store_factory,
            self.session_settings,
            self.log_factory
        )
        logger.info("FIX client initialized.")

    def start(self):
        self.initiator.start()
        logger.info("FIX client started.")

    def stop(self):
        self.initiator.stop()
        logger.info("FIX client stopped.")

    def send_order(self, order_details: dict):
        try:
            order = fix44.NewOrderSingle()
            order.setField(fix.ClOrdID(order_details['ClOrdID']))
            order.setField(fix.HandlInst('1'))
            order.setField(fix.Symbol(order_details['Symbol']))
            order.setField(fix.Side(order_details['Side']))
            order.setField(fix.TransactTime())
            order.setField(fix.OrdType(order_details['OrdType']))
            order.setField(fix.OrderQty(order_details['OrderQty']))
            order.setField(fix.Price(order_details['Price']))
            fix.Session.sendToTarget(order, self.application.session_id)
            logger.info(f"Sent NewOrderSingle: {order_details['ClOrdID']}")
        except fix.SessionNotFound as e:
            logger.error(f"Session not found: {e}")
        except Exception as e:
            logger.exception(f"Error sending order: {e}")

    def send_order_cancel(self, cancel_details: dict):
        try:
            cancel_request = fix44.OrderCancelRequest()
            cancel_request.setField(fix.OrigClOrdID(cancel_details['OrigClOrdID']))
            cancel_request.setField(fix.ClOrdID(cancel_details['ClOrdID']))
            cancel_request.setField(fix.Symbol(cancel_details['Symbol']))
            cancel_request.setField(fix.OrderQty(cancel_details['OrderQty']))
            fix.Session.sendToTarget(cancel_request, self.application.session_id)
            logger.info(f"Sent OrderCancelRequest: {cancel_details['ClOrdID']}")
        except fix.SessionNotFound as e:
            logger.error(f"Session not found: {e}")
        except Exception as e:
            logger.exception(f"Error sending order cancel request: {e}")
