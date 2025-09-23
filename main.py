from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import time

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "http://api.ocoa.cn/api/beautyvideo.php"
        self.session = aiohttp.ClientSession()
        self.last_request_time = 0
        self.cooldown = 5  # 5秒冷却时间

    async def terminate(self):
        await self.session.close()

    @filter.command("美女视频", alias={"视频", "美女"})
    async def get_beauty_video(self, event: AstrMessageEvent):
        # 检查冷却时间
        current_time = time.time()
        if current_time - self.last_request_time < self.cooldown:
            remaining = self.cooldown - (current_time - self.last_request_time)
            yield event.plain_result(f"请求过于频繁，请等待 {remaining:.1f} 秒后再试")
            return
        
        self.last_request_time = current_time

        try:
            async with self.session.get(self.api_url) as response:
                if response.status != 200:
                    yield event.plain_result(f"请求失败：状态码{response.status}")
                    return
                
                # 直接使用API地址作为视频源
                video_component = Video.fromURL(self.api_url)
                message_chain = [video_component]
                yield event.chain_result(message_chain)

        except aiohttp.ClientError as e:
            yield event.plain_result(f"网络请求出错：{str(e)}")
        except Exception as e:
            yield event.plain_result(f"发生未知错误：{str(e)}")
            import traceback
            traceback.print_exc()
