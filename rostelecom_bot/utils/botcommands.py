from aiogram.types.bot_command import BotCommand

user_commands = [
    BotCommand(command="check_disk", description="Проверка диска"),
    BotCommand(command="get_data", description="Извлечь данные"),
    BotCommand(command="admin", description="Администратор"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="quit", description="Выход")
]

admin_commands = [
    BotCommand(command="check_disk", description="Проверка диска"),
    BotCommand(command="get_data", description="Извлечь данные"),
    BotCommand(command="user", description="Пользователь"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="quit", description="Выход")
]

wait_pass_cmd = [
    BotCommand(command="cancel", description="Покинуть авторизацию")
]

wait_file_cmd = [
    BotCommand(command="cancel_upload", description="Покинуть загрузку")
]