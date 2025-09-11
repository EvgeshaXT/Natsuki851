from disnake.ext import commands

class PingCog(commands.Cog):
    """Данный модуль создан исключительно для проверки работоспособности бота"""
    def __init__(self, bot):
        self.bot = bot

    # Используется простой декоратор слушателя событий
    @commands.Cog.listener()
    # Событие при получении сообщения
    async def on_message(self, message):
        if message.content == f"<@{self.bot.user.id}>":
            # Бот "печатает" для имитации человечности
            async with message.channel.typing():
                await message.reply("Я тут.")
            return

def setup(bot):
    bot.add_cog(PingCog(bot))