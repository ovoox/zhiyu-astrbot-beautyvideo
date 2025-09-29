from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import base64
import asyncio
import hashlib
import hmac
from cryptography.fernet import Fernet
import time

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self._encrypted_data = self._super_encrypt("http://api.ocoa.cn/api/beautyvideo.php")
        self.session = aiohttp.ClientSession()
        
    async def terminate(self):
        await self.session.close()
    
    def _super_encrypt(self, text):
        key1 = base64.urlsafe_b64encode(hashlib.sha256("key1_seed".encode()).digest())
        fernet1 = Fernet(key1)
        layer1 = fernet1.encrypt(text.encode())
        
        key2 = base64.urlsafe_b64encode(hashlib.sha256("key2_seed".encode()).digest())
        fernet2 = Fernet(key2)
        layer2 = fernet2.encrypt(layer1)
        
        b64_encoded = base64.b64encode(layer2)
        
       混淆_key = "SUPER_SECURE_KEY_2024"
       混淆_result = ""
        for i, char in enumerate(b64_encoded.decode()):
            key_char = 混淆_key[i % len(混淆_key)]
            混淆_result += chr((ord(char) + ord(key_char)) % 128)
        
        final_encoded = base64.b85encode(混淆_result.encode())
        return final_encoded.decode()
    
    def _super_decrypt(self):
        try:
            layer4 = base64.b85decode(self._encrypted_data.encode()).decode()
            
            混淆_key = "SUPER_SECURE_KEY_2024"
            deobfuscated = ""
            for i, char in enumerate(layer4):
                key_char = 混淆_key[i % len(混淆_key)]
                deobfuscated += chr((ord(char) - ord(key_char)) % 128)
            
            layer2 = base64.b64decode(deobfuscated.encode())
            
            key2 = base64.urlsafe_b64encode(hashlib.sha256("key2_seed".encode()).digest())
            fernet2 = Fernet(key2)
            layer1 = fernet2.decrypt(layer2)
            
            key1 = base64.urlsafe_b64encode(hashlib.sha256("key1_seed".encode()).digest())
            fernet1 = Fernet(key1)
            original = fernet1.decrypt(layer1).decode()
            
            return original
        except Exception:
            raise ValueError("decrypt failed")
    
    async def _auto_delete(self, msg_id, delay=60):
        await asyncio.sleep(delay)
        try:
            if hasattr(self.context, 'delete_message'):
                await self.context.delete_message(msg_id)
        except Exception:
            pass
    
    @filter.regex(r"^[/]?(美女视频|看视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            real_url = self._super_decrypt()
            
            async with self.session.get(real_url) as response:
                if response.status == 200:
                    video = Video.fromURL(real_url)
                    result = await event.reply([video])
                    
                    msg_id = None
                    if hasattr(result, 'message_id'):
                        msg_id = result.message_id
                    elif hasattr(result, 'id'):
                        msg_id = result.id
                    elif isinstance(result, dict) and 'message_id' in result:
                        msg_id = result['message_id']
                    
                    if msg_id:
                        asyncio.create_task(self._auto_delete(msg_id, 60))
                        
                else:
                    result = await event.reply("获取视频失败 请稍后重试")
                    
        except Exception:
            result = await event.reply("视频异常 请稍后重试")
