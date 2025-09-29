from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import base64
import asyncio

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.encrypted_api = "aHR0cDovL2FwaS5vY29hLmNuL2FwaS9iZWF1dHl2aWRlby5waHA="
        self.session = aiohttp.ClientSession()
    
    async def terminate(self):
        await self.session.close()
    
    def _decrypt_api(self):
        return base64.b64decode(self.encrypted_api).decode()
    
    async def _recall_message(self, message_id: str, delay: int = 60):
        await asyncio.sleep(delay)
        try:
            await self.context.recall_message(message_id)
        except Exception:
            pass
    
    @filter.regex(r"^[/]?(美女视频|看视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            real_api_url = self._decrypt_api()
            
            async with self.session.get(real_api_url) as response:
                if response.status == 200:
                    video_component = Video.fromURL(real_api_url)
                    result = event.chain_result([video_component])
                    message_id = yield result
                    
                    if message_id:
                        asyncio.create_task(self._recall_message(message_id, 60))
                else:
                    yield event.plain_result("获取视频失败 请稍后重试")

        except Exception:
            yield event.plain_result("视频异常 请稍后重试")
