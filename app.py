# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/8/27 13:21
#   @File : app.py.py
#   @des: 
# ================================================================

import argparse
import logging
import os
import socketserver
import sys
import time
import psutil
import win32api
import win32con
from Server import MyServer
from config import DEFAULT_CONFIGS, reg, APP_NAME
from util.RegTool import RegTool
from util import is_admin
from util.ChromeBrowser import update_driver



def update_config(key, value):
    try:
        if key in DEFAULT_CONFIGS.keys():
            if type(DEFAULT_CONFIGS[key]) == bool:
                if value.lower() == 'true':
                    reg.setValue(key, True)
                else:
                    reg.setValue(key, False)
            elif type(DEFAULT_CONFIGS[key]) == str:
                reg.setValue(key, value)
            elif type(type(DEFAULT_CONFIGS[key])) == int:
                reg.setValue(key, int(value))
        else:
            print('不支持配置: {}'.format(key))
        print('ok')
    except Exception as e:
        print('参数错误')
        print(e)


def show_config():
    for key, value in DEFAULT_CONFIGS.items():
        print('{}\t{}'.format(key, value))


def exist_app():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == APP_NAME:
            if pid != os.getpid():
                print(pid, os.getpid(),)

                input()
                print('已有相同程序运行')
                return True
    return False


def start_app():
    # 启动时要检查是否已有启动的app
    print('正在启动')
    if exist_app():
        return None
    update_driver()
    port = DEFAULT_CONFIGS['port']
    s = socketserver.ThreadingUDPServer(('0.0.0.0', port), MyServer)
    s.serve_forever()


def stop_app():
    # 检查是否有已存在的服务
    pids = psutil.pids()
    print(APP_NAME)
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == APP_NAME:
            print(p.name(),APP_NAME)
            # if p.exe() == DEFAULT_CONFIGS['install_path']:
            if pid != os.getpid():
                os.system('taskkill /f /pid %s' % pid)


def install():
    # 判断是否具有管理员权限
    print('正在安装。。。')
    if not is_admin():
        win32api.MessageBox(0, '请以管理员身份运行', '警告', win32con.MB_ICONWARNING)
        return None

    # copy_cmd = 'copy /Y {} "{}"'.format(fn, DEFAULT_CONFIGS['install_path'])
    # print(copy_cmd)
    # os.system(copy_cmd)
    # 创建计划任务
    mktasks_cmd = 'schtasks /create /F /RL HIGHEST /sc onstart /tn arcs /tr "\\"{install_path}\\" --start"'
    print(mktasks_cmd.format(install_path=DEFAULT_CONFIGS['install_path']))
    os.system(mktasks_cmd.format(install_path=DEFAULT_CONFIGS['install_path']))
    # 配置环境变量
    # os.system('setx /m arcs "{}"'.format(install_dir))
    # ev = [
    #     {'key':win32con.HKEY_LOCAL_MACHINE,'sub_key':r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'},
    #     {'key': win32con.HKEY_LOCAL_MACHINE,
    #      'sub_key': r'SYSTEM\ControlSet001\Control\Session Manager\Environment'},
    #     {'key': win32con.HKEY_CURRENT_USER,
    #      'sub_key': r'Environment'},
    # ]
    # for item in ev:
    #     env_reg = RegTool(item['key'],item['sub_key'])
    #     path_list = [i for i in env_reg.queryValue('Path').split(';') if i]
    #     print(path_list)
    #
    #     if install_dir not in path_list:
    #         path_list.append(install_dir)
    #         env_reg.setValue('Path',';'.join(path_list),win32con.REG_EXPAND_SZ)
    print('安装成功')


def uninstall():
    if not is_admin():
        win32api.MessageBox(0, '请以管理员身份运行', '警告', win32con.MB_ICONWARNING)
        return None
    untask_cmd = 'schtasks /delete /f /tn arcs'
    # install_dir = os.path.dirname(DEFAULT_CONFIGS['install_path'])
    # if os.path.exists(DEFAULT_CONFIGS['install_path']):
    #     os.remove(DEFAULT_CONFIGS['install_path'])
    #     os.removedirs(os.path.dirname(DEFAULT_CONFIGS['install_path']))
    os.system(untask_cmd)
    reg.deleteKey()

    print('卸载成功')
    # ev = [
    #     {'key': win32con.HKEY_LOCAL_MACHINE,
    #      'sub_key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'},
    #     {'key': win32con.HKEY_LOCAL_MACHINE,
    #      'sub_key': r'SYSTEM\ControlSet001\Control\Session Manager\Environment'},
    #     {'key': win32con.HKEY_CURRENT_USER,
    #      'sub_key': r'Environment'},
    # ]
    # for item in ev:
    #     env_reg = RegTool(item['key'], item['sub_key'])
    #     path_list = [i for i in env_reg.queryValue('Path').split(';') if i]
    #
    #     if install_dir in path_list:
    #         path_list.remove(install_dir)
    #         env_reg.setValue('Path', ';'.join(path_list), win32con.REG_EXPAND_SZ)


def main():
    parse = argparse.ArgumentParser("电脑遥控器服务端")
    parse.add_argument('--set', help='设置服务器配置', nargs=2)
    parse.add_argument('--config', help='显示服务器配置,可以通过set进行修改', action='store_true')
    parse.add_argument('--start', help='启动服务器', action='store_true')
    parse.add_argument('--stop', help='停止服务器', action='store_true')
    parse.add_argument('--install', help='安装服务器', action='store_true')
    parse.add_argument('--uninstall', help='卸载服务器', action='store_true')

    args = parse.parse_args()
    if args.set:
        update_config(args.set[0], args.set[1])
    elif args.config:
        show_config()
    elif args.start:
        start_app()
    elif args.stop:
        stop_app()
    elif args.install:
        install()
    elif args.uninstall:
        uninstall()


if __name__ == '__main__':
    main()
