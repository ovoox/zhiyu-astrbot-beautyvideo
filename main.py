from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import base64

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 加密的API地址，避免直接暴露
        self.encrypted_api = "aHR0cDovL2FwaS5vY29hLmNuL2FwaS9iZWF1dHl2aWRlby5waHA="
        self.session = aiohttp.ClientSession()

    async def terminate(self):
        await self.session.close()

    def _decrypt_api(self):
        """解密API接口地址"""
        return base64.b64decode(self.encrypted_api).decode()

    @filter.command("美女视频", alias={"视频", "美女"})
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            # 使用解密后的真实API地址
            real_api_url = self._decrypt_api()
            
            async with self.session.get(real_api_url) as response:
                if response.status == 200:
                    video_component = Video.fromURL(real_api_url)
                    yield event.chain_result([video_component])
                else:
                    yield event.plain_result("视频获取失败，请稍后重试")

        except Exception:
            yield event.plain_result("视频加载异常，请稍后重试")
