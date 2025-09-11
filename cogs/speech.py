from disnake.ext import commands
import time
import asyncio
from collections import defaultdict

class SpeechCog(commands.Cog):
    """Модуль для имитации общения бота с пользователями"""
    def __init__(self, bot):
        self.bot = bot
        self.last_reply_time = defaultdict(float) # Специальный словарь для отслеживания времени последнего ответа в каждом канале

    async def good_night(self, message):
        """Спокойной ночи!"""
        if "спокойной ночи" in message.content.lower():
            # Получаем время и ID канала, в котором было отправлено сообщение
            current_time = time.time()
            channel_id = message.channel.id

            # Бот будет отправлять такое сообщение максимум раз в 5 минут во избежании флуда
            if current_time - self.last_reply_time[channel_id] >= 300:
                self.last_reply_time[channel_id] = current_time

                # Бот "печатает" и задержка в 3 секунды для имитации человечности
                async with message.channel.typing():
                    await asyncio.sleep(3)
                    await message.channel.send("Спокойной ночи!")


    # Используется простой декоратор слушателя событий
    @commands.Cog.listener()
    # Событие при получении сообщения
    async def on_message(self, message):
        """Обработчик входящих сообщений"""
        await self.good_night(message)

def setup(bot):
    bot.add_cog(SpeechCog(bot))