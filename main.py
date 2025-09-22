import os
import time
from astrbot.api.all import *

BEAUTY_VIDEO_API = "http://api.ocoa.cn/api/beautyvideo.php"
COOLDOWN_TIME = 5  # 冷却时间5秒

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.last_query_time = 0  # 记录上次查询时间
    
    async def _can_request(self):
        """检查是否可以发起请求"""
        current_time = time.time()
        if current_time - self.last_query_time < COOLDOWN_TIME:
            remaining = COOLDOWN_TIME - (current_time - self.last_query_time)
            return False, f"请求过于频繁，请等待 {remaining:.1f} 秒后再试"
        self.last_query_time = current_time
        return True, None
    
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群聊消息处理器"""
        msg = event.message_str.strip()
        
        if msg == "美女视频":
            # 检查冷却时间
            can_request, error = await self._can_request()
            if not can_request:
                yield event.chain_result([Plain(text=error)])
                return
            
            # 直接使用API地址作为视频源
            video = Comp.Video.fromURL(url=BEAUTY_VIDEO_API)
            yield event.chain_result([video])
        
        elif msg == "视频帮助":
            help_text = """美女视频插件使用说明：
指令：美女视频 - 获取随机美女视频
注意：每次请求后有5秒冷却时间"""
            yield event.chain_result([Plain(text=help_text)])
