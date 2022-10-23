# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/10/13 15:43
#   @File : __init__.py.py
#   @des: 
# ================================================================
import socketserver
import logging
import json
from Server.controller import handler


class MyServer(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        try:

            content = self.request[0].decode('utf-8')
            logging.info(content)
            if content:
                body = json.loads(content)
                handler(body)
        except Exception as e:
            logging.error(e)
            logging.exception(e)

    def setup(self) -> None:
        logging.info('setup')
        super().setup()

    def finish(self) -> None:
        logging.info('finish')
        super().finish()

