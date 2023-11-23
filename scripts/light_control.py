import asyncio
import aiohttp
import subprocess
from miio import Device

ip_address = "设备ip地址"
token = "获取设备token"
model = "yeelink.light.bslamp2"
api_url = "https://填写你的api服务域名/api/get_light_status/"

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
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    # 启动异步轮询任务
    asyncio.run(poll_api())
