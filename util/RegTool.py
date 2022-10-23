# -*- coding: utf-8 -*-
# ===============================================================
#   @author: 易流锋
#   @date: 2022/10/13 9:45
#   @File : RegTool.py
#   @des: 
# ================================================================
import logging
import winreg
import win32con


class RegTool:
    def __init__(self,key,sub_key):
        self.key = key
        self.sub_key = sub_key


    def existKey(self):
        try:
            key = winreg.OpenKeyEx(self.key,self.sub_key,access=winreg.KEY_ALL_ACCESS)
            key.Close()
            return True
        except FileNotFoundError as e:
            return False

    def createKey(self):
        try:
            winreg.CreateKeyEx(self.key,self.sub_key,0,access=winreg.KEY_ALL_ACCESS)
            return True
        except Exception as e:
            logging.error('注册表键创建失败')
            logging.exception(e)
            return False

    def deleteKey(self):
        winreg.DeleteKeyEx(self.key,self.sub_key,access=winreg.KEY_ALL_ACCESS,reserved=0)

    def queryValue(self,name):
        try:
            key = winreg.OpenKeyEx(self.key, self.sub_key, access=winreg.KEY_ALL_ACCESS)
            value = winreg.QueryValueEx(key,name)

            key.Close()
            if type(value[0]) == bytes:
                return bool(value[0])
            return value[0]
        except FileNotFoundError as e:
            return None

    def setValue(self, name, value, _type=None):
        """

        :param name:
        :param value:
        :param _type: 若None，则自动选择类型
        :return:
        """
        try:
            key = winreg.OpenKeyEx(self.key, self.sub_key, access=winreg.KEY_ALL_ACCESS)
            if _type:
                __type = _type
            elif type(value) == str:
                __type = winreg.REG_SZ
            elif type(value) == int:
                __type = winreg.REG_DWORD
            elif type(value) == bool:
                __type = winreg.REG_BINARY
                value = value.to_bytes(1,'little')
            else:
                return False
            winreg.SetValueEx(key,name,0,__type,value)
            key.Close()
            return True
        except FileNotFoundError as e:
            return False

    def deleteValue(self,name):
        try:
            key = winreg.OpenKeyEx(self.key, self.sub_key, access=winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key,name)
            key.Close()
            return True
        except FileNotFoundError as e:
            return False

    def openKey(self,):
        try:
            key = winreg.OpenKeyEx(self.key, self.sub_key, access=winreg.KEY_ALL_ACCESS)
            return key
        except FileNotFoundError as e:
            return None

    def closeKey(self,key):
        key.Close()


if __name__ == '__main__':
    reg = RegTool(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Run\aa')
    reg.deleteKey()
    # print(reg.setValue('test',True))
    # print(reg.queryValue('test'))
    #
    # print(reg.deleteValue('test'))