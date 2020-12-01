import asyncio
import base64
import json
from queue import Queue
from lib import global_data as gbd
import config
from loguru import logger
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread

class WebSocketClient():

    client = None
    
    def do_login(self,):
        if gbd.user_data == None:
            gbd.main_log_info_call_back("用户未登录")
            return
        user_info = {
        "user_id":gbd.user_data.user_id,
        "user_name":gbd.user_data.user_name,
        "user_pass":gbd.user_data.user_pass
        }
        user_data = json.dumps(user_info)
        user_data = base64.b64encode(user_data.encode('utf-8'))
        url = config.ws_url + "/ws/"+user_data.decode('utf-8')
        try:
            websocket.enableTrace(True)
            self.client = websocket.WebSocketApp(url,
                              on_message = WebSocketClient.on_message,
                              on_error = WebSocketClient.on_error,
                              on_close = WebSocketClient.on_close)
            self.client.on_open = WebSocketClient.on_open
            self.client.run_forever()
        except Exception as identifier:
            logger.info("socket 连接断开 "+str(identifier))

    @staticmethod
    def on_message(ws, message):
        logger.info(message)
        ws.send("okokokokokok")

    @staticmethod
    def on_error(ws, error):
        logger.info(error)

    @staticmethod
    def on_close(ws):
        logger.info("### closed ###")

    @staticmethod
    def on_open(ws):
        def run(*args):
            logger.info("con to server")
        thread.start_new_thread(run, ())
