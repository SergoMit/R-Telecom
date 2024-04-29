"""
Данный файл содержит наборы фраз, выдаваемые
чат-ботом
"""

greeting_usr = """
Вы Пользователь 🧑‍💻
"""

greeting_adm = """
Вы Администратор 🛠
"""

usr_phrase = """
Вы Пользователь!🧑‍💻

🟢 Вам разрешается:

- Извлекать необходимую информацию 📖
"""

adm_phrase = """
Вы Администратор! 🛠

🟢 Вам разрешается: 

- Загружать/удалять файлы с данными на Яндекс.Диск 💾

- Запрашивать и очищать лог-файл с ошибками 📝

- Извлекать необходимую информацию 📖

- Переходить в режим пользователя 🧑‍💻
"""

phrase_help = """
📌 В меню чат-бота представлены следующие команды:

/start 🚀

/check_disk 🩺

/get_data 📖

/help 🛟

/quit 🚪

- Команда /start позволяет как активировать, так и перезагружать
данного бота. Учтите, что при перезагрузке весь прогресс по обращениям
будет сброшен!

- Команда /check_disk проверяет подключение к Яндекс.Диску, а также сообщает
пользователю имена содержащихся на нём файлов и их количество. Рекомендуется
использовать данную команду для проверки диска перед запросом данных через чат-бот.

- Команда /get_data переводит пользователя в режим запроса к таблице, содержащейся на 
Яндекс.Диске, и выводит в чат данные по указанному запросу.

- Команда /help содержит всю необходимую информацию о чат-боте (Вы сейчас здесь).

- Команда /quit завершает текущую сессию с чат-ботом. Возобновить работу можно
с помощью /start.
"""

bye_phrase = """
До свидания!\n\rДля возобновления работы воспользутесь /start
"""
