# Телеграм-бот в рамках кейса от Ростелекома
## О проекте
Вы можете найти бота в telegram по следующему имени:
@Samanter_bot

В данном боте реализованы два профиля - Пользователь и Администратор, присутствует возможность переключения между ними 
при успешной авторизации.

## Для разработчиков
Данный проект разрабатывается в среде `poetry` с использованием библиотеки pyTelegramBotAPI.

Для начала работы с проектом вам необходимо:


1. Установить `poetry`. Инструкцию по установке можно посмотреть здесь: (https://python-poetry.org/docs/).

2. Сделать форк git-репозитория с помощью следующей команды в терминале:
> git clone ...

3. Инициировать зависимости с помощью команды `poetry`:
> poetry install

4. Активировать виртуальное окружение:
> poetry shell

5. Выбрать интерпретатор виртуального окружения `poetry`
(Python 3.10.2 ('.venv': Poetry)) - должно указываться в строке выбранного интерпретатора

6. Чтобы удостовериться, что зависимости установлены верно, введите команду:
> pip list

Список с зависимостями должен выглядеть примерно так:
![Модули](/Sources/Package%20list.png)

7. Можно приступать к разработке! Если необходимо добавить новую библиотеку,
делайте это с помощью команды:
> poetry add (название библиотеки)

`Poetry` установит библиотеку и реализует все зависимости за вас

8. Средства тестирования и оценки качества кода уже внесены в групповую зависимость, о них беспокоиться не надо. Их список:
 
 - flake8 (анализатор качества и стиля кода)
 - mypy (статитеский анализатор типов)
 - pylint (оценка общего качества кода)
 - pytest (инструмент для осуществления тестов)