import asyncio
import aiohttp
from miio.device import Device

class CatFeeder:
    def __init__(self, ip, token):
        self.device = Device(ip=ip, token=token)
        self.previous_index = None

    async def action_cat(self, number):
        # 使用 send 方法调用动作
        print('喂食数量', number)
        self.device.send("set_properties", [{'did': 'MYDID', 'siid': 2, 'piid': 5, 'code': 0, 'value': number}])
        action_params = {'did': 'MYDID', 'siid': 2, 'aiid': 1, 'in': []}
        self.device.send('action', action_params)

    async def poll_api(self, api_url):
        while True:
            try:
                # 发起 GET 请求获取接口数据
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url, ssl=False) as response:
                        if response.status == 200:
                            # 解析 JSON 数据
                            data = await response.json()

                            # 获取当前的 index 值
                            current_index = data.get("index")

                            # 判断 index 是否改变
                            if current_index != self.previous_index:
                                # 喂食
                                number = int(data.get("number", "0"))
                                print(f"Index 改变，出食物，number: {number}, index: {current_index}")
                                await self.action_cat(number)

                                # 更新上一次的 index
                                self.previous_index = current_index
                            else:
                                print("Index 未改变，不执行动作")
                        else:
                            print("请求失败:", response.status)
            except Exception as e:
                print("发生异常:", str(e))

            # 间隔一定时间再次发起请求
            await asyncio.sleep(0.1)  # 推荐使用较长的时间间隔

if __name__ == "__main__":
    # 定义设备的相关信息
    device_info = {'ip': '', 'token': ''}
    
    # 创建CatFeeder对象
    cat_feeder = CatFeeder(ip=device_info['ip'], token=device_info['token'])
    
    # 定义接口URL
    api_url = "https://m.h5in.net/gpts_dev/api/get_cat_status/"
    
    # 启动异步轮询任务
    asyncio.run(cat_feeder.poll_api(api_url))
