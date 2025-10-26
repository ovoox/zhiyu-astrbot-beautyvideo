from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import base64

@register("beauty_video", "美女视频", "获取美女视频的插件", "2.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 新接口地址 https://tx.2cnm.cn/video-api.php 的 Base64 编码
        self.encrypted_api = "aHR0cHM6Ly90eC4yY25tLmNuL3ZpZGVvLWFwaS5waHA="
        self.session = aiohttp.ClientSession()

    async def terminate(self):
        await self.session.close()

    def _decrypt_api(self):
        return base64.b64decode(self.encrypted_api).decode()

    @filter.regex(r"^[/]?(美女视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            real_api_url = self._decrypt_api()
            
            async with self.session.get(real_api_url) as response:
                if response.status == 200:
                    # 注意：这里假设接口直接返回视频文件（如 .mp4）
                    # 如果接口返回的是 JSON（例如 {"url": "xxx.mp4"}），则需要解析 JSON
                    video_component = Video.fromURL(real_api_url)
                    yield event.chain_result([video_component])
                else:
                    yield event.plain_result("获取视频失败，请稍后重试")

        except Exception as e:
            # 可选：记录异常 e 用于调试
            yield event.plain_result("视频异常，请稍后重试")
