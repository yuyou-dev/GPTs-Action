import asyncio
import aiohttp
import subprocess
from miio import Device

ip_address = ""
token = ""
model = "yeelink.light.bslamp2"
# 获取灯状态的地址，api接口
api_url = "https://m.h5in.net/gpts_dev/api/get_light_status/"  
# 创建Yeelight设备实例
yeelight_device = Device(ip_address, token)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def build_yeelight_command(action, brightness=None, rgb=None):
    # 构建Yeelight命令的基本部分
    base_cmd = f"miiocli yeelight --model {model} --ip {ip_address} --token {token}"
    
    # 根据不同的操作构建完整的命令
    if action == 'on':
        return f"{base_cmd} {action}"
    elif action == 'off':
        return f"{base_cmd} {action}"
    elif action == 'set_brightness':
        return f"{base_cmd} {action} {brightness}" if brightness is not None else ""
    elif action == 'set_rgb':
        return f"{base_cmd} {action} {rgb}" if rgb is not None else ""

def map_color_to_rgb(color):
    # 将颜色映射到RGB值
    return '255 0 0' if color == 'red' else '255 255 255'

async def control_yeelight(on, brightness=None, rgb=None):
    # 构建不同操作的Yeelight命令
    on_cmd = build_yeelight_command(on)
    brightness_cmd = build_yeelight_command('set_brightness', brightness=brightness)
    rgb_cmd = build_yeelight_command('set_rgb', rgb=rgb)

    # 执行Yeelight命令
    run_command(on_cmd)
    if on == 'on':
        run_command(brightness_cmd)
        run_command(rgb_cmd)
        print("灯已打开并调节亮度。")

async def poll_api():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        light_status = data.get("light_on")
                        color = data.get("color")
                        rgb = map_color_to_rgb(color)

                        if light_status == "1":
                            light_value = data.get("light_value")
                            # 控制Yeelight灯的开关和亮度
                            await control_yeelight('on', brightness=int(light_value), rgb=str(rgb))
                        elif light_status == "2":
                            # 控制Yeelight灯的开关
                            await control_yeelight('off')
                        else:
                            print("未知状态:", light_status)
                    else:
                        print("请求失败:", response.status)
        except Exception as e:
            print("发生异常:", str(e))

        await asyncio.sleep(0.1)  # 间隔一分钟再次发起请求

if __name__ == "__main__":
    asyncio.run(poll_api())
