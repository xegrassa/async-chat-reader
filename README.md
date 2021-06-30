#Девман чат

##Чтение чата

Чтобы почитать чат Девман запустите скрипт: 

`python3 listen-minechat.py --host 192.168.0.1 \
--port 5001 --history ~/minechat.history`

```
usage: listen_minechat.py [-h] [--host HOST] [--port PORT] [--history HISTORY]

Скрипт для чтения и логгирования чата Devman

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        IP адресс чата 
  --port PORT        port чата 
  --history HISTORY  Лог файл чата 
```

Можно добавить аргументы в **.env** файл в корне приложения или в само окружение
```
HOST = 192.168.0.1
LISTEN_PORT = 1234
HISTORY = ./minechat.log
```


##Написать сообщение в чат

