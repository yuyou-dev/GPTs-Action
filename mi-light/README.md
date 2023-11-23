# 小米智能管家python开发

相关参考链接如下：

[https://github.com/cxr1/py-miio-for-Xiaomi-Mi-Smart-WiFi-Socket](https://github.com/cxr1/py-miio-for-Xiaomi-Mi-Smart-WiFi-Socket)

[https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor)

https://github.com/rytilahti/python-miio/

小米python官网：[https://python-miio.readthedocs.io/en/latest/index.html#installation](https://python-miio.readthedocs.io/en/latest/index.html#installation)

色温等具体值的查看：[https://www.cnblogs.com/ff888/p/16977114.html](https://www.cnblogs.com/ff888/p/16977114.html)

只需要运行 
```
source myenv/bin/activate

python3 token_extractor.py

python3 light_control_v2.py
```

创建虚拟环境

```bash
python3 -m venv myenv

source myenv/bin/activate
```

## 一、获取设备token

安装压缩包并解压

```bash
wget [https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor/releases/latest/download/token_extractor.zip](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor/releases/latest/download/token_extractor.zip)
unzip token_extractor.zip
cd token_extractor
```

```bash
pip3 install -r requirements.txt
```

现在小米的miio更新了，用新的安装方式安装

```bash
pip install python-miio
pip3 install aiohttp
```

然后运行如下代码，选择cn, 输入账户密码，即可获得，这一步不要用魔法哦

```bash
python3 token_extractor.py
```

## 二、使用

先写一个简单的控制开灯的脚本

```bash
from miio import Device

plug = Device("你的设备ip地址", "你的设备tooken")
#打开
plug.send("set_properties", [{'did': 'MYDID', 'siid': 2, 'piid': 1, 'value': True}])
#关闭
plug.send("set_properties", [{'did': 'MYDID', 'siid': 2, 'piid': 1, 'value': False}])
```

进阶，使用远程代码异步调用

```bash
import time
import requests
from miio import Device

# Xiaomi设备的IP地址和token
device_ip = ""
device_token = ""

# 接口URL
api_url = "https://你的API服务域名/api/get_light_status/"

# 创建Xiaomi设备实例
plug = Device(device_ip, device_token)

def control_light(value):
    # 控制灯的开关
    plug.send("set_properties", [{'did': 'MYDID', 'siid': 2, 'piid': 1, 'value': value}])

def poll_api():
    while True:
        # 发起GET请求获取接口数据
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            
            # 获取灯的状态
            light_status = data.get("light_on", "0")
            
            # 根据状态控制灯的开关
            if light_status == "1":
                print("开灯")
                control_light(True)
            elif light_status == "2":
                print("关灯")
                control_light(False)
            else:
                print("未知状态:", light_status)
        else:
            print("请求失败:", response.status_code)
        
        # 间隔一定时间再次发起请求
        time.sleep(0.2)
if __name__ == "__main__":
    # 启动轮询
    poll_api()
```

再次进阶，加入色温等值。这些值如何查看的呢？

第一步：安装miio,我们已经安装过了

第二步：在mac终端输入下面的 代码,查看您的型号，复制下来

```bash
miiocli -d device --ip xxx.xxx.xxx --token 您的token值 info
```

第三步：查看您的设备：在这个网址搜索您的型号，例如：urn:miot-spec-v2:device:light:0000A001:yeelink-lamp27:1

[http://miot-spec.org/miot-spec-v2/instances?status=al](https://miot-spec.org/miot-spec-v2/instances?status=all)

第四步：复制刚才的型号到[https://miot-spec.org/miot-spec-v2/instance?type=](https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:light:0000A001:yeelink-lamp27:1)‘刚才复制的链接’ 打开链接：[https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:light:0000A001:yeelink-lamp27:1](https://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:light:0000A001:yeelink-lamp27:1) 。这一步您将看到设备规格的未格式化 JSON 文本

第五步：粘贴到json文本格式化程序更容易阅读 [http://json.parser.online.fr/](http://json.parser.online.fr/)

![Untitled](%E5%B0%8F%E7%B1%B3%E6%99%BA%E8%83%BD%E7%AE%A1%E5%AE%B6python%E5%BC%80%E5%8F%91%20b96f9ad11be24db7b53857300cbd9fbe/Untitled.png)

```bash
#加入亮度
import asyncio
import aiohttp
from miio import Device

# Xiaomi设备的IP地址和token
device_ip = "填写设备ip"
device_token = "填写设备token"

# 接口URL
api_url = "https://填写你的API服务域名/api/get_light_status/"

# 创建Xiaomi设备实例
plug = Device(device_ip, device_token)

async def control_light(value, brightness=None):
    properties = [{'did': 'MYDID', 'siid': 2, 'piid': 1, 'value': value}]
    
    # 如果有亮度值，则替换掉原有的开关控制
    if brightness is not None:
        properties = [{'did': 'MYDID', 'siid': 2, 'piid': 2, 'code': 0, 'value': brightness}]

    # 控制灯的开关和亮度
    await plug.send("set_properties", properties)

async def poll_api():
    while True:
        try:
            # 发起 GET 请求获取接口数据
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, ssl=False) as response:
                    if response.status == 200:
                        # 解析 JSON 响应
                        data = await response.json()

                        # 获取灯的状态
                        light_status = data.get("light_on", "0")
                        
                        if light_status == "1":
                            # 获取亮度值
                            light_value = data.get("light_value")
                            print("开灯，亮度:", light_value)

                            # 控制灯的亮度
                            await control_light(True, brightness=int(light_value))
                        elif light_status == "2":
                            print("关灯")

                            # 控制灯的开关
                            await control_light(False)
                        else:
                            print("未知状态:", light_status)
                    else:
                        print("请求失败:", response.status)
        except Exception as e:
            print("发生异常:", str(e))

        # 间隔一定时间再次发起请求
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # 启动异步轮询任务
    asyncio.run(poll_api())
```

有的报错{'code': -9999, 'message': 'user ack timeout'} 版本较低怎么办？

先通过—help查看我们想要的设备yeelight 的具体型号yeelink.light.bslamp2  里面有哪些内容 

```bash
miiocli yeelight --model yeelink.light.bslamp2 --ip xxx --token xxx --help
```

然后找出我们需要的运行

![Untitled](%E5%B0%8F%E7%B1%B3%E6%99%BA%E8%83%BD%E7%AE%A1%E5%AE%B6python%E5%BC%80%E5%8F%91%20b96f9ad11be24db7b53857300cbd9fbe/Untitled%201.png)

```bash
miiocli yeelight --model yeelink.light.bslamp2 --ip xx.xx.xx.xx --token xxx on
```

行得通 ，把上面的代码替换为⬇️

```bash
import asyncio
import aiohttp
import subprocess
from miio import Device

ip_address = "xxx"
token = "xxx"
model = "yeelink.light.bslamp2"
api_url = "https://你的API服务域名/api/get_light_status/"

# 创建Yeelight设备实例
yeelight_device = Device(ip_address, token)

async def control_yeelight(on, brightness=None):
    on_cmd = f"miiocli yeelight --model {model} --ip {ip_address} --token {token} {'on' if on else 'off'}"
    brightness_cmd = f"miiocli yeelight --model {model} --ip {ip_address} --token {token} set_brightness {brightness}" if brightness is not None else ""

    # 使用subprocess运行命令
    try:
        subprocess.run(on_cmd, shell=True, check=True)
        if brightness_cmd:
            subprocess.run(brightness_cmd, shell=True, check=True)
        print("灯已打开并调节亮度。")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

async def poll_api():
    while True:
        try:
            # 发起 GET 请求获取接口数据
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, ssl=False) as response:
                    if response.status == 200:
                        # 解析 JSON 响应
                        data = await response.json()

                        # 获取灯的状态
                        light_status = data.get("light_on", "0")
                        
                        if light_status == "1":
                            # 获取亮度值
                            light_value = data.get("light_value")
                            print("开灯，亮度:", light_value)

                            # 控制Yeelight灯的开关和亮度
                            await control_yeelight(True, brightness=int(light_value))
                        elif light_status == "2":
                            print("关灯")

                            # 控制Yeelight灯的开关
                            await control_yeelight(False)
                        else:
                            print("未知状态:", light_status)
                    else:
                        print("请求失败:", response.status)
        except Exception as e:
            print("发生异常:", str(e))

        # 间隔一定时间再次发起请求
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # 启动异步轮询任务
    asyncio.run(poll_api())
