# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/10/13 8:48
#   @File : ChromeBrowser.py
#   @des: 
# ================================================================
import json
import logging
import os
import requests
import psutil
import win32api
import zipfile
from config import DEFAULT_CONFIGS
from tqdm import tqdm
from util import do_system_cmd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver = None


def getFileVersion(file_name):
    """
    获取文件版本号
    :param file_name:
    :return:
    """
    info = win32api.GetFileVersionInfo(file_name, os.sep)
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = '%d.%d.%d.%d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    return version


def getChromedriverVersion(driver_path):
    if os.path.exists(driver_path):
        cmd_result = os.popen(driver_path + '  -v')
        current_driver_version_info = cmd_result.read()
        return current_driver_version_info.split()[1]
    else:
        return ''


def getNewVersionDriverUrl(chrome_version):
    vs = chrome_version.split('.')[0]
    res = requests.get('http://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}'.format(vs))
    if not res:
        logging.error('最新驱动下载地址获取异常')
        return None
    return DEFAULT_CONFIGS['chrome_driver_download_url'].format(chrome_version=res.text)


def download_from_url(url,dst):
    dst_path = os.path.dirname(dst)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    response = requests.get(url, stream=True)
    with tqdm.wrapattr(open(dst, "wb"), "write",
                       miniters=1, desc=url.split('/')[-1],
                       total=int(response.headers.get('content-length', 0))) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)


def unzip(file_path):
    base_path = os.path.dirname(file_path)
    zip_file = zipfile.ZipFile(file_path)
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f, base_path)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存


def update_driver():
    # 1. 版本检查，决定是否更新
    #  - 1 获取浏览器版本
    chrome_version = getFileVersion(DEFAULT_CONFIGS['chrome_path'])
    logging.info("当前chrome浏览器版本:{}".format(chrome_version))
    #  - 2 获取驱动版本
    chromedriver_version = getChromedriverVersion(DEFAULT_CONFIGS['driver_path'])
    if chromedriver_version == '':
        logging.info('Chrome浏览器驱动未安装')
    else:
        logging.info('chromedriver.exe驱动版本:{}'.format(chromedriver_version))

    if chromedriver_version.split('.')[0:3] != chrome_version.split('.')[0:3]:
        logging.info("chrome驱动正在更新")
        # 分3部
        # 1. 获取对应驱动最新版本地址
        new_version_driver_download_url = getNewVersionDriverUrl(chrome_version)
        # 2. 下载驱动
        dst = DEFAULT_CONFIGS['driver_path'].replace('.exe','.zip')
        download_from_url(new_version_driver_download_url,dst)
        # 3. 解压
        unzip(dst)
        # 4. 删除压缩包
        os.remove(dst)
    else:
        logging.info('驱动无需更新')


def start_debug_chrome():
    """
    启动调试模式的chrome
    :return:
    """
    # 1. 判断是否已启动
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            if p.name() == 'chrome.exe':
                if '--remote-debugging-port=9222' in p.cmdline():
                    logging.info(p.cmdline())
                    logging.info('chrome调试模式以启动')
                    return True
        except:
            pass
    else:
        # do_system_cmd('"{}" --remote-debugging-port=9222 --user-data-dir="{}"'.format(chrome_path,
        #                                                                               os.path.join(os.getcwd(),user_data_dir)))
        do_system_cmd('"{}" --remote-debugging-port=9222'.format(DEFAULT_CONFIGS['chrome_path'],))
        return True


def debug_chrome():
    global driver
    # user_data_dir = ".\\lib\\user_data_dir"
    # if not os.path.exists(user_data_dir):
    #     os.makedirs(user_data_dir)
    start_debug_chrome()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # driver就是当前浏览器窗口
    driver = webdriver.Chrome(service=Service(DEFAULT_CONFIGS['driver_path'],), options=chrome_options)
    return driver


def init_chrome(func):
    def inner(*args, **kwargs):
        if not driver:
            debug_chrome()
        else:
            try:
                driver.current_url
            except Exception as e:
                debug_chrome()
        func(*args, **kwargs)
    return inner


@init_chrome
def open_url(url):
    switch_to_visible_window()
    driver.get(url)


def get_driver():
    return driver


@init_chrome
def click_element(xpath):
    # 要点，当前显示在最前的页面
    switch_to_visible_window()
    driver.find_element(By.XPATH,xpath).click()


@init_chrome
def close():
    driver.quit()


def switch_to_visible_window():
    try:
        while driver.execute_script('return document.hidden'):
            switch_to_next_handle()
    except:
        driver.switch_to.window(driver.window_handles[0])


def input_text(xpath,text):
    switch_to_visible_window()
    driver.find_element(By.XPATH, xpath).send_keys(text)


def switch_to_next_handle():
    size = len(driver.window_handles)
    index = driver.window_handles.index(driver.current_window_handle)
    next_index = (index+1) % size
    driver.switch_to.window(driver.window_handles[next_index])


def create_tab():
    driver.switch_to.new_window('tab')



def browser(command,args):
    if command == 'open_url':
        open_url(args)
    elif command == 'click_by_xpath':
        click_element(args)
    elif command == 'quit':
        close()
    elif command == 'input_text':
        # 添加输入文本功能
        args = json.loads(args)
        input_text(**args)
    elif command == 'next_tab':
        switch_to_next_handle()
    elif command == 'create_tab':
        create_tab()
    return None

