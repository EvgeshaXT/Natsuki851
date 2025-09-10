import disnake
from disnake.ext import commands
from disnake.ext.commands import MissingPermissions
from disnake import Option, OptionType

class ClearCog(commands.Cog):
    """Модуль, добавляющий слеш-команду очистки сообщений в канале"""
    def __init__(self, bot):
        self.bot = bot

    # Функция для получения правильной формы слова
    def get_message_word(self, count):
        # 1, 21, 31, 41, 51...
        if count % 10 == 1 and count % 100 != 11:
            return "сообщение"
        
        # 2, 3, 4, 22, 23...
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "сообщения"
        
        # Остальные случаи
        else:
            return "сообщений"

    # Отдельный обработчик ошибки при отсутствии прав администратора
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, MissingPermissions):
            await inter.response.send_message("> У вас недостаточно прав для выполнения этой команды ❌")
        else:
            # Передаём другие ошибки для обработки по умолчанию
            raise error

    # Создаём слеш-команду
    @commands.has_permissions(administrator=True)
    @commands.slash_command(
        name="clear",
        description="Удалить последние сообщения в чате",
        # Добавляем параметр количества сообщений, которых нужно удалить
        options=[
            Option(
                name="number_of_messages",
                description="Количество сообщений для удаления (1 - 100)",
                type=OptionType.integer,
                required=True, # Делаем параметр обязательным
                min_value=1,
                max_value=100
            )
        ]
    )

    # inter - аналог ctx в префиксных командах
    async def clear(
        self,
        inter: disnake.ApplicationCommandInteraction,
        number_of_messages: int
    ):
        try:
            # Отправляем временный ответ
            await inter.response.send_message("Удаление сообщений ...")

            # Получаем сообщение бота для добавления его в исключения из удаления
            bot_message = await inter.original_response()
            # Для этого используем check функцию
            def check(message):
                return message.id != bot_message.id

            # Удаляем сообщения
            deleted = await inter.channel.purge(
                limit=number_of_messages,
                check=check,
                before=bot_message
            )

            count = len(deleted)
            word_form = self.get_message_word(count)
        
            # Редактируем сообщение, которое было отправлено ранее
            await inter.edit_original_response(f"```ansi\n[2;34m{count}[0m {word_form} было удалено.```", delete_after=3) # Используется ansi, чтобы сделать фрагмент текста цветным

        # Обработка общих HTTP-ошибок со стороны Discord API
        except disnake.HTTPException as error:
            await inter.edit_original_response(f"Произошла ошибка при удалении сообщений (код: {error.status}).")
            print(f"❌ cogs/clear.py: HTTP ошибка при удалении сообщений: код {error.status}) - {error}")

        # Общий обработчик для непредвиденных ошибок
        except Exception as error:
            await inter.edit_original_response("Произошла непредвиденная ошибка при удалении сообщений.")
            print(f"❌ cogs/clear.py: Непредвиденная ошибка при попытке удалить сообщения: {error}")

        
def setup(bot):
    bot.add_cog(ClearCog(bot))