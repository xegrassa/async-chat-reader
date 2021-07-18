import configargparse


def parse_args_listen():
    p = configargparse.ArgParser(description='Скрипт для чтения и логирования чата Devman')
    p.add_argument('--host', default='minechat.dvmn.org', env_var='HOST', help='IP адресс чата')
    p.add_argument('--port', default='5000', env_var='LISTEN_PORT', help='port чата')
    p.add_argument('--history', default='./minechat.log', env_var='HISTORY', help='Файл логов чата')
    args = p.parse_args()
    return args


def parse_args_write():
    p = configargparse.ArgParser(default_config_files=['token.txt'],
                                 description='Скрипт для отправки сообщения в чат Devman')
    p.add_argument('message', help='Сообщение для чата')
    p.add_argument('--host', default='minechat.dvmn.org', env_var='HOST', help='IP адресс чата')
    p.add_argument('--port', default='5050', env_var='WRITE_PORT', help='port чата')
    p.add_argument('--token', env_var='TOKEN', help='Токен')
    p.add_argument('--name', default='anonymous', help='Имя пользователя для регистрации')
    args = p.parse_args()
    return args
