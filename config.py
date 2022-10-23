# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/10/12 16:22
#   @File : config.py
#   @des: 
# ================================================================
import sys
import winreg
import logging
import os
from util.RegTool import RegTool
import time

log_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'log')
if not os.path.exists(log_path):
    os.makedirs(log_path)
file_name = os.path.join(log_path,
                         '{}_{}.log'.format(os.path.basename(sys.argv[0])[:-3], time.strftime("%Y%m%d_%H%M%S")))
print(file_name)
logging.basicConfig(filename=file_name, filemode='w', level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

APP_NAME = sys.argv[0]
if not APP_NAME.endswith('.exe'):
    APP_NAME += '.exe'
# 文件名


# print(APP_NAME,os.getcwd(),os.path.split(os.path.realpath(__file__))[0])

DEFAULT_CONFIGS = {
    'port': 5002,  # 端口
    'password': '123456',  # 密码
    'auto_start': True,  # 开机自启
    'mouse_base_distance': 10,  # 鼠标移动间隔
    'has_admin': True,  # 是否具有管理员权限
    # 'install_path': os.path.join(os.environ['USERPROFILE'],'AndroidRemoteControlServer\\arcs.exe'),
    'log_path': os.path.join(os.path.split(os.path.realpath(__file__))[0],'log'),
    'install_path': os.path.join(os.path.split(os.path.realpath(__file__))[0],sys.argv[0]),
    'chrome_path': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'driver_path': os.path.join(os.path.split(os.path.realpath(__file__))[0],r'lib\chromedriver.exe'),
    'chrome_driver_download_url': 'https://registry.npmmirror.com/-/binary/chromedriver/{chrome_version}/chromedriver_win32.zip',

}

REG_SUB_KEY = r'Software\AndroidRemoteControlServer\Config'
reg = RegTool(winreg.HKEY_CURRENT_USER,REG_SUB_KEY)
if not reg.existKey():
    # 创建注册表键
    reg.createKey()
    # 查询谷歌浏览器安装位置
    chrome_path = RegTool(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe').queryValue('')
    DEFAULT_CONFIGS['chrome_path'] = chrome_path
    # 获取网易云安装位置

    # 设置默认值
    for key,value in DEFAULT_CONFIGS.items():
        reg.setValue(key,value)

else:
    for key in DEFAULT_CONFIGS.keys():
        value = reg.queryValue(key)
        if value is not None:
            DEFAULT_CONFIGS[key] = value
    logging.info('配置查询完成')

# print('配置文件初始化完成')