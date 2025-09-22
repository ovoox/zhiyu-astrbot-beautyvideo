import os
import aiohttp
import time
from astrbot.api.all import *

PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_beautyvideo')
BEAUTY_VIDEO_API = "http://api.ocoa.cn/api/beautyvideo.php"
COOLDOWN_TIME = 5  # 冷却时间5秒

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.last_query_time = 0  # 记录上次查询时间
    
    async def _get_beauty_video(self):
        """获取美女视频"""
        try:
            current_time = time.time()
            if current_time - self.last_query_time < COOLDOWN_TIME:
                remaining = COOLDOWN_TIME - (current_time - self.last_query_time)
                return None, f"请求过于频繁，请等待 {remaining:.1f} 秒后再试"
            
            self.last_query_time = current_time
            
            async with aiohttp.ClientSession() as session:
                async with session.get(BEAUTY_VIDEO_API) as response:
                    if response.status == 200:
                        # 尝试读取为文本（URL），如果失败则可能是二进制数据
                        try:
                            video_url = await response.text()
                            # 简单验证是否是URL
                            if video_url.startswith(('http://', 'https://')):
                                return video_url, None
                            else:
                                return None, "API返回的数据不是有效的视频URL"
                        except UnicodeDecodeError:
                            # 如果是二进制数据，可能需要保存为文件
                            return None, "API返回的是二进制数据，请检查API文档确认返回格式"
                    else:
                        return None, f"获取视频失败，状态码：{response.status}"
        except Exception as e:
            return None, f"获取视频时发生错误: {str(e)}"
    
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群聊消息处理器"""
        msg = event.message_str.strip()
        
        # 美女视频指令
        if msg == "美女视频":
            video_url, error = await self._get_beauty_video()
            if error:
                yield event.chain_result([Plain(text=error)])
            else:
                # 创建视频消息并返回
                video = Comp.Video.fromURL(url=video_url)
                yield event.chain_result([video])
        
        # 帮助指令
        elif msg == "视频帮助":
            help_text = """美女视频插件使用说明：
指令：美女视频 - 获取随机美女视频
注意：每次请求后有5秒冷却时间"""
            yield event.chain_result([Plain(text=help_text)])
