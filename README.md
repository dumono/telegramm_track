# CatBot

CatBot - это бот для Telegram, который умеет присылать фотографии котиков

### Установка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл settings.py и создайте в нем переменные:
    ```
    API_KEY = "Ключ вашего бота"
    PROXY_URL = "URL socks5-прокси"
    PROXY_USERNAME = "Username для авторизации на прокси"
    PROXY_PASSWORD = "Пароль  для авторизации на прокси"
    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']