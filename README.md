# Телеграм бот для умным ассистентом

## Технологический стек

- Python 3.13.5
- Telegram Bot API
- SQLite3
- Dotenv
- PyTelegramBotAPI

## Быстрый старт

### 1.Создаем вирутуальное окружение

```bash
python -m venv venv
```

### 2. Запускаем виртуальное окружение

На Windows:

```bash
venv\Scripts\Activate.ps1
```

На сервере, Linux или MacOS:

```bash
source venv/bin/activate
```

Если вы видите ошибку после попытки активировать виртуальное окружение, выполните следующую команду:

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Устанавливаем зависимости

```bash
pip install -r requirements.txt
```

### 4. Создаем файл .env и заполняем переменные окружения

```bash
cp .env.example .env
```

### 5. Запускаем бота

```bash
python bot.py
```


