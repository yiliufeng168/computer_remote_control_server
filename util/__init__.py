# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/8/20 21:21
#   @File : __init__.py.py
#   @des: 
# ================================================================
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def do_system_cmd(command):
    subprocess.Popen(command,shell=True)