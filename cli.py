import configargparse


p = configargparse.ArgParser(default_config_files='config')
p.add_argument('--host', help='IP адресс чата с перипиской')
p.add_argument('--port', help='port чата с перипиской')

args = p.parse_args()

print(args)