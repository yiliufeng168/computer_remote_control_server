# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/8/27 18:29
#   @File : controller.py
#   @des: 
# ================================================================
import json
import logging
import os
import time
import hashlib
from config import DEFAULT_CONFIGS
from Server.commands import predefined, keyboard_control, mouse_control, input_msg, do_system_cmd, speak
from util.ChromeBrowser import browser


def handler_command(command):
    if command['type'] == 'predefined':
        predefined(command['command'], command['args'])
    elif command['type'] == 'keyboard':
        keyboard_control(command['command'], command['args'])
    elif command['type'] == 'mouse':
        mouse_control(command['command'], command['args'])
    elif command['type'] == 'input_msg':
        input_msg(command['command'], command['args'])
    elif command['type'] == 'speak':
        speak(command['command'], command['args'])
    elif command['type'] == 'browser':
        browser(command['command'], command['args'])
    else:
        # logging.info('shell: '+ command['content'])
        do_system_cmd(command['command'])


def handler(body):
    # 将内容分成两部分
    # 1. 控制命令
    # 2. 动态密码：内容MD5+时间->动态密码
    if body['type'] == 'command_list':
        # 进行hash校验
        text = json.dumps(body['content'], ensure_ascii=False, separators=(',', ':')) + str(int(time.time()) // 120) + \
               DEFAULT_CONFIGS['password']
        check_sum = hashlib.md5(text.encode('utf-8')).hexdigest()
        if body['check_sum'] == check_sum:
            for item in body['content']:
                handler_command(item)
        else:
            logging.error(text)
            logging.error('校验失败')
    # if body['type'] == 'command':
    #     command = json.loads(body['content'])
    #     handler_command(command)
    # elif body['type'] == 'command_list':
    #     command_list = json.loads(body['content'])
    #     for command in command_list:
    #         handler_command(command)
