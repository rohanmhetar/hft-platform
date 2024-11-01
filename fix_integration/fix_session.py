# fix_integration/fix_session.py

import quickfix as fix
import quickfix44 as fix44
from utils.logger import get_logger

logger = get_logger(__name__)

class FixSession(fix.Application):
    def __init__(self):
        super().__init__()
        self.session_id = None

    def onCreate(self, sessionID: fix.SessionID):
        self.session_id = sessionID
        logger.info(f"FIX session created: {sessionID}")

    def onLogon(self, sessionID: fix.SessionID):
        logger.info(f"FIX session logon: {sessionID}")

    def onLogout(self, sessionID: fix.SessionID):
        logger.info(f"FIX session logout: {sessionID}")

    def toAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        logger.debug(f"To Admin: {message}")

    def toApp(self, message: fix.Message, sessionID: fix.SessionID):
        logger.debug(f"To App: {message}")

    def fromAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        logger.debug(f"From Admin: {message}")

    def fromApp(self, message: fix.Message, sessionID: fix.SessionID):
        logger.debug(f"From App: {message}")
        self.onMessage(message, sessionID)

    def onMessage(self, message: fix.Message, sessionID: fix.SessionID):
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type == fix.MsgType_NewOrderSingle:
            self.handle_new_order_single(message)
        elif msg_type == fix.MsgType_OrderCancelRequest:
            self.handle_order_cancel_request(message)
        # Additional message types can be handled here

    def handle_new_order_single(self, message: fix.Message):
        cl_ord_id = fix.ClOrdID()
        message.getField(cl_ord_id)
        symbol = fix.Symbol()
        message.getField(symbol)
        side = fix.Side()
        message.getField(side)
        order_qty = fix.OrderQty()
        message.getField(order_qty)
        price = fix.Price()
        message.getField(price)
        logger.info(f"Received NewOrderSingle: ClOrdID={cl_ord_id.getValue()}, Symbol={symbol.getValue()}, "
                    f"Side={side.getValue()}, OrderQty={order_qty.getValue()}, Price={price.getValue()}")
        # Implement order handling logic here

    def handle_order_cancel_request(self, message: fix.Message):
        orig_cl_ord_id = fix.OrigClOrdID()
        message.getField(orig_cl_ord_id)
        cl_ord_id = fix.ClOrdID()
        message.getField(cl_ord_id)
        symbol = fix.Symbol()
        message.getField(symbol)
        order_qty = fix.OrderQty()
        message.getField(order_qty)
        logger.info(f"Received OrderCancelRequest: OrigClOrdID={orig_cl_ord_id.getValue()}, "
                    f"ClOrdID={cl_ord_id.getValue()}, Symbol={symbol.getValue()}, "
                    f"OrderQty={order_qty.getValue()}")
        # Implement order cancellation logic here
