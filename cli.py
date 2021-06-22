import configargparse


def parse_args():
    p = configargparse.ArgParser()
    p.add_argument('--host', env_var='HOST', help='IP адресс чата с перипиской')
    p.add_argument('--port', env_var='PORT', help='port чата с перипиской')
    p.add_argument('--history', env_var='HISTORY', help='файл логов чата')
    args = p.parse_args()
    return args