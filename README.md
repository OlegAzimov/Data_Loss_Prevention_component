1. Установите необходимые зависимости:

- Убедитесь, что у вас установлен Python версии 3.7 или выше.

2. Получите токен бота:

- Создайте нового бота через телеграм-бота @BotFather, выбирайте бота с галочкой.

- Скопируйте токен вашего бота.

3. Запустите сервис:
- Перейдите в папку Data_Loss_Prevention, нажмите правой кнопкой мыши на файл bot_run и выберите изменить (можно использовать любой текстовый редактор):
---------------------

#set TOKEN=<ваш токен> 

----------------------
- В этом коде, замените <ваш токен> на фактический токен вашего бота (без <>).

- Закройте с сохранением

4. Использование сервиса:
- Для запуска вашего бота запустите bot_run.bat.

- Добавьте бота в групповой чат или напишите ему в личные сообщения.

- В групповом чате бот будет автоматически проверять все сообщения на наличие потенциально важной информации и удалит сообщение, если оно содержит соответствующий шаблон регулярного выражения, и в группе ответит автору сообщения, что его сообщение было удалено.

- В личных сообщениях с ботом вы можете использовать команды:
- /add_pattern - добавить новый шаблон регулярного выражения.
- /remove_pattern - удалить существующий шаблон регулярного выражения.

5. Админка:

- В файле admin_id.txt укажите ваш идентификатор чата в Телеграме (без <>). Это ваш id, его можно узнать c помощью телеграм бота @getmyid_bot. После указания id бот будет считать вас администратором. В личном чате с ботом напишите команду /start, и бот предоставит вам доступ к командам /add_pattern, /remove_pattern и доступ к информации о сообщениях удаленных из чата.