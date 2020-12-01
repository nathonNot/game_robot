import asyncio
from typing import Tuple
import websockets
import base64
import json
from queue import Queue
from lib import global_data as gbd
import config
from loguru import logger

# # 客户端主逻辑
# async def main_logic():
#     user_info = {
#         "user_id":5,
#         "user_name":"abc",
#         "user_pass":"1111"
#     }
#     user_data = json.dumps(user_info)
#     user_data = base64.b64encode(user_data.encode('utf-8'))
#     url = 'ws://127.0.0.1:8000/ws/'+user_data.decode('utf-8')

#     async with websockets.connect(url) as websocket:
#         cred_text = "i have a connection"
#         await websocket.send(cred_text)
#         while True:
#             response_str = await websocket.recv()
#             print(response_str)

# asyncio.get_event_loop().run_until_complete(main_logic())

class WebSocketClient():

    client = None
    recv_msg_q = Queue()
    loop = asyncio.new_event_loop()
    is_run = True
    
    async def do_login(self):
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
            self.client = await websockets.connect(url)
            cred_text = "i have a connection"
            await self.client.send(cred_text)
            while self.is_run:
                response_str = await self.client.recv()
                data = ""
                try:
                    data = json.loads(response_str)
                except Exception as identifier:
                    logger.error("解析数据错误："+response_str)
                if data == "":
                    continue
                print(data)
        except Exception as identifier:
            logger.info("socket 连接断开 "+str(identifier))

    @classmethod
    def send_msg(cls,obj):
        data = ""
        try:
            data = json.dumps(obj)
        except Exception as identifier:
            logger.error("解析发送消息失败:"+str(obj))
        if data == "":
            return
        cls.loop.run_until_complete(cls.send_msg("ssssss"))

    async def send_msg_sync(self,mes):
        await self.client.send(mes)

    def start_loop(self):
        self.is_run = True
        self.loop.run_until_complete(self.do_login())

    @classmethod
    def close(cls):
        try:
            cls.is_run = False
            if cls.client:
                cls.client.close()
            if cls.loop:
                cls.loop.close()
            if cls.recv_msg_q:
                cls.recv_msg_q.clear()
        except Exception as identifier:
            logger.error(str(identifier))

