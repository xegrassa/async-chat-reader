# Асинхронное подключение к чату Девман

## Чтение чата

Чтобы читать чат Девман запустите скрипт: 

`python3 listen-minechat.py --host 192.168.0.1 --port 5001 --history ~/minechat.history`

```
usage: listen_minechat.py [-h] [--host HOST] [--port PORT] [--history HISTORY]

Скрипт для чтения и логгирования чата Devman

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        IP адресс чата 
  --port PORT        port чата 
  --history HISTORY  Лог файл чата 
```

## Отправка сообщения в чат

Для отправки сообщения в чат Девман запустите скрипт: 

`python3 write_to_minechat.py HELLO_DEVMAN --host 192.168.0.1 --port 5001 --token asd123`

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


### .env
Для удобства параметры ниже можно добавить в окружение или передать через *.env* файл созданный в корне приложения
```
HOST = 192.168.0.1
LISTEN_PORT = 1234
WRITE_PORT = 1234
HISTORY = ./minechat.log
TOKEN = abc123qwe456
```
