import asyncio
import datetime
from pathlib import Path

import aiofiles
from dotenv import load_dotenv
from requests import ConnectionError

from core.cli import parse_args_listen
from core.coroutines.connect import open_connection


async def read_chat(host, port, history):
    reconnect_count = 0
    while True:
        try:
            async with open_connection(host, port) as conn:
                reader, _ = conn
                while True:
                    data = await reader.readline()

                    message_text = data.decode()
                    message_time = datetime.datetime.now().strftime('[%d.%m.%y %H:%M]')
                    message = f'{message_time} {message_text}'

                    async with aiofiles.open(history, mode='a', encoding='utf-8') as f:
                        await f.write(message)
                    print(message)
        except ConnectionError:
            if reconnect_count > 5:
                await asyncio.sleep(5)
            reconnect_count += 1


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_listen()
    try:
        asyncio.run(read_chat(args.host, args.port, args.history))
    except KeyboardInterrupt:
        print(f'Ручное закрытие скрипта. Лог переписки в {Path().cwd() / args.history}')
