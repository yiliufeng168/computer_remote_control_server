# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/8/20 20:44
#   @File : test.py
#   @des: 
# ================================================================
import json
import sys
import threading
import time
import psutil


from util.volume import volume_up,volume_down,volume_mute
import os
import mouse
import keyboard
import pyperclip
import winreg
import subprocess



def speak(command,args):
    sentence = json.loads(command)
    # sentence['string']
    # sentence['speaker']
    # tts_sdk(sentence['string'],speaker=sentence['speaker'], output='play',audio='_')


def do_system_cmd(command):
    subprocess.Popen(command,shell=True)


def predefined(command,args):
    if command == 'volume_up':
        volume_up()
    elif command == 'volume_down':
        volume_down()
    elif command == 'mute':
        volume_mute()
    elif command == 'close_window':
        keyboard_control('alt+F4')
    elif command == 'backspace':
        keyboard_control('backspace')
    elif command == 'shutdown':
        os.system('shutdown -s -t 0')
    elif command == 'mouse_up':
        mouse.move(0,-10,False)
    elif command == 'mouse_down':
        mouse.move(0,10,False)
    elif command == 'mouse_left':
        mouse.move(-10,0,False)
    elif command == 'mouse_right':
        mouse.move(10,0,False)
    elif command == 'mouse_left_click':
        mouse.click()
    elif command == 'mouse_right_click':
        mouse.right_click()
    elif command == 'open_cloudmusic':
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\cloudmusic.exe")
        exe_path = winreg.QueryValueEx(key,'')[0]
        do_system_cmd('"{}"'.format(exe_path))
    
    elif command == 'close_cloudmusic':
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == 'cloudmusic.exe':
                do_system_cmd('taskkill /f /pid %s' % pid)
    elif command == 'exit_app':
        sys.exit(0)

# tong bu
mouse_thread_exist = False
lock_item = threading.Lock()
index = 0
base_distance = 20
seq = 0
dx = 0
dy = 0
def mouse_move_fun():
    global index,mouse_thread_exist
    # 添加自动停止，
    lock_item.acquire()
    mouse_thread_exist = True
    lock_item.release()
    while True:
        base_distance = 20
        x = dx * base_distance
        y = dy * base_distance
        # mouse.move(x,y,False,0.1)
        mouse.move(x, y, False, 0.001)
        index += 1
        if index - seq > 20:
            break
    lock_item.acquire()
    mouse_thread_exist = False
    lock_item.release()


def mouse_init():
    mouse_move_thread = threading.Thread(target=mouse_move_fun)
    mouse_move_thread.start()
    # mouse_move_thread.is_alive()


def mouse_control(command,args):
    #  解决鼠标移动问题
    global dx,dy,seq,index,base_distance
    global mouse_thread_exist
    if not args:
        base_distance = 20
    else:
        base_distance = int(args)
    lock_item.acquire()
    if not mouse_thread_exist:
        lock_item.release()
        mouse_init()
    else:
        lock_item.release()

    index = seq = 0
    # print(type(command))
    # print(command)
    relative_position = json.loads(command)
    dx = relative_position['dx']
    dy = relative_position['dy']


def keyboard_control(command,args):
    keyboard.press_and_release(command)


def input_msg(msg,args):
    pyperclip.copy(msg)
    keyboard_control('ctrl+v')


