import disnake
from disnake.ext import commands, tasks
import os, glob

class ETS2Cog(commands.Cog):
    """Данный модуль автоматически отправляет новые скриншоты из игры Euro Track Simulator 2"""
    def __init__(self, bot):
        self.bot = bot
        # Путь к папке со скриншотами
        self.screenshot_path = os.getenv('SCREENSHOT_PATH')
        # ID канала для отправки новых скриншотов
        self.channel_id = int(os.getenv('CHANNEL_ID'))
        # Переменная для управления отправкой существующих файлов при запуске модуля
        self.send_existing_on_startup = os.getenv('SEND_EXISTING', 'False').lower() == 'true' # Меняйте значение только в .env!
        # Файл для хранения списка уже отправленных скриншотов
        self.sent_files = 'data/sent_files.txt'
        # Множество для хранения путей отправленных файлов
        self.set_sent_files = set()

        # Инициализация кога
        self.create_sent_files()
        self.load_sent_files()
        if self.send_existing_on_startup == False:
            self.mark_existing_files() # Помечаем существующие файлы как отправленные (self.send_existing_on_startup)
        self.check_files.start() # Запуск работы модуля

    def cog_unload(self):
        """Принудительная остановка задачи при перезагрузке или выгрузки кога"""
        self.check_files.cancel()

    def create_sent_files(self):
        """Создаёт файл data/sent_files.txt (далее --> "файл для хранения") в случае, если он ещё не создан"""
        try:
            # Создание папки, если она ещё не создана
            if not os.path.exists('data'):
                os.makedirs('data')
                print("✅ cogs/ets2.py: Была создана директория: ./data/")

            # Создание файла data/sent_files.txt
            if not os.path.exists(self.sent_files):
                with open(self.sent_files, 'w'):
                    pass
                print(f"✅ cogs/ets2.py: Был создан файл: {self.sent_files}")

        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка при создании файла {self.sent_files}: {error}")

    def load_sent_files(self):
        """Загружает список уже отправленных файлов из файла для хранения"""
        try:
            with open(self.sent_files, 'r') as files: # Открывает файл в режиме чтения
                self.set_sent_files = set(line.strip() for line in files) # Создаёт множество, .strip очищает наше множество от \n
        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка при загрузке отправленных файлов: {error}")          

    def save_sent_files(self):
        """Сохраняет список отправленных скриншотов в файл для хранения"""
        try:
            # Проверяет наличие файла. Если он отсутствует, создаёт его вновь
            if not os.path.exists(self.sent_files):
                return self.create_sent_files()
            
            with open(self.sent_files, 'w') as files: # Открывает файл в режиме редактирования и переписывает его
                for file in self.set_sent_files:
                    files.write(f"{file}\n")

        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка при сохранении отправленных файлов: {error}")

    def mark_existing_files(self):
        """Помечает все существующие файлы как отправленные во избежание флуда при запуске"""
        try:
            # Получаем все существующие файлы .png
            existing_files = glob.glob(os.path.join(self.screenshot_path, '*.png'))

            # Добавляем их в множество отправленных файлов
            for file_path in existing_files:
                self.set_sent_files.add(file_path)

            # Сохраняем обновлённый список
            self.save_sent_files()
            print(f"cogs/ets2.py: Все существующие файлы помечены как отправленные. Всего файлов: {len(existing_files)}")

        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка при помечивании существующих файлов: {error}")

    def get_new_files(self):
        """Возвращает список новых скриншотов, которые ещё не были отправлены"""
        try:
            all_files = []
            new_files = []

            # Получаем все файлы .png в папке скриншотов
            all_files.extend(glob.glob(os.path.join(self.screenshot_path, '*.png')))

            # Фильтрируем только новые файлы с проверкой размера
            for file in all_files:
                if file not in self.set_sent_files:
                    try:
                        # Проверяем размер файла (больше 1 КБ) на случай, если файл ещё не успел полностью создаться
                        if os.path.getsize(file) > 1024:
                            new_files.append(file)

                    except OSError as error:
                        print("❌ cogs/ets2.py: Ошибка при получении размера файла: {error}")

            return new_files
        
        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка при поиске новых скриншотов: {error}")
            return []

    @tasks.loop(seconds=10)
    async def check_files(self):
        """Каждые 10 секунд проверяет "папку" на наличие новых файлов и отправляет их"""
        try:
            channel = self.bot.get_channel(self.channel_id)
            new_files = self.get_new_files()

            # Отправка каждого нового файла в дискорд
            for file_path in new_files:
                try:
                    with open(file_path, 'rb') as file_object: # rb (сокр. от read binary) - чтение файла в бинарном режиме (изображение - это бинарный файл)
                        file = disnake.File(file_object, filename = os.path.basename(file_path)) # disnake.File(Путь к файлу, имя файла)
                        await channel.send(file=file)
                    print(f"cogs/ets2.py: Отправлен скриншот: {os.path.basename(file_path)}")
                    
                    # Добавляем в отправленные
                    self.set_sent_files.add(file_path)
                    self.save_sent_files()
                
                except Exception as error:
                    print(f"❌ cogs/ets2.py: Ошибка при отправке файла {file_path}: {error}")
            
        except Exception as error:
            print(f"❌ cogs/ets2.py: Ошибка в функции проверки файлов: {error}")
    
    @check_files.before_loop
    async def before_check_files(self):
        """Ожидает готовность бота перед началом работы"""
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(ETS2Cog(bot))