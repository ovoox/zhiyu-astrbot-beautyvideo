from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import base64
import asyncio
import hashlib
import hmac
from cryptography.fernet import Fernet

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.encrypted_api = "gAAAAABn0VzL8X6qHj5Kk9mMpQrT3sVwYxZcFdEaBbGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzA=="
        self.session = aiohttp.ClientSession()
    async def terminate(self):
        await self.session.close()
    def _decrypt_api(self):
        key = base64.urlsafe_b64encode(hashlib.sha256("super_secret_key_2024".encode()).digest())
        fernet = Fernet(key)
        layer1 = fernet.decrypt(self.encrypted_api.encode())
        layer2 = base64.b85decode(layer1)
        layer3 = base64.b64decode(layer2)
       混淆_key = "ASTROBOT_ULTRA_SECURE"
        deobfuscated = ""
        for i, char in enumerate(layer3.decode()):
            key_char = 混淆_key[i % len(混淆_key)]
            deobfuscated += chr((ord(char) - ord(key_char)) % 128)
        real_api = base64.b64decode(deobfuscated).decode()
        return real_api
    async def _delete_after_60s(self, message_id):
        await asyncio.sleep(60)
        try:
            if hasattr(self.context, 'delete_message'):
                await self.context.delete_message(message_id)
        except Exception:
            pass
    @filter.regex(r"^[/]?(美女视频|看视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            real_api_url = self._decrypt_api()
            
            async with self.session.get(real_api_url) as response:
                if response.status == 200:
                    video_component = Video.fromURL(real_api_url)
                    result = await event.reply([video_component])
                    
                    message_id = None
                    if hasattr(result, 'message_id'):
                        message_id = result.message_id
                    elif hasattr(result, 'id'):
                        message_id = result.id
                    elif isinstance(result, dict) and 'message_id' in result:
                        message_id = result['message_id']
                    
                    if message_id:
                        asyncio.create_task(self._delete_after_60s(message_id))
                else:
                    yield event.plain_result("获取视频失败 请稍后重试")

        except Exception:
            yield event.plain_result("视频异常 请稍后重试")
