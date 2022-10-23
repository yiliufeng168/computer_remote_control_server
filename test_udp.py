# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/8/27 22:53
#   @File : test_udp.py
#   @des: 
# ================================================================
import socket
import json
import argparse
parse = argparse.ArgumentParser('test')
parse.add_argument('--type',help='type',required=True)
parse.add_argument('--content',help='content',required=True)
args = parse.parse_args()
addr=('127.0.0.1',5002)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
tp = args.type
ct = args.content
content = {
    'type': tp,
    'content': ct
}
pkg = {
    "type": "command",
    "content": json.dumps(content,ensure_ascii=False),
}

s.sendto(json.dumps(pkg,ensure_ascii=False).encode('utf-8'),addr)
s.close()