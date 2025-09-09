import disnake
from disnake.ext import commands

class AvatarCog(commands.Cog):
    """Модуль, который добавляет слеш-команду для получения аватарки пользователя"""
    def __init__(self, bot):
        self.bot = bot

    # Создаём слеш-команду
    @commands.slash_command(
        name="avatar",
        description="Показать аватар пользователя"
    )

    # inter - аналог ctx в префиксных командах
    async def avatar(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.User = commands.Param(description="Пользователь, у которого нужно получить аватар")
    ):
        
        # Создаём эмбед
        embed = disnake.Embed(
            title = f"Аватар пользователя: {user.display_name}",
            color = disnake.Color.darker_gray()
        )

        # Добавляем маленькую надпись с именем пользователя
        embed.set_author(
            name=f"{user.name}",
            icon_url=user.display_avatar.url
        )

        # Добавляем изображение в эмбед
        embed.set_image(url=user.display_avatar.url)

        # Отправляем эмбед
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(AvatarCog(bot))