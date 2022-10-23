# 电脑遥控器服务器端
## 简要说明
本程序为电脑遥控器服务端，用户可以使用遥控器对安装了电脑遥控器服务端的主机进行简单控制。

安卓电脑遥控器客户端: <https://github.com/yiliufeng168/computer_remote_control_client>

注意：本程序使用过程中需要获取管理员权限，请勿在公共网络上使用。

## 启动
```shell
app.exe  --start
```
首次启动会自动下载谷歌浏览器驱动
## 显示配置信息
```shell
app.exe --config 
```

## 修改配置信息
可以对端口密码等信息进行修改
```shell
app.exe --set password 123456
app.exe --set port 5003
```


## 安装
安装可省，主要是将该程序设置为开机自启动
```shell
app.exe --install
```

## 卸载
删除开机自启动和创建的注册表
```shell
app.exe --uninstall
```



[comment]: <> (## 取消开机启动)

[comment]: <> (## 需求文档)

[comment]: <> (1. 一方面需加密通信，另一方面需保证通信低延迟)

[comment]: <> (2. 支持基本的鼠标键盘事件,鼠标移动可调速)

[comment]: <> (3. 支持shell)

[comment]: <> (4. 支持复杂操作)

[comment]: <> (5. 预定义一些常用命令)

[comment]: <> (6. 支持安装卸载、设置用户密码、开机启动等功能)

[comment]: <> (7. 可测试通信是否成功)

[comment]: <> (8. 关于加密通信是否有必要，以及支持动态密码)

[comment]: <> (9. 广播通知局域网在线)

[comment]: <> (10. 指定位置点击)

[comment]: <> (11. 鼠标移动采用单独线程，并可自动停止。)

[comment]: <> (12. 能够接受配置更新。即：手机端修改配置并保存后，电脑端能够根据版本)

[comment]: <> (13. 让一切操作自动化。)

[comment]: <> (14. 对于桌面上的软件，可以将快捷方式发送到手机，并在手机上显示图标。（桌面快捷方式图标提取）)

[comment]: <> (15. 提供自动打开功能。如一键打开电视)

[comment]: <> (16. 提供自动安装功能)

[comment]: <> (17. 支持软件的一键卸载功能)

[comment]: <> (18. 支持自动更新)


[comment]: <> (## 1. 定义数据接收格式)

[comment]: <> (1. 接收json类型数据)

[comment]: <> (2. 使用MD5&#40;密码&#41;+时间戳对数据进行签名)

[comment]: <> (   考虑时间同步)
   
[comment]: <> (3. json数据结构)

[comment]: <> (```json)

[comment]: <> ({)

[comment]: <> (   "type": "command_list",)

[comment]: <> (   "content":[)

[comment]: <> (      {)

[comment]: <> (         "type": "predefined",)

[comment]: <> (         "command": "volume_down",)

[comment]: <> (         "args": "")

[comment]: <> (      },)

[comment]: <> (      {)

[comment]: <> (         "type": "predefined",)

[comment]: <> (         "command": "volume_down",)

[comment]: <> (         "args": "")

[comment]: <> (      })

[comment]: <> (   ],)

[comment]: <> (   "check_sum": "32weimd5")

[comment]: <> (})

[comment]: <> (```)

[comment]: <> (4. 添加install uninstall)

[comment]: <> (- install时指定密码,复制软件，添加注册表)

[comment]: <> (- uninstall ，删除软件，删除注册表)

[comment]: <> (- passwd , 修改密码)

[comment]: <> (5. 添加计划任务)

[comment]: <> (```shell)

[comment]: <> (schtasks /create /ru system /sc onstart /tn control_server /tr "\"C:\Program Files &#40;x86&#41;\app\app.exe\" -p 123456")

[comment]: <> (```)

[comment]: <> (6. 删除计划任务)

[comment]: <> (```shell)

[comment]: <> (schtasks /delete /f /tn control_server)

[comment]: <> (```)

[comment]: <> (# android 控制端)

[comment]: <> (## 1. 需求添加)

[comment]: <> (1. 指令集需添加关联主机id)

[comment]: <> (2. 指令保存页面需添加指令名称输入框)

[comment]: <> (3. 自定义命令按钮添加长按编辑删除)

[comment]: <> (4. 编辑指令页面需检查载入上一页传入的数据,返回后需重载数据)

[comment]: <> (5. 页面优化)

[comment]: <> (6. 考虑添加身份认证或数据签名)