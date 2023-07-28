from contextlib import contextmanager


# contextmanager - превращает генераторную функцию в контекстный менеджер
@contextmanager
def custom_open(filename: str, mode='w'):
    """Генераторная функция для открытия файлов"""
    # Всё что до yield - контекстный менеджер использует как метод __enter__, что после - как метод __exit__

    # Открываем файловый объект при помощи функции open
    file_obj = open(filename, mode)
    yield file_obj
    file_obj.close()


with custom_open('file.txt') as file:
    file.write('Python best')
