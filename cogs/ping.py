from disnake.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == f"<@{self.bot.user.id}>":
            await message.reply("Я тут.")
            return

def setup(bot):
    bot.add_cog(PingCog(bot))