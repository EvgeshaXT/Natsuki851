import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

# Функция загрузки когов
def load_cogs(bot):
    """Загружает все коги из папки cogs, кроме указанных в IGNORE_FILES из .env"""
    # Формат: IGNORE_FILES = 'file1.py, file2.py, ...'
    ignore_str = os.getenv('IGNORE_FILES', '')
    ignore = [cog for cog in ignore_str.split(', ')] if ignore_str else []
    
    loaded_cogs = []
    errors = []

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename not in ignore:
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                loaded_cogs.append(filename)
                print(f"✅ Загружен ког: {filename}")
            except Exception as error:
                errors.append(error)
                print(f"❌ Ошибка загрузки кога {filename}: {error}")
        elif filename in ignore:
            print(f"🔴 Проигнорирован ког: {filename}")

    return loaded_cogs, errors

# Проверяет существование кога в директории ./cogs
def existing_cogs(cog_name):
    return os.path.exists(f'./cogs/{cog_name}.py')

# Функция для получения последнего сообщения бота в канале
async def get_bot_last_message(channel):
    async for message in channel.history(limit=10):
        if message.author.bot:
            return message
    return None

# Функция загрузки кога
async def load_cog(bot, ctx, cog_name: str):
    """Загружает указанный ког"""
    last_bot_msg = await get_bot_last_message(ctx.channel)
    try:
        bot.load_extension(f'cogs.{cog_name}')
        if "не загружен. Загружаю... ⚙️" in last_bot_msg.content:
            await last_bot_msg.reply(f"> Ког **{cog_name}** был успешно загружен ✅")
        else:
            await ctx.reply(f"> Ког **{cog_name}** был успешно загружен ✅")
        print(f"✅ Ког {cog_name} загружен по команде")
    except commands.ExtensionAlreadyLoaded:
        await ctx.reply(f"> Ког **{cog_name}** уже загружен! ⚠️")
    except commands.ExtensionNotFound:
        await ctx.reply(f"> Ког **{cog_name}** не найден ❌")
    except Exception as error:
        await ctx.reply(f"> Ошибка при загрузке кога **{cog_name}**: {error} ❌")
        print(f"❌ Ошибка при загрузки кога {cog_name}: {error}")

# Функция перезагрузки кога
async def reload_cog(bot, ctx, cog_name: str):
    """Перезагружает указанный ког (загружает если не был загружен)"""
    try:
        bot.reload_extension(f'cogs.{cog_name}')
        await ctx.reply(f"> Ког **{cog_name}** был успешно перезагружен 🔄")
        print(f"🔄 Ког {cog_name} перезагружен по команде")
    except commands.ExtensionNotLoaded:
        if existing_cogs(cog_name):
            await ctx.reply(f"> Ког **{cog_name}** не загружен. Загружаю... ⚙️")
            await load_cog(bot, ctx, cog_name)
        else:
            await ctx.reply(f"> Ког **{cog_name}** не найден ❌")
    except Exception as error:
        await ctx.reply(f"> Ошибка при перезагрузке кога **{cog_name}**: {error} ❌")
        print(f"❌ Ошибка при перезагрузки кога {cog_name}: {error}")

# Функция выгрузки кога
async def unload_cog(bot, ctx, cog_name: str):
    """Выгружает указанный ког"""
    try:
        bot.unload_extension(f'cogs.{cog_name}')
        await ctx.reply(f"> Ког **{cog_name}** выгружен. 🔴")
        print(f"🔴 Ког {cog_name} выгружен по команде")
    except commands.ExtensionNotLoaded:
        if not existing_cogs(cog_name):
            await ctx.reply(f"> Ког **{cog_name}** не найден ❌")
        else:
            await ctx.reply(f"> Ког **{cog_name}** не был загружен ⚠️")
    except Exception as error:
        await ctx.reply(f"> Ошибка при выгружении кога **{cog_name}**: {error} ❌")
        print(f"❌ Ошибка при выгрузки кога {cog_name}: {error}")

# Функция списка когов
async def list_cogs(bot, ctx):
    """Показывает список и статус всех когов (загружены/не загружены)"""
    loaded_cogs = []
    unloaded_cogs = []

    # Перебираем все коги
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            unloaded_cogs.append(filename[:-3])

    # Получаем список загруженных когов
    for cog_name in unloaded_cogs:
        if f'cogs.{cog_name}' in bot.extensions:
            loaded_cogs.append(cog_name)

    # Формируем сообщение
    message = "**📦 Список всех моих когов:**\n"
    message += "```\n"
    for cog in unloaded_cogs:
        status = "✅" if cog in loaded_cogs else "❌"
        message += f"{status} {cog}\n"
    message += "```\n"
    message += "✅ - загружены; ❌ - не загружены"

    await ctx.reply(message)

# Функция настройки управления когами
def setup_cog_commands(bot):
    """Добавляет команды управления когами"""
    # Загружает указанный ког
    @bot.command(name='load')
    @commands.has_permissions(administrator=True)
    async def _(ctx, cog_name: str):
        await load_cog(bot, ctx, cog_name)

    # Перезагружает указанный ког
    @bot.command(name='reload')
    @commands.has_permissions(administrator=True)
    async def _(ctx, cog_name: str):
        await reload_cog(bot, ctx, cog_name)

    # Выгружает указанный ког
    @bot.command(name='unload')
    @commands.has_permissions(administrator=True)
    async def _(ctx, cog_name: str):
        await unload_cog(bot, ctx, cog_name)

    # Показывает список всех когов
    @bot.command(name='cogs')
    @commands.has_permissions(administrator=True)
    async def _(ctx):
        await list_cogs(bot, ctx)

# Основная функция
def main():
    """Основная функция инициализации и запуска бота"""
    load_dotenv()
    
    # Инициализация бота и загрузка когов
    bot = commands.Bot(command_prefix=commands.when_mentioned, intents=disnake.Intents.all(), help_command=None)
    load_cogs(bot)
    setup_cog_commands(bot)

    @bot.event
    async def on_ready():
        print(f"✅ Бот {bot.user.name} готов к работе!")

    # Обработчик ошибок
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("> У вас недостаточно прав для выполнения этой команды ❌")
        elif isinstance(error, commands.CommandNotFound):
            # Выбирайте из личных предпочтений:
            # await ctx.reply("> Указанная команда не найдена ❌")
            pass
        else:
            print(f"Произошла ошибка: {error}")
    
    # Запуск бота
    bot.run(os.getenv('TOKEN'))

if __name__ == "__main__":
    main()