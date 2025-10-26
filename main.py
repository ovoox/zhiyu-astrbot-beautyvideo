from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Video 
import aiohttp

@register("beauty_video", "美女视频", "获取美女视频的插件", "2.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "https://tx.2cnm.cn/video-api.php"  # 直接使用明文接口地址
        self.session = aiohttp.ClientSession()

    async def terminate(self):
        await self.session.close()

    @filter.regex(r"^[/]?(美女视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            # 直接使用接口地址作为视频源
            video_component = Video.fromURL(self.api_url)
            yield event.chain_result([video_component])
        except Exception:
            yield event.plain_result("视频异常，请稍后重试")
