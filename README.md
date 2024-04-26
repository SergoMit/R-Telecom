# Телеграм-бот в рамках кейса от Ростелекома
## О проекте

### Введение
Вы можете найти бота в telegram по следующему имени:
@Samanter_bot

В данном боте реализованы два профиля - Пользователь и Администратор, присутствует возможность переключения между ними при успешной авторизации.

Пользователь может: 

- Просматривать состояние диска

- Извлекать необходимую информацию

Администратору доступны возможности:

- Просматривать состояние диска

- Загружать файлы с данными на Яндекс.Диск

- Удалять файлы с Яндекс.Диска

- Извлекать необходимую информацию

Учтите, что на Яндекс.Диске должен располагаться лишь 1 файл с данными! В противном случае неизбежны сбои при
работе бота.

### Пользовательский интерфейс

Основные способы взаимодействия пользователя с ботом:

- Команды

- Reply-кнопки

- Текстовый ввод

#### Команды

Как для Пользователя, так и Админстратора, представлен следующий универсальный набор команд:

! [Команды](/Sources/Команды.png)

- Команда `/start` позволяет как активировать, так и перезагружать
данного бота. Учтите, что при перезагрузке весь прогресс по обращениям
будет сброшен!

- Команда `/check_disk` проверяет подключение к Яндекс.Диску, а также сообщает
пользователю имена содержащихся на нём файлов и их количество. Рекомендуется
использовать данную команду для проверки диска перед запросом данных через чат-бот.

- Команда `/get_data` переводит пользователя в режим запроса к таблице, содержащейся на Яндекс.Диске, и выводит в чат данные по указанному запросу.

- Команда `/help `содержит всю необходимую информацию о чат-боте (Вы сейчас здесь).

- Команда `/quit` завершает текущую сессию с чат-ботом. Возобновить работу можно
с помощью /start.

Также существует команда `/admin`, но в меню она не выводится, поскольку пользователю о ней знать не нужно.
Её необходимо ввести вручную.

#### Кнопки

Также пользователь может взаимодействовать с ботом посредством кнопок.
Например, у Администратора существует собственная панель управления, недоступная пользователю (на фото лишь фрагмент панели Администратора):

! [Панель](/Sources/Панель.png)

#### Текстовый ввод
Текстовый ввод используется в нескольких случаях: 

1. При введении команды /admin (простому пользователю о ней знать необязательно)

2. При введении пароля в ходе авторизации

3. При введении названия региона в режиме запроса к данным

Пример:
! [Ввод](/Sources/Текстовый%20ввод.png)

При активации режимов авторизации, загрузки файлов или запроса к данным всплывает кнопка, которая позволяет покинуть данный режим. Учтите, что находясь к каком-либо из режимов, бот не сможет обработать посторонние команды, поэтому если вы случайно перешли в данный режим, то для обращения к другим возможностям бота, вам необходимо перевести бота в исходный режим, для этого необходимо нажать соответствующую всплывшую кнопку. 

Пример всплывающей кнопки:

! [Кнопка](/Sources/Кнопка.png)

## Работа с проектом (non-deploy)

В данном разделе описан алгоритм начала работы с телеграм-ботом для случая, когда он не развёрнут на хостинге.

NOTES:

Для работы с проектом склонируйте этот код через `git` на свой компьютер.

Проект создан с помощью `poetry`. Убедитесь, что система `poetry` у вас установлена. Инструкцию по установке можно посмотреть здесь: (https://python-poetry.org/docs/).

Порядок действий для реализации взаимодействия с программой:

1. Склонируйте данный проект из репозитория с помощью команды в терминале любой из удобных для вас сред разработки: 
> git clone https://github.com/SergoMit/R-Telecom.git

2. Запустите следующую команду в терминале среды разработки (убедитесь, что вы находитесь в корневой папке проекта — там, где лежит файл `pyproject.toml`):
> poetry install

3. После создания всех зависимостей введите следующую команду для активации виртуального окружения `poetry`:
> poetry shell

4. Далее вам необходимо создать файл .env в корневой папке проекта. В нём нужно создать переменные окружения со следующими
названиями:
>BOT_TOKEN

>YANDEX_TOKEN

>ADMIN_PASS

>DIRECTORY

`BOT_TOKEN` содержит в себе токен телеграм-бота RT_DataFinder. Размещение токенов в открытых удалённых репозиториях небезопасно, поэтому разработчик передаст его вам в индивидуальном порядке.

`YANDEX_TOKEN` содержит в себе токен диска, с которым будет взаимодействовать бот. О том, как создать токен для вашего Яндекс.Диска, подробно рассказывается в этой статье: (https://prog-time.ru/course/api-yandeks-disk-php-1-podklyuchenie-i-nastrojka-prilozheniya/).

`ADMIN_PASS` содержит пароль, вводимый пользователем для аутентификации. В файле .env вы можете задать свой пароль, на скрине ниже он приведен в качестве примера. Пароль должен содержать только цифры и латинские буквы.

`DIRECTORY` содержит в себе имя директории, располагающейся на Яндекс.Диске. По умолчанию это `/RostelecomBot`. Если таковая на 
Яндекс.Диске отсутствует, то при первой загрузке файла бот создаст её автоматически.

В итоге файл .env должен выглядеть примерно так:

! [env-Файл](/Sources/Файл%20env.png)

5. Для запуска программы в виртуальной среде перейдите в каталог rostelecom_bot и воспользуйтесь командой:
> poetry run python main.py
