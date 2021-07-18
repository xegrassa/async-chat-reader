# Асинхронное подключение к чату Девман

### Установка
Клонируйте проект и установите зависимости командами ниже. Для работы требуется версия Python 3.8 + 
```
git clone https://github.com/xegrassa/async-chat-reader.git
cd async-chat-reader
pip install -r requirements.txt
```

после запускайте скрипт для [Чтения](#чтения-чата) или [Отправки сообщения](#отправка-сообщения-в-чат). Пример установки в разделе [Video](#video)
***
### Чтение чата
Для чтения и логирования чата Девман запустите скрипт: 

`python listen-minechat.py`

```
usage: listen_minechat.py [-h] [--host HOST] [--port PORT] [--history HISTORY]

Скрипт для чтения и логирования чата Devman

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        IP адресс чата 
  --port PORT        port чата 
  --history HISTORY  Лог файл чата 
```
***
### Отправка сообщения в чат
Для отправки сообщения в чат Девман запустите скрипт: 

`python write_to_minechat.py HELLO_DEVMAN`

```
usage: write_to_minechat.py [-h] [--host HOST] [--port PORT] [--token TOKEN] [--name NAME] message

Скрипт для отправки сообщения в чат Devman

positional arguments:
  message        Сообщение для чата

optional arguments:
  -h, --help     show this help message and exit
  --host HOST    IP адресс чата [env var: HOST]
  --port PORT    port чата [env var: WRITE_PORT]
  --token TOKEN  Токен [env var: TOKEN]
  --name NAME    Имя пользователя для регистрации
```
***
### .env
Для удобства параметры ниже можно добавить в окружение или передать через *.env* файл созданный в корне приложения
```
HOST = 192.168.0.1
LISTEN_PORT = 1234
WRITE_PORT = 1234
HISTORY = ./minechat.log
TOKEN = abc123qwe456
```
***
### Requirements
- [Python 3.8+](https://www.python.org/)
- aiofiles==0.7.0
- ConfigArgParse==1.5.1
- python-dotenv==0.18.0
***
### Video
[![asciicast](https://asciinema.org/a/426002.svg)](https://asciinema.org/a/426002)