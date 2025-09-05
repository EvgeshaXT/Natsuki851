# Natsuki851 - Дискорд бот на Disnake с поддержкой системы когов

## Установка

1. Клонирование репозитория:
```git clone https://github.com/EvgeshaXT/Natsuki851.git```

2. Переход в директорию Natsuki851:
```cd Natsuki851```

3. Создание виртуального окружения:
```python -m venv venv```

4. Активация виртуального окружения:
```venv/bin/activate```

6. Установка зависимостей
``'pip install -r requirements.txt'``

7. Настройка .env файла
Создайте .env файл
``'touch .env'``

Отредактируй .env файл, добавив свой TOKEN
```TOKEN='ваш_токен_здесь'```

Также вы можете добавить игнорируемые коги, которые будут добавлены в исключения при запуске бота. Может быть полезно при разработке когов
```IGNORE_FILES=example_cog.py, test_module.py```


## Использование

Запуск бота (не забудьте активирировать виртуальное окружение перед запуском!:
```python main.py```

Внимание! Перед использованием убедительная просьба обратить внимание на то, что в проекте за основу префикса взят именно пинг бота! ```(command_prefix=commands.when_mentioned)```
Данный префикс будет считаться стандартом для данного проекта

Команды управления когами:
@Natsuki851 load <cog_name> - Загрузить ког
@Natsuki851 reload <cog_name> - Перезагрузить ког
@Natsuki851 unload <cog_name> - Выгрузить ког
@Natsuki851 cogs - Показать список всех когов


## Структура проекта
Natsuki851/
├── cogs/                # Директория с модулями
├── main.py              # Основной файл бота
├── .env                 # Файл окружения
├── requirements.txt     # Зависимости
└── README.md            # Этот файл


## Разработка
Для создания своего собственного кога для бота, Вам необходимо создать файл в папке cogs/ с расширением .py

Используй шаблон:
```python
import disnake
from disnake.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Всё работает!")

def setup(bot):
    bot.add_cog(MyCog(bot))```
